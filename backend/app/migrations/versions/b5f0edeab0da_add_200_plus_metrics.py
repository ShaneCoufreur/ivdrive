"""add 200 plus metrics

Revision ID: b5f0edeab0da
Revises: d6654a36dab7
Create Date: 2026-02-25 06:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b5f0edeab0da'
down_revision: Union[str, None] = 'd6654a36dab7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # BatteryHealth
    op.create_table('battery_health',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_vehicle_id', sa.UUID(), nullable=False),
    sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('twelve_v_battery_voltage', sa.Float(), nullable=True),
    sa.Column('twelve_v_battery_soc', sa.Float(), nullable=True),
    sa.Column('twelve_v_battery_soh', sa.Float(), nullable=True),
    sa.Column('hv_battery_voltage', sa.Float(), nullable=True),
    sa.Column('hv_battery_current', sa.Float(), nullable=True),
    sa.Column('hv_battery_temperature', sa.Float(), nullable=True),
    sa.Column('hv_battery_soh', sa.Float(), nullable=True),
    sa.Column('hv_battery_degradation_pct', sa.Float(), nullable=True),
    sa.Column('cell_voltage_min', sa.Float(), nullable=True),
    sa.Column('cell_voltage_max', sa.Float(), nullable=True),
    sa.Column('cell_voltage_avg', sa.Float(), nullable=True),
    sa.Column('cell_temperature_min', sa.Float(), nullable=True),
    sa.Column('cell_temperature_max', sa.Float(), nullable=True),
    sa.Column('cell_temperature_avg', sa.Float(), nullable=True),
    sa.Column('imbalance_mv', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_vehicle_id'], ['user_vehicles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_vehicle_id', 'captured_at', name='uq_battery_health_vehicle_captured')
    )
    op.create_index(op.f('ix_battery_health_user_vehicle_id'), 'battery_health', ['user_vehicle_id'], unique=False)

    # PowerUsage
    op.create_table('power_usage',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_vehicle_id', sa.UUID(), nullable=False),
    sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('total_power_kw', sa.Float(), nullable=True),
    sa.Column('motor_power_kw', sa.Float(), nullable=True),
    sa.Column('hvac_power_kw', sa.Float(), nullable=True),
    sa.Column('auxiliary_power_kw', sa.Float(), nullable=True),
    sa.Column('battery_heater_power_kw', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_vehicle_id'], ['user_vehicles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_vehicle_id', 'captured_at', name='uq_power_usage_vehicle_captured')
    )
    op.create_index(op.f('ix_power_usage_user_vehicle_id'), 'power_usage', ['user_vehicle_id'], unique=False)

    # ChargingCurve
    op.create_table('charging_curves',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_vehicle_id', sa.UUID(), nullable=False),
    sa.Column('session_id', sa.BigInteger(), nullable=True),
    sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('soc_pct', sa.Float(), nullable=True),
    sa.Column('power_kw', sa.Float(), nullable=True),
    sa.Column('voltage_v', sa.Float(), nullable=True),
    sa.Column('current_a', sa.Float(), nullable=True),
    sa.Column('battery_temp_celsius', sa.Float(), nullable=True),
    sa.Column('charger_temp_celsius', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['charging_sessions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_vehicle_id'], ['user_vehicles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_vehicle_id', 'captured_at', name='uq_charging_curves_vehicle_captured')
    )
    op.create_index(op.f('ix_charging_curves_user_vehicle_id'), 'charging_curves', ['user_vehicle_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_charging_curves_user_vehicle_id'), table_name='charging_curves')
    op.drop_table('charging_curves')
    op.drop_index(op.f('ix_power_usage_user_vehicle_id'), table_name='power_usage')
    op.drop_table('power_usage')
    op.drop_index(op.f('ix_battery_health_user_vehicle_id'), table_name='battery_health')
    op.drop_table('battery_health')
