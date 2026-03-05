"""SQLAlchemy model definitions registry.

Model modules are imported here and exposed via
``ALL_METADATA`` and ``get_metadata()``.
"""

from __future__ import annotations

from sqlalchemy import MetaData

from pdbminebuilder.models import (
    cc,
    ccmodel,
    contacts,
    emdb,
    ihm,
    pdbj,
    prd,
    prd_family,
    sifts,
    vrpt,
)

ALL_METADATA: dict[str, MetaData] = {
    "cc": cc.metadata,
    "ccmodel": ccmodel.metadata,
    "contacts": contacts.metadata,
    "emdb": emdb.metadata,
    "ihm": ihm.metadata,
    "pdbj": pdbj.metadata,
    "prd": prd.metadata,
    "prd_family": prd_family.metadata,
    "sifts": sifts.metadata,
    "vrpt": vrpt.metadata,
}


def get_metadata(schema_name: str) -> MetaData:
    """Return the MetaData object for the given schema name.

    Args:
        schema_name: One of the registered schema names.

    Returns:
        The SQLAlchemy MetaData instance for that schema.

    Raises:
        KeyError: If the schema name is not registered.
    """
    try:
        return ALL_METADATA[schema_name]
    except KeyError:
        available = ", ".join(sorted(ALL_METADATA))
        msg = f"Unknown schema {schema_name!r}. Available schemas: {available}"
        raise KeyError(msg) from None
