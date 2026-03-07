"""prd_family: replace docid with name in brief_summary

Revision ID: bf39ba596b4a
Revises:
Create Date: 2026-03-07 11:53:56.043789

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bf39ba596b4a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "prd_family"
TABLE = "brief_summary"


def upgrade() -> None:
    """Remove docid column and add name column to prd_family.brief_summary."""
    op.drop_column(TABLE, "docid", schema=SCHEMA)
    op.add_column(TABLE, sa.Column("name", sa.Text(), nullable=True), schema=SCHEMA)


def downgrade() -> None:
    """Restore docid column and remove name column."""
    op.drop_column(TABLE, "name", schema=SCHEMA)
    op.add_column(
        TABLE, sa.Column("docid", sa.BigInteger(), nullable=True), schema=SCHEMA
    )
