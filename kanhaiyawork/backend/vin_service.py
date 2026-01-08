print(">>> vin_service module loaded")

import requests

def get_vehicle_details(vin: str) -> dict:
    print(">>> get_vehicle_details called with:", vin)

    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()