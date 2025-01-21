import requests
import os
import json

# Google API Configuration
API_KEY = "GOOGLE API KEY"  # Your Google API key
STREET_VIEW_URL = "https://maps.googleapis.com/maps/api/streetview"

# Directories for saving images
geojson_file = "altadena_standardized.geojson"  # Path to your GeoJSON file
image_output_dir = "Altadena_Pictures/StreetView_PreFire"
os.makedirs(image_output_dir, exist_ok=True)

# Fetch and save images
def fetch_street_view_images(geojson_file, output_dir, api_key):
    with open(geojson_file, "r") as f:
        data = json.load(f)
    
    features = data.get("features", [])
    print(f"Processing {len(features)} features...")

    for idx, feature in enumerate(features, start=1):
        # Extract properties for coordinates
        properties = feature.get("properties", {})
        latitude = properties.get("Latitude")
        longitude = properties.get("Longitude")

        if latitude is None or longitude is None:
            print(f"Skipping feature {idx}: Missing latitude or longitude")
            continue

        # Build the Street View API request
        params = {
            "size": "640x640",  # Image size
            "location": f"{latitude},{longitude}",
            "key": api_key
        }

        try:
            # Send request to Google API
            response = requests.get(STREET_VIEW_URL, params=params)
            response.raise_for_status()

            # Check for "location not found" in the response
            if b"The specified location could not be found" in response.content:
                print(f"Feature {idx}: No Street View available at Latitude={latitude}, Longitude={longitude}")
                continue

            # Save the image
            image_name = properties.get("Name", f"streetview_{idx}.jpg")  # Use Name if available
            image_path = os.path.join(output_dir, image_name)
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)
            print(f"Saved image {idx} to {image_path}")

        except Exception as e:
            print(f"Error fetching image for feature {idx}: {e}")

# Run the image fetching process
fetch_street_view_images(geojson_file, image_output_dir, API_KEY)
