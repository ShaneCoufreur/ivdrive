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
        if not vehicles:
            print("No vehicles")
            return
            
        # find the legacy vehicle
        vehicle_id = None
        for v in vehicles:
            if v["display_name"] == "Legacy Vehicle":
                vehicle_id = v["id"]
        
        if not vehicle_id:
            vehicle_id = vehicles[0]["id"]
            
        print("Using vehicle:", vehicle_id)
        
        # Test legacy endpoints
        endpoints = [
            f"/vehicles/{vehicle_id}/analytics/legacy/charging-power-curve",
            f"/vehicles/{vehicle_id}/analytics/legacy/power-vs-battery-temp",
            f"/vehicles/{vehicle_id}/analytics/legacy/errors",
            f"/vehicles/{vehicle_id}/analytics/legacy/climatization",
        ]
        
        for ep in endpoints:
            res = await client.get(f"{base_url}{ep}", headers=headers)
            print(f"[{res.status_code}] GET {ep}")
            if res.status_code == 200:
                print(res.text[:100] + "...")
            else:
                print("Error:", res.text)
                
if __name__ == "__main__":
    asyncio.run(main())
