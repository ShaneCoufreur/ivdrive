import asyncio
import httpx

base_url = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{base_url}/auth/login", json={
            "email": "test@example.com",
            "password": "Password123!"
        })
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get vehicles
        res = await client.get(f"{base_url}/vehicles", headers=headers)
        vehicles = res.json()
        vehicle_id = vehicles[0]["id"]
        
        # Test endpoints
        endpoints = [
            f"/vehicles/{vehicle_id}/analytics/battery-health",
            f"/vehicles/{vehicle_id}/analytics/power-usage",
            f"/vehicles/{vehicle_id}/analytics/charging-curves",
            f"/vehicles/{vehicle_id}/analytics/efficiency",
            f"/vehicles/{vehicle_id}/analytics/charging-costs",
            f"/vehicles/{vehicle_id}/analytics/charging-sessions",
            f"/vehicles/{vehicle_id}/analytics/pulse",
        ]
        
        for ep in endpoints:
            res = await client.get(f"{base_url}{ep}", headers=headers)
            print(f"[{res.status_code}] GET {ep}")
            if res.status_code != 200:
                print("Error:", res.text)
                
if __name__ == "__main__":
    asyncio.run(main())
