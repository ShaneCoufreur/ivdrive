import asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.user import User
from app.models.vehicle import UserVehicle, ConnectorSession
from app.models.telemetry import (
    BatteryHealth, PowerUsage, ChargingCurve, ChargingSession,
    ChargingPower, ClimatizationState, OutsideTemperature, BatteryTemperature, WeconnectError
)
from app.services.crypto import encrypt_field

async def main():
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Get user or create
        res = await session.execute(select(User).limit(1))
        user = res.scalar_one_or_none()
        if not user:
            print("No user found. Please create one.")
            return
            
        vehicle_id = uuid.uuid4()
        vin = "TMBLEGACY12345"
        
        vehicle = UserVehicle(
            id=vehicle_id,
            user_id=user.id,
            vin_hash=vin,
            vin_encrypted=encrypt_field(vin),
            display_name="Legacy Vehicle",
            collection_enabled=True,
            collection_interval_seconds=300
        )
        session.add(vehicle)
        
        cs = ConnectorSession(
            user_vehicle_id=vehicle_id,
            connector_type="skoda",
            status="active"
        )
        session.add(cs)
        
        now = datetime.now(timezone.utc)
        
        # Legacy items
        session.add(ChargingPower(
            user_vehicle_id=vehicle_id,
            first_date=now,
            last_date=now,
            power=50.5
        ))
        
        session.add(ClimatizationState(
            user_vehicle_id=vehicle_id,
            first_date=now,
            last_date=now,
            state="HEATING"
        ))
        
        session.add(OutsideTemperature(
            user_vehicle_id=vehicle_id,
            first_date=now,
            last_date=now,
            outside_temperature=-5.0
        ))
        
        session.add(BatteryTemperature(
            user_vehicle_id=vehicle_id,
            first_date=now,
            last_date=now,
            battery_temperature=10.0
        ))
        
        session.add(WeconnectError(
            user_vehicle_id=vehicle_id,
            datetime=now,
            error_text="Timeout calling Skoda API"
        ))
        
        await session.commit()
        print(f"Legacy Vehicle {vehicle_id} inserted.")

if __name__ == "__main__":
    asyncio.run(main())
