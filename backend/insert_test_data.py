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
from app.models.telemetry import BatteryHealth, PowerUsage, ChargingCurve, ChargingSession
from app.services.crypto import encrypt_field

async def main():
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Get user
        res = await session.execute(select(User).limit(1))
        user = res.scalar_one_or_none()
        if not user:
            print("No user found")
            return
            
        vehicle_id = uuid.uuid4()
        vin = "TMBTEST1234567890"
        
        vehicle = UserVehicle(
            id=vehicle_id,
            user_id=user.id,
            vin_hash=vin,
            vin_encrypted=encrypt_field(vin),
            display_name="Test Vehicle",
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
        
        bh = BatteryHealth(
            user_vehicle_id=vehicle_id,
            captured_at=now,
            twelve_v_battery_voltage=14.2,
            twelve_v_battery_soc=90.0,
            twelve_v_battery_soh=100.0,
            hv_battery_voltage=380.0,
            hv_battery_current=0.0,
            hv_battery_temperature=20.0,
            hv_battery_soh=100.0,
            hv_battery_degradation_pct=0.0,
            cell_voltage_min=4.1,
            cell_voltage_max=4.2,
            cell_voltage_avg=4.15,
            cell_temperature_min=19.0,
            cell_temperature_max=21.0,
            cell_temperature_avg=20.0,
            imbalance_mv=10.0
        )
        session.add(bh)
        
        pu = PowerUsage(
            user_vehicle_id=vehicle_id,
            captured_at=now,
            total_power_kw=10.0,
            motor_power_kw=8.0,
            hvac_power_kw=1.5,
            auxiliary_power_kw=0.5,
            battery_heater_power_kw=0.0
        )
        session.add(pu)
        
        ch_sess = ChargingSession(
            user_vehicle_id=vehicle_id,
            session_start=now,
            start_level=20.0,
            energy_kwh=50.0
        )
        session.add(ch_sess)
        await session.flush()
        
        cc = ChargingCurve(
            user_vehicle_id=vehicle_id,
            session_id=ch_sess.id,
            captured_at=now,
            soc_pct=50.0,
            power_kw=50.0,
            voltage_v=380.0,
            current_a=131.0,
            battery_temp_celsius=25.0,
            charger_temp_celsius=30.0
        )
        session.add(cc)
        
        await session.commit()
        print(f"Vehicle {vehicle_id} inserted.")

if __name__ == "__main__":
    asyncio.run(main())
