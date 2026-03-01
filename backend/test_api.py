import asyncio
import httpx
import json

base_url = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient() as client:
        print("Registering user...")
        res = await client.post(f"{base_url}/auth/register", json={
            "email": "test@example.com",
            "password": "Password123!",
            "display_name": "Test User"
        })
        if res.status_code == 409:
            print("User already exists, proceeding to login...")
        else:
            print(res.status_code, res.text)
            
        res = await client.post(f"{base_url}/auth/login", json={
            "email": "test@example.com",
            "password": "Password123!"
        })
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Register a fake vehicle
        print("Registering vehicle...")
        res = await client.post(f"{base_url}/vehicles/link", headers=headers, json={
            "email": "skoda@example.com",
            "password": "skodapassword",
            "spin": "1234",
            "vin": "TMBTEST1234567890",
            "display_name": "My Skoda"
        })
        # Note: Linking might fail if Skoda API is called during /link.
        # Let's see what happens.
        print(res.status_code, res.text)
        
        # Let's get list of vehicles
        res = await client.get(f"{base_url}/vehicles", headers=headers)
        print("Vehicles list:", res.status_code, res.text)
        vehicles = res.json()
        
        if not vehicles:
            print("Could not register vehicle due to external API call. We will insert one into DB directly.")
            # We can run another script to insert if necessary.
            
if __name__ == "__main__":
    asyncio.run(main())
