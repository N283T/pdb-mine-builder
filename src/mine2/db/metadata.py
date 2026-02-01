"""Pipeline metadata management.

Tracks when each pipeline was last updated.
"""

from datetime import datetime, timezone

import psycopg


def ensure_metadata_table(conninfo: str) -> None:
    """Create pipeline_metadata table if it doesn't exist.

    Args:
        conninfo: Database connection string
    """
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.pipeline_metadata (
                    schema_name TEXT PRIMARY KEY,
                    last_updated TIMESTAMPTZ NOT NULL,
                    entries_count INT
                )
            """)
        conn.commit()


def update_pipeline_metadata(
    conninfo: str,
    schema_name: str,
    entries_count: int | None = None,
) -> None:
    """Update the last_updated timestamp for a pipeline.

    Args:
        conninfo: Database connection string
        schema_name: Schema name (e.g., 'pdbj', 'cc')
        entries_count: Optional count of entries processed
    """
    now = datetime.now(timezone.utc)

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.pipeline_metadata (schema_name, last_updated, entries_count)
                VALUES (%s, %s, %s)
                ON CONFLICT (schema_name) DO UPDATE SET
                    last_updated = EXCLUDED.last_updated,
                    entries_count = COALESCE(EXCLUDED.entries_count, pipeline_metadata.entries_count)
                """,
                (schema_name, now, entries_count),
            )
        conn.commit()


def get_pipeline_metadata(
    cur: psycopg.Cursor,
    schema_name: str,
) -> tuple[datetime | None, int | None]:
    """Get metadata for a pipeline.

    Args:
        cur: Database cursor
        schema_name: Schema name

    Returns:
        Tuple of (last_updated, entries_count)
    """
    # Check if table exists
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'pipeline_metadata'
        )
        """
    )
    result = cur.fetchone()
    if not result or not result[0]:
        return None, None

    cur.execute(
        "SELECT last_updated, entries_count FROM public.pipeline_metadata WHERE schema_name = %s",
        (schema_name,),
    )
    result = cur.fetchone()
    if result:
        return result[0], result[1]
    return None, None
