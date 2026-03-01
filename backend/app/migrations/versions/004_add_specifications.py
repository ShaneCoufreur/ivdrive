"""add specifications

Revision ID: 004_add_specifications
Revises: 003_add_capabilities
Create Date: 2026-02-22 13:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_add_specifications'
down_revision = '003_add_capabilities'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('user_vehicles', sa.Column('specifications', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

def downgrade() -> None:
    op.drop_column('user_vehicles', 'specifications')
