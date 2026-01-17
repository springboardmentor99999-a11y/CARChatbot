import requests

def get_vehicle_details(vin: str) -> dict:
    """
    Fetches vehicle details from the NHTSA vPIC API using a VIN.
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    
    try:
        # Send request to NHTSA API
        resp = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if resp.status_code != 200:
            return {"error": "VIN lookup failed", "status_code": resp.status_code}
        
        # Parse the JSON response
        data = resp.json().get("Results", [])
        
        # Convert the list of results into a flattened dictionary
        result_map = {}
        for item in data:
            # Only map keys that have an actual value
            if item.get("Value") and item.get("Variable"):
                result_map[item["Variable"]] = item["Value"]
        
        # Return a structured subset of the data
        return {
            "make": result_map.get("Make"),
            "model": result_map.get("Model"),
            "year": result_map.get("Model Year"),
            "body_class": result_map.get("Body Class"),
            "engine": result_map.get("Engine Model"),
            "recalls_note": "Check NHTSA recalls separately"
        }

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        return {"error": f"Connection error: {str(e)}"}
    except Exception:
        # Fallback for unexpected errors
        return {"error": "An unexpected error occurred"}

# Example Usage:
# details = get_vehicle_details("YOUR_VIN_HERE")
# print(details)