"""Tests for delta detection and transactional updates."""

from datetime import date, datetime


from mine2.db.delta import (
    DeltaResult,
    RowDelta,
    TableDelta,
    _make_pk_key,
    _values_equal,
    compute_delta,
    compute_table_delta,
)


class TestMakePkKey:
    """Tests for _make_pk_key function."""

    def test_single_column_pk(self):
        row = {"id": 1, "name": "test"}
        key = _make_pk_key(row, ["id"])
        assert key == (1,)

    def test_multi_column_pk(self):
        row = {"a": 1, "b": "x", "c": "extra"}
        key = _make_pk_key(row, ["a", "b"])
        assert key == (1, "x")

    def test_handles_date(self):
        row = {"id": 1, "created": date(2024, 1, 15)}
        key = _make_pk_key(row, ["id", "created"])
        assert key == (1, "2024-01-15")

    def test_handles_datetime(self):
        row = {"id": 1, "created": datetime(2024, 1, 15, 10, 30, 0)}
        key = _make_pk_key(row, ["id", "created"])
        assert key == (1, "2024-01-15T10:30:00")

    def test_handles_list(self):
        row = {"id": [1, 2, 3], "name": "test"}
        key = _make_pk_key(row, ["id"])
        assert key == ((1, 2, 3),)

    def test_missing_column_returns_none(self):
        row = {"a": 1}
        key = _make_pk_key(row, ["a", "b"])
        assert key == (1, None)


class TestValuesEqual:
    """Tests for _values_equal function."""

    def test_both_none(self):
        assert _values_equal(None, None) is True

    def test_one_none(self):
        assert _values_equal(None, 1) is False
        assert _values_equal(1, None) is False

    def test_equal_strings(self):
        assert _values_equal("abc", "abc") is True
        assert _values_equal("abc", "def") is False

    def test_equal_numbers(self):
        assert _values_equal(42, 42) is True
        assert _values_equal(42, 43) is False

    def test_date_comparison(self):
        d1 = date(2024, 1, 15)
        d2 = date(2024, 1, 15)
        d3 = date(2024, 1, 16)
        assert _values_equal(d1, d2) is True
        assert _values_equal(d1, d3) is False

    def test_date_with_string(self):
        d = date(2024, 1, 15)
        assert _values_equal(d, "2024-01-15") is True
        assert _values_equal(d, "2024-01-16") is False

    def test_datetime_with_string(self):
        dt = datetime(2024, 1, 15, 10, 30, 0)
        assert _values_equal(dt, "2024-01-15T10:30:00") is True

    def test_list_comparison(self):
        assert _values_equal([1, 2, 3], [1, 2, 3]) is True
        assert _values_equal([1, 2, 3], [1, 2, 4]) is False
        assert _values_equal([1, 2], [1, 2, 3]) is False
        assert _values_equal([], []) is True


class TestComputeTableDelta:
    """Tests for compute_table_delta function."""

    def test_no_changes(self):
        db_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
        new_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.has_changes is False
        assert delta.inserts == []
        assert delta.updates == []
        assert delta.deletes == []

    def test_insert_only(self):
        db_rows = [{"id": 1, "name": "a"}]
        new_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.has_changes is True
        assert delta.inserts == [1]  # Index of new row
        assert delta.updates == []
        assert delta.deletes == []

    def test_delete_only(self):
        db_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
        new_rows = [{"id": 1, "name": "a"}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.has_changes is True
        assert delta.inserts == []
        assert delta.updates == []
        assert delta.deletes == [1]  # Index of db row to delete

    def test_update_only(self):
        db_rows = [{"id": 1, "name": "a"}]
        new_rows = [{"id": 1, "name": "updated"}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.has_changes is True
        assert delta.inserts == []
        assert len(delta.updates) == 1
        assert delta.updates[0].db_idx == 0
        assert delta.updates[0].new_idx == 0
        assert delta.updates[0].changed_columns == ["name"]
        assert delta.deletes == []

    def test_multiple_column_update(self):
        db_rows = [{"id": 1, "name": "a", "value": 10}]
        new_rows = [{"id": 1, "name": "updated", "value": 20}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name", "value"],
        )

        assert len(delta.updates) == 1
        assert set(delta.updates[0].changed_columns) == {"name", "value"}

    def test_mixed_operations(self):
        db_rows = [
            {"id": 1, "name": "a"},  # Will be updated
            {"id": 2, "name": "b"},  # Will be deleted
        ]
        new_rows = [
            {"id": 1, "name": "updated"},  # Update
            {"id": 3, "name": "c"},  # Insert
        ]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.has_changes is True
        assert delta.inserts == [1]  # Index of row with id=3
        assert len(delta.updates) == 1
        assert delta.updates[0].db_idx == 0  # Row with id=1
        assert delta.deletes == [1]  # Index of row with id=2

    def test_composite_pk(self):
        db_rows = [{"a": 1, "b": "x", "value": 100}]
        new_rows = [
            {"a": 1, "b": "x", "value": 200},  # Update
            {"a": 1, "b": "y", "value": 300},  # Insert (different PK)
        ]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["a", "b"],
            columns=["a", "b", "value"],
        )

        assert len(delta.inserts) == 1
        assert len(delta.updates) == 1
        assert delta.updates[0].changed_columns == ["value"]

    def test_ignore_columns(self):
        db_rows = [{"id": 1, "name": "a", "update_date": date(2024, 1, 1)}]
        new_rows = [{"id": 1, "name": "a", "update_date": date(2024, 1, 15)}]

        # Without ignore - should detect update
        delta1 = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name", "update_date"],
        )
        assert delta1.has_changes is True

        # With ignore - should not detect update
        delta2 = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name", "update_date"],
            ignore_columns=["update_date"],
        )
        assert delta2.has_changes is False

    def test_empty_db(self):
        db_rows: list[dict] = []
        new_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.inserts == [0, 1]
        assert delta.updates == []
        assert delta.deletes == []

    def test_empty_new_data(self):
        db_rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
        new_rows: list[dict] = []

        delta = compute_table_delta(
            table_name="test",
            db_rows=db_rows,
            new_rows=new_rows,
            pk_columns=["id"],
            columns=["id", "name"],
        )

        assert delta.inserts == []
        assert delta.updates == []
        assert delta.deletes == [0, 1]


class TestComputeDelta:
    """Tests for compute_delta function."""

    def test_single_table(self):
        db_data = {"table1": [{"id": 1, "name": "a"}]}
        new_data = {"table1": [{"id": 1, "name": "updated"}]}
        table_pk = {"table1": ["id"]}
        table_cols = {"table1": ["id", "name"]}

        result = compute_delta(
            entry_id="test",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        assert result.entry_id == "test"
        assert result.has_changes is True
        assert "table1" in result.tables
        assert len(result.tables["table1"].updates) == 1

    def test_multiple_tables(self):
        db_data = {
            "table1": [{"id": 1, "name": "a"}],
            "table2": [{"id": 1, "value": 100}],
        }
        new_data = {
            "table1": [{"id": 1, "name": "a"}],  # No change
            "table2": [{"id": 1, "value": 200}],  # Update
        }
        table_pk = {"table1": ["id"], "table2": ["id"]}
        table_cols = {"table1": ["id", "name"], "table2": ["id", "value"]}

        result = compute_delta(
            entry_id="test",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        # Only table2 should be in result (table1 has no changes)
        assert "table1" not in result.tables
        assert "table2" in result.tables

    def test_is_new_entry_when_no_brief_summary(self):
        db_data = {"brief_summary": []}
        new_data = {"brief_summary": [{"pdbid": "101d", "title": "Test"}]}
        table_pk = {"brief_summary": []}
        table_cols = {"brief_summary": ["pdbid", "title"]}

        result = compute_delta(
            entry_id="101d",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        assert result.is_new_entry is True

    def test_is_not_new_entry_when_brief_summary_exists(self):
        db_data = {"brief_summary": [{"pdbid": "101d", "title": "Test"}]}
        new_data = {"brief_summary": [{"pdbid": "101d", "title": "Updated"}]}
        table_pk = {"brief_summary": []}
        table_cols = {"brief_summary": ["pdbid", "title"]}

        result = compute_delta(
            entry_id="101d",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        assert result.is_new_entry is False

    def test_brief_summary_ignores_update_date(self):
        db_data = {
            "brief_summary": [
                {"pdbid": "101d", "title": "Test", "update_date": date(2024, 1, 1)}
            ]
        }
        new_data = {
            "brief_summary": [
                {"pdbid": "101d", "title": "Test", "update_date": date(2024, 1, 15)}
            ]
        }
        table_pk = {"brief_summary": []}
        table_cols = {"brief_summary": ["pdbid", "title", "update_date"]}

        result = compute_delta(
            entry_id="101d",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        # update_date should be ignored, so no changes
        assert result.has_changes is False

    def test_total_counts(self):
        db_data = {
            "table1": [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
            "table2": [{"id": 1, "value": 100}],
        }
        new_data = {
            "table1": [
                {"id": 1, "name": "updated"},
                {"id": 3, "name": "c"},
            ],  # 1 update, 1 insert, 1 delete
            "table2": [],  # 1 delete
        }
        table_pk = {"table1": ["id"], "table2": ["id"]}
        table_cols = {"table1": ["id", "name"], "table2": ["id", "value"]}

        result = compute_delta(
            entry_id="test",
            db_data=db_data,
            new_data=new_data,
            table_pk_columns=table_pk,
            table_columns=table_cols,
        )

        assert result.total_inserts == 1
        assert result.total_updates == 1
        assert result.total_deletes == 2


class TestDeltaResult:
    """Tests for DeltaResult dataclass."""

    def test_has_changes_false_when_empty(self):
        result = DeltaResult(entry_id="test")
        assert result.has_changes is False

    def test_has_changes_true_with_inserts(self):
        result = DeltaResult(entry_id="test")
        result.tables["t1"] = TableDelta(table_name="t1", inserts=[0])
        assert result.has_changes is True

    def test_has_changes_true_with_updates(self):
        result = DeltaResult(entry_id="test")
        result.tables["t1"] = TableDelta(
            table_name="t1",
            updates=[RowDelta(db_idx=0, new_idx=0, changed_columns=["col"])],
        )
        assert result.has_changes is True

    def test_has_changes_true_with_deletes(self):
        result = DeltaResult(entry_id="test")
        result.tables["t1"] = TableDelta(table_name="t1", deletes=[0])
        assert result.has_changes is True


class TestTableDelta:
    """Tests for TableDelta dataclass."""

    def test_has_changes_false_when_empty(self):
        delta = TableDelta(table_name="test")
        assert delta.has_changes is False

    def test_has_changes_true_with_any_operation(self):
        delta1 = TableDelta(table_name="test", inserts=[0])
        delta2 = TableDelta(table_name="test", deletes=[0])
        delta3 = TableDelta(
            table_name="test",
            updates=[RowDelta(db_idx=0, new_idx=0, changed_columns=["x"])],
        )

        assert delta1.has_changes is True
        assert delta2.has_changes is True
        assert delta3.has_changes is True
