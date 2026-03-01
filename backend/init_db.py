import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.config import settings
import app.models.user
import app.models.vehicle
import app.models.telemetry

async def main():
    engine = create_async_engine(settings.database_url, echo=True)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Database initialized.")

if __name__ == "__main__":
    asyncio.run(main())
