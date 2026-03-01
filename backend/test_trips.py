import asyncio
from app.services.skoda_auth import SkodaAuthClient
from app.services.skoda_api import SkodaAPIClient
from app.config import settings

async def main():
    auth = SkodaAuthClient()
    tokens = await auth.login(settings.skoda_username, settings.skoda_password)
    access_token = tokens.get("accessToken") or tokens.get("access_token")
    await auth.close()
    
    api = SkodaAPIClient(access_token)
    try:
        resp = await api._client.get(f"/api/v1/trip-statistics/vehicles/{settings.skoda_vin}/trips")
        print(resp.status_code)
        print(resp.text[:500])
    except Exception as e:
        print(e)
    await api.close()

if __name__ == "__main__":
    asyncio.run(main())
