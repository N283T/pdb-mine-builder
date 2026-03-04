"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires database)"
    )


# =============================================================================
# Path fixtures
# =============================================================================


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def pdbj_fixtures_dir(fixtures_dir: Path) -> Path:
    """Return the pdbj fixtures directory."""
    return fixtures_dir / "pdbj"


@pytest.fixture
def cc_fixtures_dir(fixtures_dir: Path) -> Path:
    """Return the cc fixtures directory."""
    return fixtures_dir / "cc"


@pytest.fixture
def ccmodel_fixtures_dir(fixtures_dir: Path) -> Path:
    """Return the ccmodel fixtures directory."""
    return fixtures_dir / "ccmodel"


@pytest.fixture
def prd_fixtures_dir(fixtures_dir: Path) -> Path:
    """Return the prd fixtures directory."""
    return fixtures_dir / "prd"


# =============================================================================
# Database fixtures (for integration tests)
# =============================================================================


@pytest.fixture(scope="session")
def test_conninfo() -> str:
    """Return the connection string for the test database.

    This connects to the Docker PostgreSQL container started by
    `pixi run test-db-up`.
    """
    return (
        "host=localhost port=15433 dbname=mine2_test user=pdbj password=test_password"
    )


@pytest.fixture(scope="session")
def db_connection(test_conninfo: str):
    """Create a database connection for the test session.

    This fixture creates a connection pool that can be used by all
    integration tests in the session.
    """
    import psycopg

    # Test the connection
    with psycopg.connect(test_conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")

    yield test_conninfo


# =============================================================================
# Schema fixtures (for integration tests)
# =============================================================================


@pytest.fixture(scope="session")
def pdbj_metadata():
    """Load the pdbj schema metadata."""
    from mine2.models import get_metadata

    return get_metadata("pdbj")


@pytest.fixture(scope="session")
def cc_metadata():
    """Load the cc schema metadata."""
    from mine2.models import get_metadata

    return get_metadata("cc")


@pytest.fixture(scope="session")
def ccmodel_metadata():
    """Load the ccmodel schema metadata."""
    from mine2.models import get_metadata

    return get_metadata("ccmodel")


@pytest.fixture(scope="session")
def prd_metadata():
    """Load the prd schema metadata."""
    from mine2.models import get_metadata

    return get_metadata("prd")


@pytest.fixture(scope="function")
def pdbj_schema(db_connection: str, pdbj_metadata):
    """Ensure pdbj schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema, get_all_tables

    # Create schema and tables
    ensure_schema(pdbj_metadata, db_connection)

    yield pdbj_metadata

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in get_all_tables(pdbj_metadata):
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(pdbj_metadata.schema, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def cc_schema(db_connection: str, cc_metadata):
    """Ensure cc schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema, get_all_tables

    # Create schema and tables
    ensure_schema(cc_metadata, db_connection)

    yield cc_metadata

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in get_all_tables(cc_metadata):
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(cc_metadata.schema, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def ccmodel_schema(db_connection: str, ccmodel_metadata):
    """Ensure ccmodel schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema, get_all_tables

    # Create schema and tables
    ensure_schema(ccmodel_metadata, db_connection)

    yield ccmodel_metadata

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in get_all_tables(ccmodel_metadata):
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(ccmodel_metadata.schema, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def prd_schema(db_connection: str, prd_metadata):
    """Ensure prd schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema, get_all_tables

    # Create schema and tables
    ensure_schema(prd_metadata, db_connection)

    yield prd_metadata

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in get_all_tables(prd_metadata):
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(prd_metadata.schema, table_name)
                    )
                )
        conn.commit()
