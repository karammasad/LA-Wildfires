import os
import requests
import json

# Google API Configuration
API_KEY = "GOOGLE API KEY"  # Replace with your Google API key
STREET_VIEW_URL = "https://maps.googleapis.com/maps/api/streetview"

# File and output directories
geojson_file = "DINS_2025_Eaton_Public_View.geojson"  # Path to your GeoJSON file
output_dir = "Eaton_PreFireImages"
os.makedirs(output_dir, exist_ok=True)

# Function to fetch Street View images
def fetch_street_view_images(geojson_file, output_dir, api_key):
    # Load GeoJSON file
    with open(geojson_file, "r") as f:
        data = json.load(f)

    features = data.get("features", [])
    print(f"Processing {len(features)} features...")

    skipped = 0  # Count of skipped features
    for idx, feature in enumerate(features, start=1):
        # Extract coordinates
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        if not coordinates or len(coordinates) != 2:
            print(f"Skipping feature {idx}: Invalid or missing coordinates")
            skipped += 1
            continue

        longitude, latitude = coordinates

        # Extract feature-specific properties for naming
        properties = feature.get("properties", {})
        object_id = properties.get("OBJECTID", idx)
        damage = properties.get("DAMAGE", "Unknown").replace(" ", "_")
        structure_type = properties.get("STRUCTURETYPE", "Unknown").replace(" ", "_")

        # Create a descriptive filename
        file_name = f"OBJECTID_{object_id}_{damage}_{structure_type}_pre_fire.jpg"
        file_path = os.path.join(output_dir, file_name)

        # Prepare the Street View API request
        params = {
            "size": "640x640",  # Image size
            "location": f"{latitude},{longitude}",
            "key": api_key
        }

        # Fetch and save the image
        try:
            print(f"Downloading image for OBJECTID {object_id} at {latitude}, {longitude}...")
            response = requests.get(STREET_VIEW_URL, params=params, stream=True)
            response.raise_for_status()

            # Save the image
            with open(file_path, "wb") as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)

            print(f"Saved image to {file_path}")
        except Exception as e:
            print(f"Error fetching image for OBJECTID {object_id}: {e}")
            skipped += 1

    print(f"Processing completed. Skipped {skipped} features.")

# Run the function
fetch_street_view_images(geojson_file, output_dir, API_KEY)
