"""add capabilities

Revision ID: 003_add_capabilities
Revises: 002_expand_telemetry
Create Date: 2026-02-22 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_add_capabilities'
down_revision = '002_expand_telemetry'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('user_vehicles', sa.Column('capabilities', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

def downgrade() -> None:
    op.drop_column('user_vehicles', 'capabilities')
