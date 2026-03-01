import re

with open("app/api/v1/analytics.py", "r") as f:
    data = f.read()

# Add imports for the new models
if "BatteryHealth" not in data:
    data = data.replace(
        "from app.models.telemetry import Trip, ChargingSession, VehiclePosition, ChargingState, ConnectionState",
        "from app.models.telemetry import Trip, ChargingSession, VehiclePosition, ChargingState, ConnectionState, BatteryHealth, PowerUsage, ChargingCurve"
    )

new_endpoints = """
@router.get("/{vehicle_id}/analytics/battery-health")
async def get_battery_health(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 100
):
    \"\"\"Return the latest battery health metrics including 12V and cell voltages.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(BatteryHealth)
        .where(BatteryHealth.user_vehicle_id == vehicle_id)
        .order_by(BatteryHealth.captured_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "captured_at": r.captured_at.isoformat(),
            "twelve_v_battery_voltage": r.twelve_v_battery_voltage,
            "twelve_v_battery_soc": r.twelve_v_battery_soc,
            "twelve_v_battery_soh": r.twelve_v_battery_soh,
            "hv_battery_voltage": r.hv_battery_voltage,
            "hv_battery_current": r.hv_battery_current,
            "hv_battery_temperature": r.hv_battery_temperature,
            "hv_battery_soh": r.hv_battery_soh,
            "hv_battery_degradation_pct": r.hv_battery_degradation_pct,
            "cell_voltage_min": r.cell_voltage_min,
            "cell_voltage_max": r.cell_voltage_max,
            "cell_voltage_avg": r.cell_voltage_avg,
            "cell_temperature_avg": r.cell_temperature_avg,
            "imbalance_mv": r.imbalance_mv,
        }
        for r in records
    ]

@router.get("/{vehicle_id}/analytics/power-usage")
async def get_power_usage(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 100
):
    \"\"\"Return detailed power consumption breakdown over time.\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(PowerUsage)
        .where(PowerUsage.user_vehicle_id == vehicle_id)
        .order_by(PowerUsage.captured_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "captured_at": r.captured_at.isoformat(),
            "total_power_kw": r.total_power_kw,
            "motor_power_kw": r.motor_power_kw,
            "hvac_power_kw": r.hvac_power_kw,
            "auxiliary_power_kw": r.auxiliary_power_kw,
            "battery_heater_power_kw": r.battery_heater_power_kw,
        }
        for r in records
    ]

@router.get("/{vehicle_id}/analytics/charging-curves")
async def get_charging_curves(
    vehicle_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 100
):
    \"\"\"Return charging curve points (power/voltage vs SoC).\"\"\"
    await get_user_vehicle(user.id, vehicle_id, db)
    
    stmt = (
        select(ChargingCurve)
        .where(ChargingCurve.user_vehicle_id == vehicle_id)
        .order_by(ChargingCurve.captured_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "captured_at": r.captured_at.isoformat(),
            "soc_pct": r.soc_pct,
            "power_kw": r.power_kw,
            "voltage_v": r.voltage_v,
            "current_a": r.current_a,
            "battery_temp_celsius": r.battery_temp_celsius,
            "charger_temp_celsius": r.charger_temp_celsius,
        }
        for r in records
    ]
"""

if "@router.get(\"/{vehicle_id}/analytics/battery-health\")" not in data:
    with open("app/api/v1/analytics.py", "a") as f:
        f.write("\n" + new_endpoints)
        print("Analytics endpoints updated.")
