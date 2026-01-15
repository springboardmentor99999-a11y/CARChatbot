# backend/vin_service.py

import requests


def get_vehicle_details(vin: str) -> dict:
    """
    Fetch vehicle details from NHTSA API using VIN
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
