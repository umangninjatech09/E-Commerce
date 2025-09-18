"""merge heads

Revision ID: f44e1191ed7d
Revises: 4b950b70538b, f53332caed85
Create Date: 2025-09-18 12:38:21.087038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f44e1191ed7d'
down_revision: Union[str, Sequence[str], None] = ('4b950b70538b', 'f53332caed85')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
