"""
Verify that all API-derived data is stored in the DB as per docs:
- api_to_database_verification.md
- data_gaps_and_carconnectivity_mapping.md

Runs SELECT ... LIMIT 1 on each telemetry table and asserts that:
1. The table has all expected columns (from the verification doc).
2. When a row exists, its keys include those columns.

Run from backend/ (config loads .env from backend/ or ../.env). DB tests need database_url and valkey_url (or POSTGRES_* and VALKEY_PASSWORD in .env).

  cd backend
  pytest tests/_test_database_vs_api.py -v
  PRINT_SAMPLE_ROWS=1 pytest tests/_test_database_vs_api.py -v -s
"""

from __future__ import annotations

import asyncio
import os
import pytest
from sqlalchemy import select, text

from app.models.telemetry import (
    AirConditioningState,
    ChargingState,
    ConnectionState,
    Drive,
    DriveLevel,
    DriveRange,
    MaintenanceReport,
    OdometerReading,
    VehiclePosition,
    VehicleState,
)
from app.models.vehicle import UserVehicle


# Expected columns per table (from api_to_database_verification.md).
# Only columns that come from API responses; id/user_vehicle_id/drive_id/first_date/last_date/captured_at are included where relevant.
EXPECTED_COLUMNS_BY_TABLE: dict[str, set[str]] = {
    "charging_states": {
        "state",
        "charge_type",
        "charge_power_kw",
        "remaining_time_min",
        "charge_rate_km_per_hour",
        "battery_pct",
        "remaining_range_m",
        "target_soc_pct",
        "first_date",
        "last_date",
    },
    "drive_levels": {
        "level",
        "first_date",
        "last_date",
        "drive_id",
    },
    "drive_ranges": {
        "range_km",
        "first_date",
        "last_date",
        "drive_id",
    },
    "drives": {
        "type",
        "drive_id",
        "user_vehicle_id",
    },
    "vehicle_states": {
        "state",
        "doors_locked",
        "doors_open",
        "windows_open",
        "lights_on",
        "first_date",
        "last_date",
    },
    "air_conditioning_states": {
        "state",
        "target_temp_celsius",
        "outside_temp_celsius",
        "window_heating_enabled",
        "steering_wheel_position",
        "seat_heating_front_left",
        "seat_heating_front_right",
        "captured_at",
    },
    "connection_states": {
        "is_online",
        "in_motion",
        "ignition_on",
        "captured_at",
    },
    "vehicle_positions": {
        "latitude",
        "longitude",
        "captured_at",
    },
    "maintenance_reports": {
        "mileage_in_km",
        "inspection_due_in_days",
        "inspection_due_in_km",
        "oil_service_due_in_days",
        "oil_service_due_in_km",
        "captured_at",
    },
    "odometer_readings": {
        "mileage_in_km",
        "captured_at",
    },
    "user_vehicles": {
        "display_name",
        "model",
        "model_year",
        "body_type",
        "battery_capacity_kwh",
        "engine_power_kw",
        "max_charging_power_kw",
        "image_url",
        "specifications",
        "warning_lights",
    },
}

TABLE_MODELS = {
    "charging_states": ChargingState,
    "drive_levels": DriveLevel,
    "drive_ranges": DriveRange,
    "drives": Drive,
    "vehicle_states": VehicleState,
    "air_conditioning_states": AirConditioningState,
    "connection_states": ConnectionState,
    "vehicle_positions": VehiclePosition,
    "maintenance_reports": MaintenanceReport,
    "odometer_readings": OdometerReading,
    "user_vehicles": UserVehicle,
}


def _table_columns(model_class) -> set[str]:
    return {c.key for c in model_class.__table__.columns}


def test_all_tables_have_expected_columns_from_verification_doc():
    """Every table listed in api_to_database_verification.md has at least the expected columns."""
    for table_name, expected in EXPECTED_COLUMNS_BY_TABLE.items():
        model = TABLE_MODELS[table_name]
        actual = _table_columns(model)
        missing = expected - actual
        assert not missing, (
            f"Table {table_name}: missing columns {missing}. "
            "Update api_to_database_verification.md or add migration."
        )


async def _run_all_db_checks():
    """Single async entry so we use one event loop and avoid 'attached to a different loop'."""
    from app.database import async_session

    async with async_session() as session:
        # 1. At least one vehicle and one telemetry table has data
        result = await session.execute(
            text("SELECT COUNT(*) AS n FROM user_vehicles")
        )
        n_vehicles = result.scalar() or 0
        if n_vehicles == 0:
            pytest.skip("No user_vehicles in DB (run app and add a vehicle first)")

        tables_to_check = [
            "charging_states",
            "drive_levels",
            "drive_ranges",
            "vehicle_states",
            "air_conditioning_states",
            "connection_states",
            "vehicle_positions",
            "maintenance_reports",
            "odometer_readings",
        ]
        any_has_data = False
        for table_name in tables_to_check:
            res = await session.execute(
                text(f"SELECT 1 FROM {table_name} LIMIT 1")
            )
            if res.scalar() is not None:
                any_has_data = True
                break
        assert any_has_data, (
            "No telemetry rows found in any of: " + ", ".join(tables_to_check) + ". "
            "Run the collector and retry."
        )

        # 2. SELECT LIMIT 1 from each table; when a row exists, assert expected columns present.
        # Use table columns explicitly so result.mappings() has column-name keys.
        for table_name, expected_cols in EXPECTED_COLUMNS_BY_TABLE.items():
            model = TABLE_MODELS[table_name]
            stmt = select(*model.__table__.c).limit(1)
            result = await session.execute(stmt)
            row = result.mappings().first()
            if row is None:
                continue
            row_keys = set(row.keys())
            missing = expected_cols - row_keys
            assert not missing, (
                f"Table {table_name}: sample row missing keys {missing}. "
                "Expected from api_to_database_verification.md."
            )
            if os.environ.get("PRINT_SAMPLE_ROWS"):
                print(f"\n--- {table_name} (limit 1) ---")
                for k, v in dict(row).items():
                    print(f"  {k}: {v}")


def test_database_has_expected_columns_and_telemetry():
    """
    Single DB test (one asyncio.run) to avoid event-loop conflicts.
    Asserts: (1) at least one user_vehicle and one telemetry table has data;
    (2) for each table with a row, that row has all expected columns.
    Set PRINT_SAMPLE_ROWS=1 to print each sample row.
    """
    asyncio.run(_run_all_db_checks())
