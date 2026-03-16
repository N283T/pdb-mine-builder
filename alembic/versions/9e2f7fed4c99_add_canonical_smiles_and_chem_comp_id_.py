"""add canonical_smiles and chem_comp_id to prd brief_summary

Revision ID: 9e2f7fed4c99
Revises: bf39ba596b4a
Create Date: 2026-03-16 10:59:05.745158

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e2f7fed4c99"
down_revision: Union[str, Sequence[str], None] = "bf39ba596b4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add canonical_smiles and chem_comp_id columns to prd.brief_summary."""
    op.add_column(
        "brief_summary",
        sa.Column(
            "canonical_smiles",
            sa.Text(),
            nullable=True,
            comment="Canonical SMILES from PRDCC block via ccd2rdmol",
        ),
        schema="prd",
    )
    op.add_column(
        "brief_summary",
        sa.Column(
            "chem_comp_id",
            sa.Text(),
            nullable=True,
            comment="Linked CCD comp_id (from pdbx_reference_molecule)",
        ),
        schema="prd",
    )


def downgrade() -> None:
    """Remove canonical_smiles and chem_comp_id columns from prd.brief_summary."""
    op.drop_column("brief_summary", "chem_comp_id", schema="prd")
    op.drop_column("brief_summary", "canonical_smiles", schema="prd")
