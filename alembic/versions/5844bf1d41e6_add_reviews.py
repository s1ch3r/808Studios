"""add reviews

Revision ID: 5844bf1d41e6
Revises: 24f1dfeb732d
Create Date: 2025-12-20 01:22:04.519559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5844bf1d41e6'
down_revision: Union[str, Sequence[str], None] = '24f1dfeb732d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('studio_id', sa.Integer(), sa.ForeignKey('studios.id'), nullable=False),
    )


def downgrade():
    op.drop_table('reviews')