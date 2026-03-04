"""Tests for mine2.db._type_utils module."""

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

from mine2.db._type_utils import sa_type_to_pg


class TestSaTypeToPg:
    """Tests for sa_type_to_pg conversion function."""

    def test_text(self) -> None:
        assert sa_type_to_pg(Text()) == "text"

    def test_integer(self) -> None:
        assert sa_type_to_pg(Integer()) == "integer"

    def test_bigint(self) -> None:
        assert sa_type_to_pg(BigInteger()) == "bigint"

    def test_double(self) -> None:
        assert sa_type_to_pg(Double()) == "double precision"

    def test_real(self) -> None:
        assert sa_type_to_pg(Float()) == "real"

    def test_date(self) -> None:
        assert sa_type_to_pg(Date()) == "date"

    def test_timestamp(self) -> None:
        assert sa_type_to_pg(DateTime()) == "timestamp without time zone"

    def test_timestamptz(self) -> None:
        assert sa_type_to_pg(DateTime(timezone=True)) == "timestamp with time zone"

    def test_boolean(self) -> None:
        assert sa_type_to_pg(Boolean()) == "boolean"

    def test_text_array(self) -> None:
        assert sa_type_to_pg(ARRAY(Text)) == "text[]"

    def test_integer_array(self) -> None:
        assert sa_type_to_pg(ARRAY(Integer)) == "integer[]"

    def test_double_array(self) -> None:
        assert sa_type_to_pg(ARRAY(Double)) == "double precision[]"

    def test_boolean_array(self) -> None:
        assert sa_type_to_pg(ARRAY(Boolean)) == "boolean[]"

    def test_jsonb(self) -> None:
        assert sa_type_to_pg(JSONB()) == "jsonb"

    def test_char(self) -> None:
        assert sa_type_to_pg(String(3)) == "char(3)"

    def test_string_no_length(self) -> None:
        assert sa_type_to_pg(String()) == "text"
