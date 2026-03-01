"""add warning_lights

Revision ID: 005_add_warning_lights
Revises: 004_add_specifications
Create Date: 2026-02-22 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '005_add_warning_lights'
down_revision: Union[str, None] = '004_add_specifications'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('user_vehicles', sa.Column('warning_lights', JSONB(), nullable=True))

def downgrade() -> None:
    op.drop_column('user_vehicles', 'warning_lights')
