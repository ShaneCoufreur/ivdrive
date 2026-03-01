import re

with open("app/api/v1/analytics.py", "r") as f:
    data = f.read()

# Add imports for legacy tables
if "ChargingPower" not in data:
    data = data.replace(
        "from app.models.telemetry import Trip, ChargingSession, VehiclePosition, ChargingState, ConnectionState, BatteryHealth, PowerUsage, ChargingCurve",
        "from app.models.telemetry import Trip, ChargingSession, VehiclePosition, ChargingState, ConnectionState, BatteryHealth, PowerUsage, ChargingCurve, ChargingPower, DriveRangeEstimatedFull, DriveConsumption, ClimatizationState, OutsideTemperature, BatteryTemperature, WeconnectError"
    )

legacy_endpoints = """
@router.get("/{vehicle_id}/analytics/legacy/charging-power-curve")
async def get_legacy_charging_power_curve(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 500
):
    \"\"\"Query 41 & 51: Real-time charging power curve.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(ChargingPower)
        .where(ChargingPower.user_vehicle_id == vehicle_id)
        .order_by(ChargingPower.first_date.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "time": r.first_date.isoformat(),
            "power": r.power
        }
        for r in records
    ]

@router.get("/{vehicle_id}/analytics/legacy/power-vs-battery-temp")
async def get_legacy_power_vs_battery_temp(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    \"\"\"Query 29: Charging power Min/Avg/Max grouped by Battery Temperature.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    # We'll map it natively through a raw query-like aggregation
    stmt = (
        select(
            func.round(BatteryTemperature.battery_temperature).label("temp"),
            func.min(ChargingPower.power).label("min_p"),
            func.avg(ChargingPower.power).label("avg_p"),
            func.max(ChargingPower.power).label("max_p")
        )
        .join(ChargingPower, ChargingPower.user_vehicle_id == BatteryTemperature.user_vehicle_id)
        .where(BatteryTemperature.user_vehicle_id == vehicle_id)
        .where(BatteryTemperature.first_date == ChargingPower.first_date) # Approximation for overlapping time
        .group_by("temp")
        .order_by("temp")
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    return [
        {
            "battery_temperature": int(row.temp) if row.temp is not None else 0,
            "min_power": round(float(row.min_p), 2) if row.min_p else 0,
            "avg_power": round(float(row.avg_p), 2) if row.avg_p else 0,
            "max_power": round(float(row.max_p), 2) if row.max_p else 0,
        }
        for row in rows
    ]

@router.get("/{vehicle_id}/analytics/legacy/errors")
async def get_legacy_weconnect_errors(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    \"\"\"Query 48: Connection Errors over time.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(WeconnectError)
        .where(WeconnectError.user_vehicle_id == vehicle_id)
        .order_by(WeconnectError.datetime.desc())
        .limit(100)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "datetime": r.datetime.isoformat(),
            "error_text": r.error_text
        }
        for r in records
    ]
    
@router.get("/{vehicle_id}/analytics/legacy/climatization")
async def get_legacy_climatization(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    \"\"\"Query 58: Climatization states over time.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(ClimatizationState)
        .where(ClimatizationState.user_vehicle_id == vehicle_id)
        .order_by(ClimatizationState.first_date.desc())
        .limit(100)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "time": r.first_date.isoformat(),
            "state": r.state
        }
        for r in records
    ]
"""

if "@router.get(\"/{vehicle_id}/analytics/legacy/charging-power-curve\")" not in data:
    with open("app/api/v1/analytics.py", "a") as f:
        f.write("\n" + legacy_endpoints)
        print("Analytics endpoints updated with legacy queries.")
