"""add working hours for studios

Revision ID: 24f1dfeb732d
Revises: d860c902e90f
Create Date: 2025-12-19 22:54:11.141881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import time


# revision identifiers, used by Alembic.
revision: str = '24f1dfeb732d'
down_revision: Union[str, Sequence[str], None] = 'd860c902e90f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'studios',
        sa.Column('work_start', sa.Time(), nullable=True)
    )
    op.add_column(
        'studios',
        sa.Column('work_end', sa.Time(), nullable=True)
    )

    # проставляем значения для существующих студий
    op.execute(
        "UPDATE studios SET work_start = '10:00', work_end = '22:00'"
    )

    # теперь делаем NOT NULL
    op.alter_column('studios', 'work_start', nullable=False)
    op.alter_column('studios', 'work_end', nullable=False)


def downgrade():
    op.drop_column('studios', 'work_end')
    op.drop_column('studios', 'work_start')
