"""PostgreSQL connection management using psycopg3."""

from contextlib import contextmanager
from typing import Any, Iterator, Sequence

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from rich.console import Console

console = Console()

_pool: ConnectionPool[psycopg.Connection[dict[str, Any]]] | None = None


def init_pool(
    conninfo: str,
    min_size: int = 1,
    max_size: int = 10,
    timeout: float = 30.0,
) -> ConnectionPool[psycopg.Connection[dict[str, Any]]]:
    """Initialize the connection pool.

    Args:
        conninfo: PostgreSQL connection string
        min_size: Minimum number of connections
        max_size: Maximum number of connections
        timeout: Timeout for acquiring a connection (seconds)
    """
    global _pool
    if _pool is not None:
        _pool.close()

    _pool = ConnectionPool(
        conninfo=conninfo,
        min_size=min_size,
        max_size=max_size,
        timeout=timeout,
        kwargs={"row_factory": dict_row},
    )
    return _pool


def get_pool() -> ConnectionPool[psycopg.Connection[dict[str, Any]]]:
    """Get the connection pool."""
    if _pool is None:
        raise RuntimeError("Connection pool not initialized. Call init_pool() first.")
    return _pool


def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


@contextmanager
def get_connection() -> Iterator[psycopg.Connection[dict[str, Any]]]:
    """Get a connection from the pool."""
    pool = get_pool()
    with pool.connection() as conn:
        yield conn


def execute(
    query: sql.SQL | sql.Composed | str,
    params: Sequence[Any] | dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a query and return results."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)  # type: ignore[arg-type]
            if cur.description:
                return list(cur.fetchall())
            return []


def executemany(
    query: sql.SQL | sql.Composed | str,
    params_seq: Sequence[Sequence[Any] | dict[str, Any]],
) -> None:
    """Execute a query with multiple parameter sets."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, params_seq)  # type: ignore[arg-type]
        conn.commit()


def execute_batch(
    query: sql.SQL | sql.Composed | str,
    params_seq: Sequence[Sequence[Any] | dict[str, Any]],
    page_size: int = 1000,
) -> None:
    """Execute a query in batches for better performance."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Use copy for bulk inserts when possible
            for i in range(0, len(params_seq), page_size):
                batch = params_seq[i : i + page_size]
                cur.executemany(query, batch)  # type: ignore[arg-type]
        conn.commit()


def table_exists(table_name: str, schema: str = "public") -> bool:
    """Check if a table exists."""
    result = execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        )
        """,
        (schema, table_name),
    )
    return result[0]["exists"] if result else False


def create_schema_if_not_exists(schema: str) -> None:
    """Create a schema if it doesn't exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema))
            )
        conn.commit()
