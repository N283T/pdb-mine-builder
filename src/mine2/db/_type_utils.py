"""SQLAlchemy type to PostgreSQL type string utilities."""

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Double,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeEngine


def sa_type_to_pg(sa_type: TypeEngine) -> str:
    """Convert a SQLAlchemy type instance to its PostgreSQL type string.

    Order matters for subclass relationships in SQLAlchemy 2.x:
    - Text before String (Text extends String)
    - BigInteger before Integer (BigInteger extends Integer)
    - Double before Float (Double extends Float via Numeric)

    Args:
        sa_type: A SQLAlchemy type instance (e.g. ``Integer()``, ``Text()``).

    Returns:
        The corresponding PostgreSQL type string (e.g. ``"integer"``, ``"text"``).
    """
    if isinstance(sa_type, ARRAY):
        item = sa_type_to_pg(sa_type.item_type)
        return f"{item}[]"
    # Text before String (Text is a subclass of String)
    if isinstance(sa_type, Text):
        return "text"
    if isinstance(sa_type, String):
        length = sa_type.length
        return f"char({length})" if length else "text"
    # BigInteger before Integer (BigInteger is a subclass of Integer)
    if isinstance(sa_type, BigInteger):
        return "bigint"
    if isinstance(sa_type, Integer):
        return "integer"
    # Double before Float (Double is a subclass of Float)
    if isinstance(sa_type, Double):
        return "double precision"
    if isinstance(sa_type, Float):
        return "real"
    if isinstance(sa_type, Date):
        return "date"
    if isinstance(sa_type, DateTime):
        if sa_type.timezone:
            return "timestamp with time zone"
        return "timestamp without time zone"
    if isinstance(sa_type, Boolean):
        return "boolean"
    if isinstance(sa_type, JSONB):
        return "jsonb"
    return str(sa_type)
