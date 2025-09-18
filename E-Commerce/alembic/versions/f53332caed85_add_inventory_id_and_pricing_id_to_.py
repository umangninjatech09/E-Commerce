"""add inventory_id and pricing_id to search_index

Revision ID: f53332caed85
Revises: a861423c47ac
Create Date: 2025-09-18 12:21:40.546183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f53332caed85'
down_revision: Union[str, Sequence[str], None] = 'a861423c47ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns without foreign key constraints (SQLite safe)
    op.add_column('search_index', sa.Column('inventory_id', sa.Integer(), nullable=True))
    op.add_column('search_index', sa.Column('pricing_id', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('search_index', 'inventory_id')
    op.drop_column('search_index', 'pricing_id')
