from __future__ import annotations

import logging
import asyncio

import httpx
import aiohttp
from myskoda import MySkoda

from app.config import settings
from app.schemas.skoda import (
    AirConditioningResponse,
    ChargingResponse,
    ConnectionStatusResponse,
    DrivingRangeResponse,
    GarageResponse,
    MaintenanceResponse,
    PositionResponse,
    VehicleStatusResponse,
)

logger = logging.getLogger(__name__)

_BASE = settings.skoda_base_url


class SkodaAPIClient:
    """Read-only client for telemetry collection using manual HTTP calls.
    
    Kept for backward compatibility with the DataCollector until it is refactored.
    """
    def __init__(self, access_token: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=_BASE,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": "iVDrive/1.0",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    async def get_garage(self) -> GarageResponse:
        resp = await self._client.get("/api/v2/garage")
        resp.raise_for_status()
        return GarageResponse.model_validate(resp.json())

    async def get_charging(self, vin: str) -> ChargingResponse:
        resp = await self._client.get(f"/api/v1/charging/{vin}")
        resp.raise_for_status()
        return ChargingResponse.model_validate(resp.json())

    async def get_driving_range(self, vin: str) -> DrivingRangeResponse:
        resp = await self._client.get(f"/api/v2/vehicle-status/{vin}/driving-range")
        resp.raise_for_status()
        return DrivingRangeResponse.model_validate(resp.json())

    async def get_vehicle_status(self, vin: str) -> VehicleStatusResponse:
        resp = await self._client.get(f"/api/v2/vehicle-status/{vin}")
        resp.raise_for_status()
        return VehicleStatusResponse.model_validate(resp.json())

    async def get_air_conditioning(self, vin: str) -> AirConditioningResponse:
        resp = await self._client.get(f"/api/v2/air-conditioning/{vin}")
        resp.raise_for_status()
        return AirConditioningResponse.model_validate(resp.json())

    async def get_position(self, vin: str) -> PositionResponse:
        resp = await self._client.get("/api/v1/maps/positions", params={"vin": vin})
        resp.raise_for_status()
        return PositionResponse.model_validate(resp.json())

    async def get_maintenance(self, vin: str) -> MaintenanceResponse:
        resp = await self._client.get(f"/api/v3/vehicle-maintenance/vehicles/{vin}/report")
        resp.raise_for_status()
        return MaintenanceResponse.model_validate(resp.json())

    async def get_connection_status(self, vin: str) -> ConnectionStatusResponse:
        resp = await self._client.get(f"/api/v2/connection-status/{vin}/readiness")
        resp.raise_for_status()
        return ConnectionStatusResponse.model_validate(resp.json())

    async def get_warning_lights(self, vin: str) -> dict:
        resp = await self._client.get(f"/api/v1/vehicle-health-report/warning-lights/{vin}")
        resp.raise_for_status()
        return resp.json()

    async def get_garage_vehicle(self, vin: str) -> dict:
        resp = await self._client.get(f"/api/v2/garage/vehicles/{vin}")
        resp.raise_for_status()
        return resp.json()

    async def get_vehicle_renders(self, vin: str) -> dict:
        resp = await self._client.get(f"/api/v1/vehicle-information/{vin}/renders")
        resp.raise_for_status()
        return resp.json()

    # Legacy command methods removed/deprecated in favor of SkodaCommandClient
    # to avoid confusion.

    async def close(self) -> None:
        await self._client.aclose()


class SkodaCommandClient:
    """Command execution client using the myskoda library."""
    
    def __init__(self, email: str, password: str, spin: str | None = None) -> None:
        self.email = email
        self.password = password
        self.spin = spin

    async def _execute(self, vin: str, action: str, **kwargs):
        """Execute a command on a specific vehicle."""
        async with aiohttp.ClientSession() as session:
            myskoda = MySkoda(session)
            
            # Login first to get tokens
            await myskoda.connect(self.email, self.password)
            
            try:
                # We need to find the vehicle first to get its object
                vehicle = await myskoda.get_vehicle(vin)
            except Exception as e:
                logger.error(f"Failed to find vehicle {vin}: {e}")
                raise

            if action == "start_climatization":
                temp = kwargs.get("target_temp")
                if temp:
                    await vehicle.set_target_temperature(temp)
                await vehicle.start_air_conditioning()
            
            elif action == "stop_climatization":
                await vehicle.stop_air_conditioning()
            
            elif action == "start_charging":
                await vehicle.start_charging()
            
            elif action == "stop_charging":
                await vehicle.stop_charging()
            
            elif action == "lock":
                await vehicle.lock()
            
            elif action == "unlock":
                if not self.spin:
                    raise ValueError("SPIN is required to unlock vehicle")
                await vehicle.unlock(self.spin)
            
            elif action == "honk_flash":
                await vehicle.honk_flash()
            
            elif action == "wake":
                # myskoda might handle wakeup implicitly, but let's see if there's an explicit call
                # Often just fetching status wakes it, or there is a wake_up method
                if hasattr(vehicle, "wake_up"):
                    await vehicle.wake_up()
                else:
                    # Fallback or specific implementation
                    pass
            else:
                raise ValueError(f"Unknown command action: {action}")
        
        # Session is closed automatically by async with

    async def start_climatization(self, vin: str, target_temp: float):
        await self._execute(vin, "start_climatization", target_temp=target_temp)

    async def stop_climatization(self, vin: str):
        await self._execute(vin, "stop_climatization")

    async def start_charging(self, vin: str):
        await self._execute(vin, "start_charging")

    async def stop_charging(self, vin: str):
        await self._execute(vin, "stop_charging")

    async def lock(self, vin: str):
        await self._execute(vin, "lock")

    async def unlock(self, vin: str, spin: str | None = None):
        # Allow overriding spin if passed explicitly
        if spin:
            self.spin = spin
        await self._execute(vin, "unlock")

    async def honk_flash(self, vin: str):
        await self._execute(vin, "honk_flash")

    async def wake(self, vin: str):
        await self._execute(vin, "wake")

