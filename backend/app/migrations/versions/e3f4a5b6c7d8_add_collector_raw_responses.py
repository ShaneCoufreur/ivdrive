"""Add collector_raw_responses table

Revision ID: e3f4a5b6c7d8
Revises: ceb70f201aef
Create Date: 2026-03-10 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'e3f4a5b6c7d8'
down_revision: Union[str, None] = 'a2b3c4d5e6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'collector_raw_responses',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_vehicle_id', sa.UUID(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('raw_connection_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_vehicle_status', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_charging', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_driving_range', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_position', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_air_conditioning', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_maintenance', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_warning_lights', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_vehicle_id'], ['user_vehicles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_collector_raw_responses_user_vehicle_id'),
        'collector_raw_responses',
        ['user_vehicle_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_collector_raw_responses_captured_at'),
        'collector_raw_responses',
        ['captured_at'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_collector_raw_responses_captured_at'), table_name='collector_raw_responses')
    op.drop_index(op.f('ix_collector_raw_responses_user_vehicle_id'), table_name='collector_raw_responses')
    op.drop_table('collector_raw_responses')
