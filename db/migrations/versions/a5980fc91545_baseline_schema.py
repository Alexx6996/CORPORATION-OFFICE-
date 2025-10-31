"""baseline schema

Revision ID: a5980fc91545
Revises: 
Create Date: 2025-10-28 18:38:20.729189

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'a5980fc91545'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass


