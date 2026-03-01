"""Expand telemetry: new tables and vehicle metadata columns.

Revision ID: 002_expand_telemetry
Revises:
Create Date: 2026-02-21
"""

from alembic import op
import sqlalchemy as sa

revision = "002_expand_telemetry"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- New columns on user_vehicles ---
    op.add_column("user_vehicles", sa.Column("image_url", sa.Text(), nullable=True))
    op.add_column("user_vehicles", sa.Column("body_type", sa.String(50), nullable=True))
    op.add_column("user_vehicles", sa.Column("trim_level", sa.String(100), nullable=True))
    op.add_column("user_vehicles", sa.Column("exterior_colour", sa.String(50), nullable=True))
    op.add_column("user_vehicles", sa.Column("battery_capacity_kwh", sa.Float(), nullable=True))
    op.add_column("user_vehicles", sa.Column("max_charging_power_kw", sa.Float(), nullable=True))
    op.add_column("user_vehicles", sa.Column("engine_power_kw", sa.Float(), nullable=True))
    op.add_column("user_vehicles", sa.Column("software_version", sa.String(100), nullable=True))

    # --- New columns on charging_states ---
    op.add_column("charging_states", sa.Column("charge_power_kw", sa.Float(), nullable=True))
    op.add_column("charging_states", sa.Column("charge_rate_km_per_hour", sa.Float(), nullable=True))
    op.add_column("charging_states", sa.Column("remaining_time_min", sa.Integer(), nullable=True))
    op.add_column("charging_states", sa.Column("target_soc_pct", sa.Integer(), nullable=True))
    op.add_column("charging_states", sa.Column("battery_pct", sa.Integer(), nullable=True))
    op.add_column("charging_states", sa.Column("remaining_range_m", sa.Integer(), nullable=True))
    op.add_column("charging_states", sa.Column("charge_type", sa.String(30), nullable=True))

    # --- New columns on vehicle_states ---
    op.add_column("vehicle_states", sa.Column("doors_locked", sa.String(30), nullable=True))
    op.add_column("vehicle_states", sa.Column("doors_open", sa.String(200), nullable=True))
    op.add_column("vehicle_states", sa.Column("windows_open", sa.String(200), nullable=True))
    op.add_column("vehicle_states", sa.Column("lights_on", sa.String(200), nullable=True))
    op.add_column("vehicle_states", sa.Column("trunk_open", sa.Boolean(), nullable=True))
    op.add_column("vehicle_states", sa.Column("bonnet_open", sa.Boolean(), nullable=True))

    # --- air_conditioning_states ---
    op.create_table(
        "air_conditioning_states",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("user_vehicle_id", sa.Uuid(), sa.ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("state", sa.String(30), nullable=True),
        sa.Column("target_temp_celsius", sa.Float(), nullable=True),
        sa.Column("outside_temp_celsius", sa.Float(), nullable=True),
        sa.Column("seat_heating_front_left", sa.Boolean(), nullable=True),
        sa.Column("seat_heating_front_right", sa.Boolean(), nullable=True),
        sa.Column("window_heating_enabled", sa.Boolean(), nullable=True),
        sa.Column("steering_wheel_position", sa.String(30), nullable=True),
        sa.UniqueConstraint("user_vehicle_id", "captured_at", name="uq_ac_states_vehicle_captured"),
    )

    # --- maintenance_reports ---
    op.create_table(
        "maintenance_reports",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("user_vehicle_id", sa.Uuid(), sa.ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mileage_in_km", sa.Integer(), nullable=True),
        sa.Column("inspection_due_in_days", sa.Integer(), nullable=True),
        sa.Column("inspection_due_in_km", sa.Integer(), nullable=True),
        sa.Column("oil_service_due_in_days", sa.Integer(), nullable=True),
        sa.Column("oil_service_due_in_km", sa.Integer(), nullable=True),
        sa.UniqueConstraint("user_vehicle_id", "captured_at", name="uq_maintenance_vehicle_captured"),
    )

    # --- odometer_readings ---
    op.create_table(
        "odometer_readings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("user_vehicle_id", sa.Uuid(), sa.ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mileage_in_km", sa.Integer(), nullable=False),
        sa.UniqueConstraint("user_vehicle_id", "captured_at", name="uq_odometer_vehicle_captured"),
    )

    # --- connection_states ---
    op.create_table(
        "connection_states",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("user_vehicle_id", sa.Uuid(), sa.ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_online", sa.Boolean(), nullable=True),
        sa.Column("in_motion", sa.Boolean(), nullable=True),
        sa.Column("ignition_on", sa.Boolean(), nullable=True),
        sa.UniqueConstraint("user_vehicle_id", "captured_at", name="uq_conn_states_vehicle_captured"),
    )


def downgrade() -> None:
    op.drop_table("connection_states")
    op.drop_table("odometer_readings")
    op.drop_table("maintenance_reports")
    op.drop_table("air_conditioning_states")

    op.drop_column("vehicle_states", "bonnet_open")
    op.drop_column("vehicle_states", "trunk_open")
    op.drop_column("vehicle_states", "lights_on")
    op.drop_column("vehicle_states", "windows_open")
    op.drop_column("vehicle_states", "doors_open")
    op.drop_column("vehicle_states", "doors_locked")

    op.drop_column("charging_states", "charge_type")
    op.drop_column("charging_states", "remaining_range_m")
    op.drop_column("charging_states", "battery_pct")
    op.drop_column("charging_states", "target_soc_pct")
    op.drop_column("charging_states", "remaining_time_min")
    op.drop_column("charging_states", "charge_rate_km_per_hour")
    op.drop_column("charging_states", "charge_power_kw")

    op.drop_column("user_vehicles", "software_version")
    op.drop_column("user_vehicles", "engine_power_kw")
    op.drop_column("user_vehicles", "max_charging_power_kw")
    op.drop_column("user_vehicles", "battery_capacity_kwh")
    op.drop_column("user_vehicles", "exterior_colour")
    op.drop_column("user_vehicles", "trim_level")
    op.drop_column("user_vehicles", "body_type")
    op.drop_column("user_vehicles", "image_url")
