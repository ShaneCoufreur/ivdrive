"""Add advanced auth lifecycle

Revision ID: 1924fb48a5b1
Revises: c4d5e6f7a8b9
Create Date: 2026-07-08 16:49:04.591457
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '1924fb48a5b1'
down_revision: Union[str, None] = 'c4d5e6f7a8b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('connector_auth_events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('session_id', sa.Uuid(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['connector_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.add_column('connector_sessions', sa.Column('refresh_token_expires_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('connector_sessions', sa.Column('last_auth_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('connector_sessions', sa.Column('last_auth_method', sa.String(length=50), nullable=True))
    op.add_column('connector_sessions', sa.Column('last_auth_error', sa.String(length=255), nullable=True))
    op.add_column('connector_sessions', sa.Column('needs_user_reauth_reason', sa.String(length=255), nullable=True))
    op.add_column('connector_sessions', sa.Column('secure_mode', sa.Boolean(), server_default='true', nullable=False))
    op.add_column('connector_sessions', sa.Column('backoff_until', sa.DateTime(timezone=True), nullable=True))
    op.add_column('connector_sessions', sa.Column('consecutive_auth_failures', sa.Integer(), server_default='0', nullable=False))

def downgrade() -> None:
    op.drop_column('connector_sessions', 'consecutive_auth_failures')
    op.drop_column('connector_sessions', 'backoff_until')
    op.drop_column('connector_sessions', 'secure_mode')
    op.drop_column('connector_sessions', 'needs_user_reauth_reason')
    op.drop_column('connector_sessions', 'last_auth_error')
    op.drop_column('connector_sessions', 'last_auth_method')
    op.drop_column('connector_sessions', 'last_auth_at')
    op.drop_column('connector_sessions', 'refresh_token_expires_at')
    
    op.drop_table('connector_auth_events')