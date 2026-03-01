from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


def _to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


_CAMEL_CFG = ConfigDict(populate_by_name=True, alias_generator=_to_camel)


class GarageVehicleSpec(BaseModel):
    model_config = _CAMEL_CFG
    title: str | None = None
    model: str | None = None
    model_year: str | None = None
    body: str | None = None
    system_model_id: str | None = None


class GarageVehicle(BaseModel):
    model_config = _CAMEL_CFG
    vin: str
    name: str | None = None
    specification: GarageVehicleSpec | None = None
    license_plate: str | None = None


class GarageResponse(BaseModel):
    model_config = _CAMEL_CFG
    vehicles: list[GarageVehicle] = Field(default_factory=list)


class ChargingBattery(BaseModel):
    model_config = _CAMEL_CFG
    remaining_cruising_range_in_meters: int | None = None
    state_of_charge_in_percent: int | None = None


class ChargingStatus(BaseModel):
    model_config = _CAMEL_CFG
    state: str | None = None
    charge_type: str | None = None
    charge_power_in_kw: float | None = None
    remaining_time_to_fully_charged_in_minutes: int | None = None
    charge_rate_in_kilometers_per_hour: float | None = None
    battery: ChargingBattery | None = None


class ChargingSettings(BaseModel):
    model_config = _CAMEL_CFG
    max_charge_current_ac: str | None = None
    auto_unlock_plug_when_charged: str | None = None
    target_state_of_charge_in_percent: int | None = None


class ChargingError(BaseModel):
    model_config = _CAMEL_CFG
    type: str | None = None
    description: str | None = None


class ChargingResponse(BaseModel):
    model_config = _CAMEL_CFG
    status: ChargingStatus | None = None
    settings: ChargingSettings | None = None
    errors: list[ChargingError] = Field(default_factory=list)
    is_vehicle_in_saved_location: bool | None = None


class EngineRange(BaseModel):
    model_config = _CAMEL_CFG
    engine_type: str | None = None
    current_so_c_in_percent: int | None = Field(default=None, alias="currentSoCInPercent")
    remaining_range_in_km: int | None = None
    current_fuel_level_in_percent: int | None = None


class DrivingRangeResponse(BaseModel):
    model_config = _CAMEL_CFG
    car_type: str | None = None
    total_range_in_km: int | None = None
    car_captured_timestamp: str | None = None
    primary_engine_range: EngineRange | None = None
    secondary_engine_range: EngineRange | None = None


class DoorState(BaseModel):
    model_config = _CAMEL_CFG
    name: str | None = None
    status: list[str] = Field(default_factory=list)


class WindowState(BaseModel):
    model_config = _CAMEL_CFG
    name: str | None = None
    status: list[str] = Field(default_factory=list)


class LightState(BaseModel):
    model_config = _CAMEL_CFG
    name: str | None = None
    status: str | None = None


class VehicleStatusOverall(BaseModel):
    model_config = _CAMEL_CFG
    doors_locked: str | None = None
    locked: str | None = None
    doors: list[DoorState] | str | None = None
    windows: list[WindowState] | str | None = None
    lights: list[LightState] | str | None = None


class VehicleStatusResponse(BaseModel):
    model_config = _CAMEL_CFG
    car_captured_timestamp: str | None = None
    overall: VehicleStatusOverall | None = None


class TemperatureValue(BaseModel):
    """API may send temperatureValue + unitInCar instead of celsius/fahrenheit."""
    model_config = _CAMEL_CFG
    celsius: float | None = Field(None, alias="temperatureValue")
    fahrenheit: float | None = None


class SeatHeating(BaseModel):
    model_config = _CAMEL_CFG
    front_left: bool | None = None
    front_right: bool | None = None


class AirConditioningResponse(BaseModel):
    model_config = _CAMEL_CFG
    state: str | None = None
    target_temperature: TemperatureValue | None = None
    outside_temperature: TemperatureValue | None = None
    window_heating_enabled: bool | None = None
    seat_heating_activated: SeatHeating | None = None
    steering_wheel_position: str | None = None
    car_captured_timestamp: str | None = None


class GpsCoordinates(BaseModel):
    model_config = _CAMEL_CFG
    latitude: float
    longitude: float


class Position(BaseModel):
    model_config = _CAMEL_CFG
    type: str | None = None
    gps_coordinates: GpsCoordinates | None = Field(default=None, alias="gpsCoordinates")


class PositionResponse(BaseModel):
    model_config = _CAMEL_CFG
    positions: list[Position] = Field(default_factory=list)


class MaintenanceResponse(BaseModel):
    model_config = _CAMEL_CFG
    mileage_in_km: int | None = None
    inspection_due_in_days: int | None = None
    inspection_due_in_km: int | None = None
    oil_service_due_in_days: int | None = None
    oil_service_due_in_km: int | None = None


class ConnectionStatusResponse(BaseModel):
    model_config = _CAMEL_CFG
    unreachable: bool | None = None
    in_motion: bool | None = None
    ignition_on: bool | None = None
