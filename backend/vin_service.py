
import requests
from typing import Dict, Any

def get_vehicle_details(vin: str) -> Dict[str, Any]:
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    resp = requests.get(url, timeout=10)

    if resp.status_code != 200:
        return {"error": "VIN lookup failed"}

    data = resp.json()["Results"]

    result = {}
    for item in data:
        if item["Value"]:
            result[item["Variable"]] = item["Value"]

    # Add estimated market price (mocked; in production, integrate real API)
    make = result.get("Make", "").lower()
    model = result.get("Model", "").lower()
    year = result.get("Model Year", "")
    estimated_price = estimate_vehicle_price(make, model, year)

    return {
        "make": result.get("Make"),
        "model": result.get("Model"),
        "year": result.get("Model Year"),
        "body_class": result.get("Body Class"),
        "engine": result.get("Engine Model"),
        "recalls_note": "Check NHTSA recalls separately",
        "estimated_market_price": estimated_price
    }

def estimate_vehicle_price(make: str, model: str, year: str) -> str:
    """
    Mock vehicle price estimation. Replace with real API integration.
    """
    # Simple mock based on make
    base_prices = {
        "toyota": 25000,
        "honda": 24000,
        "ford": 28000,
        "chevrolet": 27000,
        "bmw": 45000,
        "mercedes": 50000,
        "audi": 42000,
        "nissan": 23000,
        "hyundai": 22000,
        "kia": 21000
    }
    try:
        year_int = int(year) if year else 2020
        depreciation = (2026 - year_int) * 2000  # Rough depreciation
        base = base_prices.get(make, 25000)
        price = max(base - depreciation, 5000)
        return f"${price:,} - ${price + 5000:,}"
    except:
        return "Price estimate unavailable"