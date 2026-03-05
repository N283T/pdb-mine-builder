"""Alembic environment configuration for multi-schema migrations.

Combines all MINE2 schema MetaData objects into a single target for
autogenerate support. Connection URL is resolved from the PMB_DB_URL
environment variable or falls back to the default development URL.
"""

from __future__ import annotations

import logging
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import MetaData, engine_from_config, pool

from pdbminebuilder.models import ALL_METADATA

# -- Alembic Config object ---------------------------------------------------

config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -- Database URL -------------------------------------------------------------

_DEFAULT_URL = "postgresql+psycopg://pdbj@localhost:5433/pmb"
_db_url = os.environ.get("PMB_DB_URL")
if _db_url is None:
    logging.getLogger("alembic.env").warning(
        "PMB_DB_URL not set, using default development URL: %s",
        _DEFAULT_URL,
    )
    _db_url = _DEFAULT_URL
config.set_main_option("sqlalchemy.url", _db_url)

# -- Target metadata (combined from all schemas) ------------------------------

target_metadata = MetaData()
for _schema_meta in ALL_METADATA.values():
    for _table in _schema_meta.tables.values():
        _table.to_metadata(target_metadata)

# -- Schema filter ------------------------------------------------------------

PMB_SCHEMAS: frozenset[str] = frozenset(
    m.schema for m in ALL_METADATA.values() if m.schema is not None
)


def include_name(
    name: str | None,
    type_: str,
    parent_names: dict[str, str | None],
) -> bool:
    """Filter objects to only include MINE2-managed schemas."""
    if type_ == "schema":
        return name in PMB_SCHEMAS
    return True


# -- Migration runners --------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures the context with just a URL so that an Engine (and DBAPI)
    is not required.  Calls to ``context.execute()`` emit SQL strings to
    the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        version_table_schema="public",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            version_table_schema="public",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
