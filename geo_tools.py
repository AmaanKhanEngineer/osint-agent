# ── 1. IMPORTS & CONFIG ─────────────────────────────────────
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
STATICMAP_URL = "https://maps.googleapis.com/maps/api/staticmap"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


# ── 2. GEOCODING (Google Maps with OpenStreetMap Fallback) ──
def geocode_address(address: str) -> dict:
    """Convert an address or place name into latitude/longitude coordinates."""
    # Attempt 1: Google Geocoding API if key is present
    if API_KEY and API_KEY != "your_google_maps_key_here":
        try:
            response = requests.get(GEOCODE_URL, params={"address": address, "key": API_KEY}, timeout=10)
            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                location = result["geometry"]["location"]
                return {
                    "formatted_address": result["formatted_address"],
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "place_types": result.get("types", []),
                    "provider": "Google Maps"
                }
        except Exception:
            pass

    # Attempt 2: Free OpenStreetMap Nominatim Fallback
    try:
        headers = {"User-Agent": "OSINT-Agent-Intelligence/2.0"}
        resp = requests.get(NOMINATIM_URL, params={"q": address, "format": "json", "limit": 1}, headers=headers, timeout=10)
        data = resp.json()
        if data and len(data) > 0:
            first = data[0]
            return {
                "formatted_address": first.get("display_name", address),
                "latitude": float(first.get("lat")),
                "longitude": float(first.get("lon")),
                "place_types": [first.get("type", "landmark"), first.get("class", "place")],
                "provider": "OpenStreetMap"
            }
    except Exception as e:
        return {"error": f"Geocoding fallback failed: {str(e)}"}

    return {"error": f"Could not geocode address: {address}"}


# ── 3. SATELLITE IMAGERY ────────────────────────────────────
def get_satellite_image_url(address: str = None, lat: float = None, lng: float = None, zoom: int = 17) -> str:
    """Get a satellite image URL. Zoom: 15=neighborhood, 17=building, 19=close-up."""
    if address and (lat is None or lng is None):
        geocoded = geocode_address(address)
        if "error" in geocoded:
            return geocoded["error"]
        lat, lng = geocoded["latitude"], geocoded["longitude"]

    if lat is None or lng is None:
        return "Error: Provide either address or lat/lng coordinates."

    if API_KEY and API_KEY != "your_google_maps_key_here":
        return f"{STATICMAP_URL}?center={lat},{lng}&zoom={zoom}&size=640x480&maptype=satellite&key={API_KEY}"
    else:
        # ESRI World Imagery satellite tile reference
        return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/1/1"


# ── 4. LOCATION INTELLIGENCE ────────────────────────────────
def get_location_intelligence(location_query: str) -> str:
    """Get comprehensive location intelligence: satellite imagery at three zoom levels plus context."""
    geocoded = geocode_address(location_query)
    if "error" in geocoded:
        return f"Location reconnaissance notice: {geocoded['error']}"

    lat = geocoded["latitude"]
    lng = geocoded["longitude"]
    formatted = geocoded["formatted_address"]
    types = ", ".join(geocoded.get("place_types", [])) or "commercial / institutional facility"
    provider = geocoded.get("provider", "OpenStreetMap")

    has_google_key = bool(API_KEY and API_KEY != "your_google_maps_key_here")

    if has_google_key:
        wide = get_satellite_image_url(lat=lat, lng=lng, zoom=14)
        building = get_satellite_image_url(lat=lat, lng=lng, zoom=17)
        close = get_satellite_image_url(lat=lat, lng=lng, zoom=19)
        imagery_block = f"""🛰️ **Satellite imagery at multiple zoom levels:**
- Wide area (neighborhood context): {wide}
- Building level: {building}
- Close-up detail: {close}"""
    else:
        imagery_block = f"""🛰️ **Interactive Geospatial Coordinates:**
- Direct Satellite Coordinates: `{lat}, {lng}`
- Provider Verified: {provider}
- Satellite View Portal: https://www.google.com/maps/@{lat},{lng},17z/data=!3m1!1e3"""

    return f"""=== LOCATION INTELLIGENCE ===

📍 **Location:** {formatted}
🌐 **Coordinates:** {lat}, {lng}
🏷️ **Type:** {types}
📡 **Geocoding Source:** {provider}

{imagery_block}

🗺️ **Google Maps Satellite Link:** https://www.google.com/maps/@{lat},{lng},17z/data=!3m1!1e3
🌍 **OpenStreetMap Link:** https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=17/{lat}/{lng}
"""
