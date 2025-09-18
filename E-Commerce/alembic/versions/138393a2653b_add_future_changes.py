"""add future changes

Revision ID: 138393a2653b
Revises: f42324af7b60
Create Date: 2025-09-18 12:40:15.896741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '138393a2653b'
down_revision: Union[str, Sequence[str], None] = 'f42324af7b60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
