# FastAPI Routes Test Plan & Results

## Systems Check
- [x] Database: Running (healthy)
- [x] Valkey: Running (healthy)
- [x] API: Running (No errors)
- [x] Web: Running
- [x] Collector: Running (Imports fixed, Alembic migrations applied, no errors)

## Routes List
/api/v1/auth/login
/api/v1/auth/logout
/api/v1/auth/me
/api/v1/auth/me/password
/api/v1/auth/refresh
/api/v1/auth/register
/api/v1/settings/geofences
/api/v1/settings/geofences/{geofence_id}
/api/v1/vehicles/
/api/v1/vehicles/{vehicle_id}
/api/v1/vehicles/{vehicle_id}/air-conditioning
/api/v1/vehicles/{vehicle_id}/analytics/battery-health
/api/v1/vehicles/{vehicle_id}/analytics/charging-costs
/api/v1/vehicles/{vehicle_id}/analytics/charging-curves
/api/v1/vehicles/{vehicle_id}/analytics/charging-sessions
/api/v1/vehicles/{vehicle_id}/analytics/charging-sessions/{session_id}
/api/v1/vehicles/{vehicle_id}/analytics/efficiency
/api/v1/vehicles/{vehicle_id}/analytics/legacy/charging-power-curve
/api/v1/vehicles/{vehicle_id}/analytics/legacy/climatization
/api/v1/vehicles/{vehicle_id}/analytics/legacy/errors
/api/v1/vehicles/{vehicle_id}/analytics/legacy/power-vs-battery-temp
/api/v1/vehicles/{vehicle_id}/analytics/power-usage
/api/v1/vehicles/{vehicle_id}/analytics/pulse
/api/v1/vehicles/{vehicle_id}/battery
/api/v1/vehicles/{vehicle_id}/charging
/api/v1/vehicles/{vehicle_id}/charging/sessions
/api/v1/vehicles/{vehicle_id}/commands/charging/start
/api/v1/vehicles/{vehicle_id}/commands/charging/stop
/api/v1/vehicles/{vehicle_id}/commands/climatization/start
/api/v1/vehicles/{vehicle_id}/commands/climatization/stop
/api/v1/vehicles/{vehicle_id}/commands/honk-flash
/api/v1/vehicles/{vehicle_id}/commands/lock
/api/v1/vehicles/{vehicle_id}/commands/unlock
/api/v1/vehicles/{vehicle_id}/commands/wake
/api/v1/vehicles/{vehicle_id}/connection-states
/api/v1/vehicles/{vehicle_id}/maintenance
/api/v1/vehicles/{vehicle_id}/odometer
/api/v1/vehicles/{vehicle_id}/overview/efficiency
/api/v1/vehicles/{vehicle_id}/overview/levels-step
/api/v1/vehicles/{vehicle_id}/overview/outside-temperature
/api/v1/vehicles/{vehicle_id}/overview/range-at-100
/api/v1/vehicles/{vehicle_id}/overview/ranges-step
/api/v1/vehicles/{vehicle_id}/overview/state-bands
/api/v1/vehicles/{vehicle_id}/overview/wltp
/api/v1/vehicles/{vehicle_id}/positions
/api/v1/vehicles/{vehicle_id}/range
/api/v1/vehicles/{vehicle_id}/statistics
/api/v1/vehicles/{vehicle_id}/status
/api/v1/vehicles/{vehicle_id}/trips
/health

## Test Results (Authenticated with Real Data)
Token payload:
```
{"id":"98003d25-18a0-42e0-a1cf-55cd3cb8a9ad","email":"m7xlab@gmail.com","display_name":"M7xLab","is_active":true,"created_at":"2026-02-22T10:05:30.771938Z"}
```

---
URL: http://localhost:8000/api/v1/auth/login
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/auth/logout
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/auth/me
Response: {"id":"98003d25-18a0-42e0-a1cf-55cd3cb8a9ad","email":"m7xlab@gmail.com","display_name":"M7xLab","is_active":true,"created_at":"2026-02-22T10:05:30.771938Z"}
---
URL: http://localhost:8000/api/v1/auth/me/password
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/auth/refresh
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/auth/register
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/settings/geofences
Response (Array [0]): null
---
URL: http://localhost:8000/api/v1/settings/geofences/{geofence_id}
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/
Response (Array [0]): {"id":"023b3fdc-40a8-457b-a3c6-d671a3b7168f","display_name":"BlackMagic","manufacturer":"Škoda","model":"Škoda Enyaq","model_year":"2024","collection_enabled":true,"collection_interval_seconds":600,"image_url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_side1080.png","body_type":"SUV","trim_level":"60 Style iV","exterior_colour":"Black Magic, helmiäisväri (1Z1Z)","battery_capacity_kwh":58.0,"max_charging_power_kw":100.0,"engine_power_kw":132.0,"software_version":"3.7","capabilities":[{"id":"AUTOMATION","statuses":[]},{"id":"BATTERY_CHARGING_CARE","statuses":[]},{"id":"BATTERY_SUPPORT","statuses":[]},{"id":"CHARGING_PROFILES","statuses":[]},{"id":"CHARGING_STATIONS","statuses":[]},{"id":"DEALER_APPOINTMENT","statuses":[]},{"id":"MAP_UPDATE","statuses":[]},{"id":"MEASUREMENTS","statuses":[]},{"id":"ONLINE_REMOTE_UPDATE","statuses":[]},{"id":"PARKING_INFORMATION","statuses":[]},{"id":"PARKING_POSITION","statuses":[]},{"id":"PLUG_AND_CHARGE","statuses":[]},{"id":"POI_SEARCH","statuses":[]},{"id":"READINESS","statuses":[]},{"id":"ROADSIDE_ASSISTANT","statuses":[]},{"id":"ROUTING","statuses":[]},{"id":"STATE","statuses":[]},{"id":"TRAFFIC_INFORMATION","statuses":[]},{"id":"VEHICLE_HEALTH_INSPECTION","statuses":[]},{"id":"WARNING_LIGHTS","statuses":[]},{"id":"AIR_CONDITIONING","statuses":[]},{"id":"AIR_CONDITIONING_SAVE_AND_ACTIVATE","statuses":[]},{"id":"AIR_CONDITIONING_SMART_SETTINGS","statuses":[]},{"id":"AIR_CONDITIONING_TIMERS","statuses":[]},{"id":"CHARGE_MODE_SELECTION","statuses":[]},{"id":"CHARGING","statuses":[]},{"id":"CHARGING_MEB","statuses":[]},{"id":"CUBIC","statuses":[]},{"id":"DESTINATIONS","statuses":[]},{"id":"DIGICERT","statuses":[]},{"id":"E_PRIVACY","statuses":[]},{"id":"EV_ROUTE_PLANNING","statuses":[]},{"id":"EV_SERVICE_BOOKING","statuses":[]},{"id":"EXTENDED_CHARGING_SETTINGS","statuses":[]},{"id":"FLEET_SUPPORTED","statuses":[]},{"id":"GUEST_USER_MANAGEMENT","statuses":[]},{"id":"LAURA_INITIAL_PROMPTS_BEV","statuses":[]},{"id":"ONLINE_SPEECH_GPS","statuses":[]},{"id":"PAY_TO_PARK","statuses":[]},{"id":"POWERPASS_TARIFFS","statuses":[]},{"id":"ROUTE_IMPORT","statuses":[]},{"id":"ROUTE_PLANNING_10_CHARGERS","statuses":[]},{"id":"SERVICE_PARTNER","statuses":[]},{"id":"SUBSCRIPTIONS","statuses":[]},{"id":"TRIP_STATISTICS_MEB","statuses":[]},{"id":"UNAVAILABILITY_STATUSES","statuses":[]},{"id":"VEHICLE_HEALTH_WARNINGS","statuses":[]},{"id":"VEHICLE_SERVICES_BACKUPS","statuses":[]},{"id":"VEHICLE_WAKE_UP_TRIGGER","statuses":[]},{"id":"WINDOW_HEATING","statuses":[]}],"specifications":{"body":"SUV","model":"Enyaq","title":"Škoda Enyaq","engine":{"type":"iV","powerInKW":132},"battery":{"capacityInKWh":58},"gearbox":{"type":"E1H"},"renders":[{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_front1080.png","viewType":"UNMODIFIED_INTERIOR_FRONT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_boot1080.png","viewType":"UNMODIFIED_INTERIOR_BOOT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_front1080.png","viewType":"UNMODIFIED_EXTERIOR_FRONT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_side1080.png","viewType":"UNMODIFIED_EXTERIOR_SIDE"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_side1080.png","viewType":"UNMODIFIED_INTERIOR_SIDE"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_rear1080.png","viewType":"UNMODIFIED_EXTERIOR_REAR"}],"modelYear":"2024","trimLevel":"60 Style iV","systemCode":"UNKNOWN","systemModelId":"5AZFF2","exteriorColour":"Black Magic, helmiäisväri (1Z1Z)","manufacturingDate":"2023-12-13","exteriorDimensions":{"widthInMm":1879,"heightInMm":1621,"lengthInMm":4649},"maxChargingPowerInKW":100},"warning_lights":[{"defects":[],"category":"ASSISTANCE"},{"defects":[],"category":"COMFORT"},{"defects":[],"category":"BRAKE"},{"defects":[],"category":"ELECTRIC_ENGINE"},{"defects":[],"category":"LIGHTING"},{"defects":[],"category":"TIRE"},{"defects":[],"category":"OTHER"}],"connector_status":"active","last_fetch_at":"2026-02-25T17:22:56.732575Z","created_at":"2026-02-22T10:43:03.497854Z"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}
Response: {"id":"023b3fdc-40a8-457b-a3c6-d671a3b7168f","display_name":"BlackMagic","manufacturer":"Škoda","model":"Škoda Enyaq","model_year":"2024","collection_enabled":true,"collection_interval_seconds":600,"image_url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_side1080.png","body_type":"SUV","trim_level":"60 Style iV","exterior_colour":"Black Magic, helmiäisväri (1Z1Z)","battery_capacity_kwh":58.0,"max_charging_power_kw":100.0,"engine_power_kw":132.0,"software_version":"3.7","capabilities":[{"id":"AUTOMATION","statuses":[]},{"id":"BATTERY_CHARGING_CARE","statuses":[]},{"id":"BATTERY_SUPPORT","statuses":[]},{"id":"CHARGING_PROFILES","statuses":[]},{"id":"CHARGING_STATIONS","statuses":[]},{"id":"DEALER_APPOINTMENT","statuses":[]},{"id":"MAP_UPDATE","statuses":[]},{"id":"MEASUREMENTS","statuses":[]},{"id":"ONLINE_REMOTE_UPDATE","statuses":[]},{"id":"PARKING_INFORMATION","statuses":[]},{"id":"PARKING_POSITION","statuses":[]},{"id":"PLUG_AND_CHARGE","statuses":[]},{"id":"POI_SEARCH","statuses":[]},{"id":"READINESS","statuses":[]},{"id":"ROADSIDE_ASSISTANT","statuses":[]},{"id":"ROUTING","statuses":[]},{"id":"STATE","statuses":[]},{"id":"TRAFFIC_INFORMATION","statuses":[]},{"id":"VEHICLE_HEALTH_INSPECTION","statuses":[]},{"id":"WARNING_LIGHTS","statuses":[]},{"id":"AIR_CONDITIONING","statuses":[]},{"id":"AIR_CONDITIONING_SAVE_AND_ACTIVATE","statuses":[]},{"id":"AIR_CONDITIONING_SMART_SETTINGS","statuses":[]},{"id":"AIR_CONDITIONING_TIMERS","statuses":[]},{"id":"CHARGE_MODE_SELECTION","statuses":[]},{"id":"CHARGING","statuses":[]},{"id":"CHARGING_MEB","statuses":[]},{"id":"CUBIC","statuses":[]},{"id":"DESTINATIONS","statuses":[]},{"id":"DIGICERT","statuses":[]},{"id":"E_PRIVACY","statuses":[]},{"id":"EV_ROUTE_PLANNING","statuses":[]},{"id":"EV_SERVICE_BOOKING","statuses":[]},{"id":"EXTENDED_CHARGING_SETTINGS","statuses":[]},{"id":"FLEET_SUPPORTED","statuses":[]},{"id":"GUEST_USER_MANAGEMENT","statuses":[]},{"id":"LAURA_INITIAL_PROMPTS_BEV","statuses":[]},{"id":"ONLINE_SPEECH_GPS","statuses":[]},{"id":"PAY_TO_PARK","statuses":[]},{"id":"POWERPASS_TARIFFS","statuses":[]},{"id":"ROUTE_IMPORT","statuses":[]},{"id":"ROUTE_PLANNING_10_CHARGERS","statuses":[]},{"id":"SERVICE_PARTNER","statuses":[]},{"id":"SUBSCRIPTIONS","statuses":[]},{"id":"TRIP_STATISTICS_MEB","statuses":[]},{"id":"UNAVAILABILITY_STATUSES","statuses":[]},{"id":"VEHICLE_HEALTH_WARNINGS","statuses":[]},{"id":"VEHICLE_SERVICES_BACKUPS","statuses":[]},{"id":"VEHICLE_WAKE_UP_TRIGGER","statuses":[]},{"id":"WINDOW_HEATING","statuses":[]}],"specifications":{"body":"SUV","model":"Enyaq","title":"Škoda Enyaq","engine":{"type":"iV","powerInKW":132},"battery":{"capacityInKWh":58},"gearbox":{"type":"E1H"},"renders":[{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_front1080.png","viewType":"UNMODIFIED_INTERIOR_FRONT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_boot1080.png","viewType":"UNMODIFIED_INTERIOR_BOOT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_front1080.png","viewType":"UNMODIFIED_EXTERIOR_FRONT"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_side1080.png","viewType":"UNMODIFIED_EXTERIOR_SIDE"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZYKo.GaJUjNA-q3hQv0XtUlgSZ8kb_1A-ctsPR4WEH.nZKNBjokX-Hb4seB.0g6zolGNXftEvPSiR8na_-EIGD-19201080studiovint_side1080.png","viewType":"UNMODIFIED_INTERIOR_SIDE"},{"url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_rear1080.png","viewType":"UNMODIFIED_EXTERIOR_REAR"}],"modelYear":"2024","trimLevel":"60 Style iV","systemCode":"UNKNOWN","systemModelId":"5AZFF2","exteriorColour":"Black Magic, helmiäisväri (1Z1Z)","manufacturingDate":"2023-12-13","exteriorDimensions":{"widthInMm":1879,"heightInMm":1621,"lengthInMm":4649},"maxChargingPowerInKW":100},"warning_lights":[{"defects":[],"category":"ASSISTANCE"},{"defects":[],"category":"COMFORT"},{"defects":[],"category":"BRAKE"},{"defects":[],"category":"ELECTRIC_ENGINE"},{"defects":[],"category":"LIGHTING"},{"defects":[],"category":"TIRE"},{"defects":[],"category":"OTHER"}],"connector_status":"active","last_fetch_at":"2026-02-25T17:22:56.732575Z","created_at":"2026-02-22T10:43:03.497854Z"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/air-conditioning
Response (Array [0]): {"captured_at":"2026-02-25T17:22:56.732575Z","state":"OFF","target_temp_celsius":17.5,"outside_temp_celsius":null,"seat_heating_front_left":false,"seat_heating_front_right":false,"window_heating_enabled":false}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/battery-health
Response (Array [0]): null
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/charging-costs
Response: {"total_sessions":2,"total_kwh_added":40.27,"total_base_cost_eur":5.83,"total_actual_cost_eur":9.55,"markup_paid_eur":3.72}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/charging-curves
Response (Array [0]): null
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/charging-sessions
Response (Array [0]): {"id":3,"session_start":"2026-02-25T05:53:32.057269+00:00","session_end":"2026-02-25T06:30:42.560124+00:00","start_level":31.0,"end_level":80.0,"energy_kwh":29.83,"base_cost_eur":4.26,"actual_cost_eur":9.55,"provider_name":"IgnitisON","avg_temp_celsius":-1.6}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/charging-sessions/{session_id}
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/efficiency
Response (Array [0]): {"temperature_celsius":-3,"consumption_kwh_100km":32.5,"trips_recorded":2}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/legacy/charging-power-curve
Response: Internal Server Error
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/legacy/climatization
Response: Internal Server Error
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/legacy/errors
Response: Internal Server Error
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/legacy/power-vs-battery-temp
Response: Internal Server Error
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/power-usage
Response (Array [0]): null
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/analytics/pulse
Response: {"status":"PARKED","battery_pct":74,"remaining_range_km":195,"temperature_celsius":-1.2,"weather_code":"3","is_online":true,"charging_power_kw":0.0,"remaining_charge_time_min":0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/battery
Response (Array [0]): {"timestamp":"2026-02-25T17:22:56.732575Z","level":74.0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/charging
Response (Array [0]): {"first_date":"2026-02-25T17:22:56.732575Z","last_date":"2026-02-25T17:22:56.732575Z","state":"CONNECT_CABLE","charge_power_kw":0.0,"charge_rate_km_per_hour":null,"remaining_time_min":0,"target_soc_pct":80,"battery_pct":74,"remaining_range_m":195000,"charge_type":null}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/charging/sessions
Response (Array [0]): {"id":3,"session_start":"2026-02-25T05:53:32.057269Z","session_end":"2026-02-25T06:30:42.560124Z","start_level":31.0,"end_level":80.0,"charging_type":null,"energy_kwh":29.83,"latitude":54.698145,"longitude":25.265652}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/charging/start
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/charging/stop
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/climatization/start
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/climatization/stop
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/honk-flash
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/lock
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/unlock
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/commands/wake
Response: {"detail":"Method Not Allowed"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/connection-states
Response (Array [0]): {"captured_at":"2026-02-25T17:22:56.732575Z","is_online":true,"in_motion":false,"ignition_on":false}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/maintenance
Response (Array [0]): {"captured_at":"2026-02-25T17:22:56.732575Z","mileage_in_km":35824,"inspection_due_in_days":-38,"inspection_due_in_km":null,"oil_service_due_in_days":null,"oil_service_due_in_km":null}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/odometer
Response (Array [0]): {"captured_at":"2026-02-25T17:22:56.732575Z","mileage_in_km":35824}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/efficiency
Response (Array [0]): {"time":"2026-02-19T15:38:56Z","efficiency_pct":64.44838697997756}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/levels-step
Response (Array [0]): {"timestamp":"2026-02-19T15:38:56Z","level":71.0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/outside-temperature
Response (Array [0]): null
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/range-at-100
Response (Array [0]): {"time":"2026-02-19T15:38:56Z","range_estimated_full":250.7042253521127}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/ranges-step
Response (Array [0]): {"timestamp":"2026-02-19T15:38:56Z","range_km":178.0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/state-bands
Response (Array [0]): {"from_date":"2026-02-11T17:07:31.158632Z","to_date":"2026-02-15T13:09:14.636934Z","state":"online"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/overview/wltp
Response: {"wltp_range_km":389.0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/positions
Response (Array [0]): {"captured_at":"2026-02-25T17:22:56.732575Z","latitude":54.648228,"longitude":25.257917}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/range
Response (Array [0]): {"timestamp":"2026-02-25T17:22:56.732575Z","range_km":195.0}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/statistics
Response (Array [0]): {"period":"2026-02-25T00:00:00+00:00","drives_count":4,"total_distance_km":240.0,"time_driven_seconds":4005.247063,"median_distance_km":58.0,"charging_sessions_count":2,"total_energy_kwh":40.269999999999996,"avg_energy_per_session_kwh":20.13,"time_charging_seconds":2365.082141}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/status
Response: {"vin_last4":"2145","display_name":"BlackMagic","manufacturer":"Škoda","model":"Škoda Enyaq","model_year":"2024","image_url":"https://iprenders.blob.core.windows.net/base5azv24100009/1Z1ZZK.FeJU0jNB-q3hQv0XuaTmgSZ8j.2C-etsPR6WDG.mZKNBjqlY-Hb3qdB2h6zokGNXftEvOSjR8nZ_-EJAHD-19201080dayvext_side1080.png","battery_capacity_kwh":58.0,"latest_battery_level":74.0,"latest_range_km":195.0,"latest_charging_state":"CONNECT_CABLE","latest_vehicle_state":"YES","latest_position":{"latitude":54.648228,"longitude":25.257917},"last_updated":"2026-02-25T17:22:56.732575Z","charging_power_kw":0.0,"remaining_charge_time_min":0,"target_soc":80,"charge_type":null,"doors_locked":"YES","doors_open":null,"windows_open":null,"lights_on":null,"trunk_open":null,"bonnet_open":null,"climate_state":"OFF","target_temp":17.5,"outside_temp":null,"odometer_km":35824,"inspection_due_days":-38,"is_online":true,"is_in_motion":false,"connector_status":"active"}
---
URL: http://localhost:8000/api/v1/vehicles/{vehicle_id}/trips
Response (Array [0]): {"id":36,"start_date":"2026-02-25T17:01:12.018591Z","end_date":"2026-02-25T17:23:03.515835Z","start_lat":54.648236,"start_lon":25.257927,"end_lat":54.648228,"end_lon":25.257917,"start_odometer":35758.0,"end_odometer":35824.0}
---
URL: http://localhost:8000/health
Response: {"status":"ok"}

## Completed (2026-02-28)
- Phase 1: Homepage Split, Scaffold /statistics route, Refactor StatisticsShell
- Phase 2: Add Edit Modal, Wire PATCH endpoint
- Phase 3: Move BI Components, Global Date Picker, Visited Interactive Map
