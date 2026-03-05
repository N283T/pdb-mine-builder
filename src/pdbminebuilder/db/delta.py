"""Delta detection and transactional update support.

Ported from original mine2updater rdb-helper.js deltaTable() and updateRDB().
"""

import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import psycopg
import psycopg.rows
from psycopg import sql

logger = logging.getLogger("pdbminebuilder.db.delta")


@dataclass
class RowDelta:
    """Delta information for a single row."""

    # For updates: (db_row_index, new_row_index, changed_columns)
    # For inserts: new_row_index only
    # For deletes: db_row_index only
    db_idx: int | None = None
    new_idx: int | None = None
    changed_columns: list[str] = field(default_factory=list)


@dataclass
class TableDelta:
    """Delta for a single table."""

    table_name: str
    inserts: list[int] = field(default_factory=list)  # Indices into new_rows
    updates: list[RowDelta] = field(default_factory=list)
    deletes: list[int] = field(default_factory=list)  # Indices into db_rows

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return bool(self.inserts or self.updates or self.deletes)


@dataclass
class DeltaResult:
    """Result of delta computation for all tables."""

    entry_id: str
    tables: dict[str, TableDelta] = field(default_factory=dict)
    is_new_entry: bool = False  # True if brief_summary doesn't exist in DB

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes across all tables."""
        return any(t.has_changes for t in self.tables.values())

    @property
    def total_inserts(self) -> int:
        """Total number of rows to insert."""
        return sum(len(t.inserts) for t in self.tables.values())

    @property
    def total_updates(self) -> int:
        """Total number of rows to update."""
        return sum(len(t.updates) for t in self.tables.values())

    @property
    def total_deletes(self) -> int:
        """Total number of rows to delete."""
        return sum(len(t.deletes) for t in self.tables.values())


def _make_pk_key(row: dict[str, Any], pk_columns: list[str]) -> tuple:
    """Create a hashable key from primary key columns.

    Args:
        row: Row dict
        pk_columns: List of primary key column names

    Returns:
        Tuple of primary key values (hashable)
    """
    key_values = []
    for col in pk_columns:
        val = row.get(col)
        # Handle Date/datetime for comparison (convert to timestamp)
        if isinstance(val, (date, datetime)):
            val = val.isoformat()
        # Handle lists (convert to tuple for hashability)
        if isinstance(val, list):
            val = tuple(val)
        key_values.append(val)
    return tuple(key_values)


def _values_equal(val1: Any, val2: Any) -> bool:
    """Compare two values for equality.

    Handles special cases:
    - Date/datetime comparison
    - Array comparison
    - None handling

    Args:
        val1: First value (from DB)
        val2: Second value (from new data)

    Returns:
        True if values are equal
    """
    # Handle None
    if val1 is None and val2 is None:
        return True
    if val1 is None or val2 is None:
        return False

    # Handle dates
    if isinstance(val1, (date, datetime)):
        if isinstance(val2, str):
            # Convert string to date for comparison
            try:
                if isinstance(val1, datetime):
                    val2 = datetime.fromisoformat(val2)
                else:
                    val2 = date.fromisoformat(val2)
            except ValueError:
                return False
        if isinstance(val2, (date, datetime)):
            return val1 == val2
        return False

    # Handle arrays
    if isinstance(val1, list) and isinstance(val2, list):
        if len(val1) != len(val2):
            return False
        return all(v1 == v2 for v1, v2 in zip(val1, val2, strict=False))

    # Default comparison
    return val1 == val2


def compute_table_delta(
    table_name: str,
    db_rows: list[dict[str, Any]],
    new_rows: list[dict[str, Any]],
    pk_columns: list[str],
    columns: list[str],
    ignore_columns: list[str] | None = None,
) -> TableDelta:
    """Compute delta between database rows and new rows for a single table.

    Args:
        table_name: Name of the table
        db_rows: Current rows from database
        new_rows: New rows from mmJSON/CIF
        pk_columns: Primary key column names (not including entry_id)
        columns: All column names to compare
        ignore_columns: Columns to ignore during comparison (e.g., update_date)

    Returns:
        TableDelta with inserts, updates, deletes
    """
    ignore_set = set(ignore_columns or [])
    compare_columns = [
        c for c in columns if c not in ignore_set and c not in pk_columns
    ]

    delta = TableDelta(table_name=table_name)

    # Build hash map for DB rows
    db_hash: dict[tuple, int] = {}
    for idx, row in enumerate(db_rows):
        key = _make_pk_key(row, pk_columns)
        db_hash[key] = idx

    # Build hash map for new rows
    new_hash: dict[tuple, int] = {}
    for idx, row in enumerate(new_rows):
        key = _make_pk_key(row, pk_columns)
        new_hash[key] = idx

    # Find inserts and updates
    for key, new_idx in new_hash.items():
        if key in db_hash:
            # Row exists in both - check for updates
            db_idx = db_hash[key]
            db_row = db_rows[db_idx]
            new_row = new_rows[new_idx]

            changed_cols = []
            for col in compare_columns:
                db_val = db_row.get(col)
                new_val = new_row.get(col)
                if not _values_equal(db_val, new_val):
                    changed_cols.append(col)

            if changed_cols:
                delta.updates.append(
                    RowDelta(
                        db_idx=db_idx, new_idx=new_idx, changed_columns=changed_cols
                    )
                )
        else:
            # Row only in new - insert
            delta.inserts.append(new_idx)

    # Find deletes
    for key, db_idx in db_hash.items():
        if key not in new_hash:
            delta.deletes.append(db_idx)

    return delta


def compute_delta(
    entry_id: str,
    db_data: dict[str, list[dict[str, Any]]],
    new_data: dict[str, list[dict[str, Any]]],
    table_pk_columns: dict[str, list[str]],
    table_columns: dict[str, list[str]],
) -> DeltaResult:
    """Compute delta between database data and new data for all tables.

    Args:
        entry_id: Entry identifier (e.g., pdbid)
        db_data: Current data from database {table_name: [rows...]}
        new_data: New data from mmJSON/CIF {table_name: [rows...]}
        table_pk_columns: Primary key columns per table (excluding entry_id)
        table_columns: All columns per table

    Returns:
        DeltaResult with deltas for all tables
    """
    result = DeltaResult(entry_id=entry_id)

    # Check if this is a new entry (no brief_summary in DB)
    if "brief_summary" in db_data:
        brief_db_rows = db_data.get("brief_summary", [])
        result.is_new_entry = len(brief_db_rows) == 0
    else:
        result.is_new_entry = True

    # Get all tables from both sources
    all_tables = set(db_data.keys()) | set(new_data.keys())

    for table_name in all_tables:
        db_rows = db_data.get(table_name, [])
        new_rows = new_data.get(table_name, [])
        pk_cols = table_pk_columns.get(table_name, [])
        columns = table_columns.get(table_name, [])

        # For brief_summary, ignore update_date during comparison
        ignore_cols = ["update_date"] if table_name == "brief_summary" else None

        delta = compute_table_delta(
            table_name=table_name,
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=pk_cols,
            columns=columns,
            ignore_columns=ignore_cols,
        )

        if delta.has_changes:
            result.tables[table_name] = delta

    return result


def apply_delta(
    conninfo: str,
    schema: str,
    entry_id: str,
    pk_column: str,
    delta: DeltaResult,
    new_data: dict[str, list[dict[str, Any]]],
    db_data: dict[str, list[dict[str, Any]]],
    table_pk_columns: dict[str, list[str]],
    set_update_date: date | None = None,
) -> tuple[int, int, int]:
    """Apply delta changes to database in a transaction.

    Processes tables in order: brief_summary first, then others.

    Args:
        conninfo: Database connection string
        schema: Schema name
        entry_id: Entry identifier
        pk_column: Primary key column name (e.g., 'pdbid')
        delta: Computed delta result
        new_data: New rows data {table_name: [rows...]}
        db_data: Current DB rows data {table_name: [rows...]}
        table_pk_columns: Primary key columns per table
        set_update_date: Optional date to set for brief_summary.update_date

    Returns:
        Tuple of (inserted_count, updated_count, deleted_count)
    """
    if not delta.has_changes and set_update_date is None:
        return 0, 0, 0

    inserted = 0
    updated = 0
    deleted = 0

    # Create local mutable copies of data to avoid mutating caller's data
    local_delta_tables = dict(delta.tables)
    local_new_data = dict(new_data)

    # If we need to set update_date on brief_summary
    if set_update_date is not None and not delta.is_new_entry:
        # Add update_date to the changed columns for brief_summary
        if "brief_summary" in local_delta_tables:
            table_delta = local_delta_tables["brief_summary"]
            if table_delta.updates:
                # Create new RowDelta with update_date added to changed columns
                first_update = table_delta.updates[0]
                if "update_date" not in first_update.changed_columns:
                    new_changed_cols = [*first_update.changed_columns, "update_date"]
                    new_first_update = RowDelta(
                        db_idx=first_update.db_idx,
                        new_idx=first_update.new_idx,
                        changed_columns=new_changed_cols,
                    )
                    # Create new TableDelta with updated first row
                    local_delta_tables["brief_summary"] = TableDelta(
                        table_name="brief_summary",
                        inserts=table_delta.inserts,
                        updates=[new_first_update, *table_delta.updates[1:]],
                        deletes=table_delta.deletes,
                    )
            else:
                # No updates, create one just for update_date
                local_delta_tables["brief_summary"] = TableDelta(
                    table_name="brief_summary",
                    inserts=table_delta.inserts,
                    updates=[
                        RowDelta(db_idx=0, new_idx=0, changed_columns=["update_date"])
                    ],
                    deletes=table_delta.deletes,
                )
        elif "brief_summary" in local_new_data:
            # Table has no other changes, but we need to update update_date
            local_delta_tables["brief_summary"] = TableDelta(
                table_name="brief_summary",
                updates=[
                    RowDelta(db_idx=0, new_idx=0, changed_columns=["update_date"])
                ],
            )

        # Set the update_date value in local copy of new_data
        if "brief_summary" in local_new_data and local_new_data["brief_summary"]:
            # Create new dict for brief_summary rows to avoid mutating original
            local_new_data["brief_summary"] = [
                {**local_new_data["brief_summary"][0], "update_date": set_update_date},
                *local_new_data["brief_summary"][1:],
            ]

    # Order tables: brief_summary first
    table_names = list(local_delta_tables.keys())
    if "brief_summary" in table_names:
        table_names.remove("brief_summary")
        table_names.insert(0, "brief_summary")

    with psycopg.connect(conninfo) as conn:
        try:
            with conn.cursor() as cur:
                for table_name in table_names:
                    table_delta = local_delta_tables[table_name]
                    new_rows = local_new_data.get(table_name, [])
                    db_rows = db_data.get(table_name, [])
                    pk_cols = table_pk_columns.get(table_name, [])

                    # Process inserts
                    if table_delta.inserts:
                        ins_count = _apply_inserts(
                            cur,
                            schema,
                            table_name,
                            pk_column,
                            entry_id,
                            new_rows,
                            table_delta.inserts,
                        )
                        inserted += ins_count

                    # Process updates
                    if table_delta.updates:
                        upd_count = _apply_updates(
                            cur,
                            schema,
                            table_name,
                            pk_column,
                            entry_id,
                            pk_cols,
                            new_rows,
                            db_rows,
                            table_delta.updates,
                        )
                        updated += upd_count

                    # Process deletes
                    if table_delta.deletes:
                        del_count = _apply_deletes(
                            cur,
                            schema,
                            table_name,
                            pk_column,
                            entry_id,
                            pk_cols,
                            db_rows,
                            table_delta.deletes,
                        )
                        deleted += del_count

            conn.commit()
        except Exception:
            conn.rollback()
            raise

    return inserted, updated, deleted


def _apply_inserts(
    cur: Any,
    schema: str,
    table_name: str,
    pk_column: str,
    entry_id: str,
    new_rows: list[dict[str, Any]],
    insert_indices: list[int],
) -> int:
    """Apply insert operations.

    Args:
        cur: Database cursor
        schema: Schema name
        table_name: Table name
        pk_column: Entry primary key column name
        entry_id: Entry ID value
        new_rows: New rows data
        insert_indices: Indices of rows to insert

    Returns:
        Number of rows inserted
    """
    if not insert_indices:
        return 0

    # Get columns from first row
    sample_row = new_rows[insert_indices[0]]
    columns = [pk_column] + [c for c in sample_row.keys() if c != pk_column]

    # Build values list
    values_list = []
    for idx in insert_indices:
        row = new_rows[idx]
        values = [entry_id] + [row.get(c) for c in columns[1:]]
        values_list.append(tuple(values))

    # Batch insert
    col_names = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
    placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in columns)
    table = sql.Identifier(schema, table_name)

    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        table, col_names, placeholders
    )

    cur.executemany(query, values_list)
    return len(values_list)


def _apply_updates(
    cur: Any,
    schema: str,
    table_name: str,
    pk_column: str,
    entry_id: str,
    pk_cols: list[str],
    new_rows: list[dict[str, Any]],
    db_rows: list[dict[str, Any]],
    updates: list[RowDelta],
) -> int:
    """Apply update operations.

    Only updates the changed columns, not the entire row.

    Args:
        cur: Database cursor
        schema: Schema name
        table_name: Table name
        pk_column: Entry primary key column name
        entry_id: Entry ID value
        pk_cols: Table-specific primary key columns
        new_rows: New rows data
        db_rows: Current DB rows data
        updates: List of row deltas

    Returns:
        Number of rows updated
    """
    count = 0
    table = sql.Identifier(schema, table_name)

    for row_delta in updates:
        if row_delta.db_idx is None or row_delta.new_idx is None:
            continue

        db_row = db_rows[row_delta.db_idx]
        new_row = new_rows[row_delta.new_idx]
        changed_cols = row_delta.changed_columns

        if not changed_cols:
            continue

        # Build SET clause
        set_parts = []
        values = []
        for col in changed_cols:
            set_parts.append(sql.SQL("{} = %s").format(sql.Identifier(col)))
            values.append(new_row.get(col))

        set_clause = sql.SQL(", ").join(set_parts)

        # Build WHERE clause
        where_parts = [sql.SQL("{} = %s").format(sql.Identifier(pk_column))]
        values.append(entry_id)

        for col in pk_cols:
            where_parts.append(sql.SQL("{} = %s").format(sql.Identifier(col)))
            values.append(db_row.get(col))

        where_clause = sql.SQL(" AND ").join(where_parts)

        query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            table, set_clause, where_clause
        )
        cur.execute(query, values)
        count += 1

    return count


def _apply_deletes(
    cur: Any,
    schema: str,
    table_name: str,
    pk_column: str,
    entry_id: str,
    pk_cols: list[str],
    db_rows: list[dict[str, Any]],
    delete_indices: list[int],
) -> int:
    """Apply delete operations.

    Args:
        cur: Database cursor
        schema: Schema name
        table_name: Table name
        pk_column: Entry primary key column name
        entry_id: Entry ID value
        pk_cols: Table-specific primary key columns
        db_rows: Current DB rows data
        delete_indices: Indices of rows to delete

    Returns:
        Number of rows deleted
    """
    count = 0
    table = sql.Identifier(schema, table_name)

    for db_idx in delete_indices:
        db_row = db_rows[db_idx]

        # Build WHERE clause
        where_parts = [sql.SQL("{} = %s").format(sql.Identifier(pk_column))]
        values = [entry_id]

        for col in pk_cols:
            where_parts.append(sql.SQL("{} = %s").format(sql.Identifier(col)))
            values.append(db_row.get(col))

        where_clause = sql.SQL(" AND ").join(where_parts)

        query = sql.SQL("DELETE FROM {} WHERE {}").format(table, where_clause)
        cur.execute(query, values)
        count += 1

    return count


def fetch_entry_data(
    conninfo: str,
    schema: str,
    entry_id: str,
    pk_column: str,
    tables: list[str],
) -> dict[str, list[dict[str, Any]]]:
    """Fetch current data for an entry from the database.

    Args:
        conninfo: Database connection string
        schema: Schema name
        entry_id: Entry identifier
        pk_column: Primary key column name
        tables: List of table names to fetch

    Returns:
        Dict mapping table names to lists of row dicts
    """
    result: dict[str, list[dict[str, Any]]] = {}

    with psycopg.connect(conninfo) as conn:
        conn.row_factory = psycopg.rows.dict_row  # type: ignore[assignment]
        with conn.cursor() as cur:
            for table_name in tables:
                table = sql.Identifier(schema, table_name)
                pk_col = sql.Identifier(pk_column)

                query = sql.SQL("SELECT * FROM {} WHERE {} = %s").format(table, pk_col)

                try:
                    cur.execute(query, (entry_id,))
                    rows = cur.fetchall()
                    # dict_row factory returns dict[str, Any]
                    result[table_name] = [dict(row) for row in rows]
                except psycopg.errors.UndefinedTable:
                    # Table doesn't exist yet; rollback to clear
                    # the aborted transaction state
                    conn.rollback()
                    result[table_name] = []

    return result


def entry_exists(
    conninfo: str,
    schema: str,
    entry_id: str,
    pk_column: str,
) -> bool:
    """Check if an entry exists in brief_summary.

    Args:
        conninfo: Database connection string
        schema: Schema name
        entry_id: Entry identifier
        pk_column: Primary key column name

    Returns:
        True if the entry exists in brief_summary, False otherwise
        (including when the table does not yet exist).
    """
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            table = sql.Identifier(schema, "brief_summary")
            pk_col = sql.Identifier(pk_column)
            query = sql.SQL("SELECT 1 FROM {} WHERE {} = %s LIMIT 1").format(
                table, pk_col
            )
            try:
                cur.execute(query, (entry_id,))
                return cur.fetchone() is not None
            except psycopg.errors.UndefinedTable:
                conn.rollback()
                logger.warning(
                    "brief_summary table does not exist in schema %r; "
                    "treating entry %r as new",
                    schema,
                    entry_id,
                )
                return False


def insert_new_entry(
    conninfo: str,
    schema: str,
    entry_id: str,
    pk_column: str,
    table_rows: dict[str, list[dict[str, Any]]],
) -> int:
    """Fast-path insert for a new entry (no delta sync needed).

    Inserts all rows directly in a single transaction.
    brief_summary is inserted first to satisfy foreign key constraints.

    Args:
        conninfo: Database connection string
        schema: Schema name
        entry_id: Entry identifier
        pk_column: Primary key column name
        table_rows: Dict mapping table names to lists of row dicts

    Returns:
        Total number of rows inserted
    """
    # Filter to tables with actual data
    tables_with_data = {k: v for k, v in table_rows.items() if v}
    if not tables_with_data:
        logger.warning(
            "insert_new_entry called for %r with no data rows",
            entry_id,
        )
        return 0

    if "brief_summary" not in tables_with_data:
        raise ValueError(
            f"Cannot insert new entry {entry_id!r}: brief_summary data is missing. "
            f"Available tables: {sorted(tables_with_data.keys())}"
        )

    total_inserted = 0

    # Order: brief_summary first (FK constraint)
    table_names = list(tables_with_data.keys())
    table_names.remove("brief_summary")
    table_names.insert(0, "brief_summary")

    current_table = "<unknown>"
    with psycopg.connect(conninfo) as conn:
        try:
            with conn.cursor() as cur:
                for table_name in table_names:
                    current_table = table_name
                    rows = tables_with_data[table_name]
                    if not rows:
                        continue

                    # Build column list: entry PK first (not in parsed row
                    # data), then all columns from the parsed row
                    sample_row = rows[0]
                    columns = [pk_column] + [
                        c for c in sample_row.keys() if c != pk_column
                    ]

                    col_names = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
                    placeholders = sql.SQL(", ").join(
                        sql.Placeholder() for _ in columns
                    )
                    table = sql.Identifier(schema, table_name)

                    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                        table, col_names, placeholders
                    )

                    values_list = [
                        tuple([entry_id] + [row.get(c) for c in columns[1:]])
                        for row in rows
                    ]

                    cur.executemany(query, values_list)
                    total_inserted += len(values_list)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(
                f"Fast-path insert failed for entry {entry_id!r} "
                f"on table {current_table!r} in schema {schema!r}: {e}"
            ) from e

    return total_inserted
