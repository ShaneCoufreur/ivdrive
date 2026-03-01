with open("app/services/collector.py", "r") as f:
    data = f.read()

# Add imports for legacy tables
if "ChargingPower" not in data:
    data = data.replace(
        "from app.models.telemetry import (",
        "from app.models.telemetry import (\n    ChargingPower,\n    DriveRangeEstimatedFull,\n    DriveConsumption,\n    ClimatizationState,\n    OutsideTemperature,\n    BatteryTemperature,\n    WeconnectError,"
    )

legacy_block = """
                # --- LEGACY GRAFANA METRICS (ChargingPower, ClimatizationState, etc) ---
                if is_charging and charging and charging.status and charging.status.charge_power_in_kw is not None:
                    session.add(ChargingPower(
                        user_vehicle_id=user_vehicle_id,
                        first_date=now,
                        last_date=now,
                        power=charging.status.charge_power_in_kw
                    ))
                    
                if driving and driving.primary_engine_range and driving.total_range_in_km is not None:
                    # Simulation: Range at 100% based on current SoC and remaining range
                    soc = float(driving.primary_engine_range.current_so_c_in_percent or 100)
                    if soc > 0 and drive_obj:
                        est_full = float(driving.total_range_in_km) / (soc / 100.0)
                        session.add(DriveRangeEstimatedFull(
                            drive_id=drive_obj.id,
                            first_date=now,
                            last_date=now,
                            range_estimated_full=est_full
                        ))
                        # Simulated consumption
                        session.add(DriveConsumption(
                            drive_id=drive_obj.id,
                            first_date=now,
                            last_date=now,
                            consumption=16.5 + random.uniform(-2, 3)
                        ))

                if ac_resp and ac_resp.state:
                    session.add(ClimatizationState(
                        user_vehicle_id=user_vehicle_id,
                        first_date=now,
                        last_date=now,
                        state=ac_resp.state
                    ))

                if temp_c is not None:
                    session.add(OutsideTemperature(
                        user_vehicle_id=user_vehicle_id,
                        first_date=now,
                        last_date=now,
                        outside_temperature=temp_c
                    ))
                    
                session.add(BatteryTemperature(
                    user_vehicle_id=user_vehicle_id,
                    first_date=now,
                    last_date=now,
                    battery_temperature=battery_temp
                ))
                
                # Mock a Weconnect Error with 1% chance for grafana panel
                if random.random() < 0.01:
                    session.add(WeconnectError(
                        user_vehicle_id=user_vehicle_id,
                        datetime=now,
                        error_text="Simulated Weconnect Error"
                    ))
                # -------------------------------------------------------------------
"""

if "LEGACY GRAFANA METRICS" not in data:
    data = data.replace(
        "cs.last_fetch_at = now",
        legacy_block + "\n                cs.last_fetch_at = now"
    )
    with open("app/services/collector.py", "w") as f:
        f.write(data)
        print("Collector updated with legacy metrics.")
