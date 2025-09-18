"""add customer_id to search_index

Revision ID: a861423c47ac
Revises: 1c7daed4e496
Create Date: 2025-09-18 12:12:05.151790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a861423c47ac'
down_revision: Union[str, Sequence[str], None] = '1c7daed4e496'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('search_index', sa.Column('customer_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('search_index', 'customer_id')

