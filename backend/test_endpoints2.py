import asyncio
import httpx

base_url = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient() as client:
        # Re-register test user (database got recreated)
        res = await client.post(f"{base_url}/auth/register", json={
            "email": "legacy@example.com",
            "password": "Password123!",
            "display_name": "Legacy User"
        })
        
        res = await client.post(f"{base_url}/auth/login", json={
            "email": "legacy@example.com",
            "password": "Password123!"
        })
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # We must insert a fake vehicle to test these endpoints since database was recreated
        # Actually wait, test_endpoints2 shouldn't insert DB directly. I will create insert script first.
        
if __name__ == "__main__":
    asyncio.run(main())
