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
    return "host=localhost port=15433 dbname=mine2_test user=pdbj password=test_password"


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
def pdbj_schema_def():
    """Load the pdbj schema definition."""
    from mine2.db.loader import load_schema_def

    return load_schema_def(Path("schemas/pdbj.def.yml"))


@pytest.fixture(scope="session")
def cc_schema_def():
    """Load the cc schema definition."""
    from mine2.db.loader import load_schema_def

    return load_schema_def(Path("schemas/cc.def.yml"))


@pytest.fixture(scope="session")
def ccmodel_schema_def():
    """Load the ccmodel schema definition."""
    from mine2.db.loader import load_schema_def

    return load_schema_def(Path("schemas/ccmodel.def.yml"))


@pytest.fixture(scope="session")
def prd_schema_def():
    """Load the prd schema definition."""
    from mine2.db.loader import load_schema_def

    return load_schema_def(Path("schemas/prd.def.yml"))


@pytest.fixture(scope="function")
def pdbj_schema(db_connection: str, pdbj_schema_def):
    """Ensure pdbj schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema

    # Create schema and tables
    ensure_schema(pdbj_schema_def, db_connection)

    yield pdbj_schema_def

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in pdbj_schema_def.tables:
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(pdbj_schema_def.schema_name, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def cc_schema(db_connection: str, cc_schema_def):
    """Ensure cc schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema

    # Create schema and tables
    ensure_schema(cc_schema_def, db_connection)

    yield cc_schema_def

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in cc_schema_def.tables:
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(cc_schema_def.schema_name, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def ccmodel_schema(db_connection: str, ccmodel_schema_def):
    """Ensure ccmodel schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema

    # Create schema and tables
    ensure_schema(ccmodel_schema_def, db_connection)

    yield ccmodel_schema_def

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in ccmodel_schema_def.tables:
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(ccmodel_schema_def.schema_name, table_name)
                    )
                )
        conn.commit()


@pytest.fixture(scope="function")
def prd_schema(db_connection: str, prd_schema_def):
    """Ensure prd schema and tables exist, cleanup after test."""
    import psycopg
    from psycopg import sql

    from mine2.db.loader import ensure_schema

    # Create schema and tables
    ensure_schema(prd_schema_def, db_connection)

    yield prd_schema_def

    # Cleanup: truncate all tables in the schema
    with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            for table in prd_schema_def.tables:
                table_name = table.name.lower()
                cur.execute(
                    sql.SQL("TRUNCATE TABLE {} CASCADE").format(
                        sql.Identifier(prd_schema_def.schema_name, table_name)
                    )
                )
        conn.commit()
