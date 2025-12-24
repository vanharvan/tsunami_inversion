import requests
import re
import time

# --- Configuration ---
stations_file = "stations_list.txt"
output_file = "station_coordinates.csv"
base_url = "https://www.ndbc.noaa.gov/station_page.php"

# --- 1. Read Station List ---
try:
    with open(stations_file, "r") as f:
        stations = [line.strip() for line in f if line.strip()]
    print(f"Found {len(stations)} stations to process.")
except FileNotFoundError:
    print(f"Error: Could not find '{stations_file}'.")
    stations = []

results = []

# --- 2. Iterate Through Stations ---
print("Starting metadata extraction (Script Method)...\n")

for station_code in stations:
    print(f"Processing Station: {station_code}...", end=" ", flush=True)
    
    try:
        # A. Request Page
        params = {"station": station_code}
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"[Error: HTTP {response.status_code}]")
            continue
            
        raw_html = response.text
        
        # B. Extract using Regex on the Javascript variables
        # Pattern looks for: const currentstnlat = '-26.743';
        lat_match = re.search(r"const\s+currentstnlat\s*=\s*'([^']+)'", raw_html)
        lon_match = re.search(r"const\s+currentstnlng\s*=\s*'([^']+)'", raw_html)

        if lat_match and lon_match:
            try:
                lat = float(lat_match.group(1))
                lon = float(lon_match.group(1))
                
                print(f"[Found: {lat}, {lon}]")
                
                # C. Apply 0-360 Conversion for Longitude
                # If negative (West), add 360.
                #if lon < 0:
                #    lon = 360 + lon
                
                results.append({
                    "lon": lon,
                    "lat": lat,
                    "station_code": f"%{station_code}" 
                })
            except ValueError:
                print("[Error: Could not convert data to number]")
        else:
            print("[Error: JS Variables not found]")

    except Exception as e:
        print(f"[Exception: {e}]")
    
    # Pause briefly to be polite to the server
    time.sleep(0.5)

# --- 3. Save to File ---
if results:
    with open(output_file, "w") as f:
        for row in results:
            # Format: 286.017, -26.743 %32402
            # Using .3f to match the precision in your example
            f.write(f"{row['lon']:.3f}, {row['lat']:.3f} {row['station_code']}\n")
    
    print("-" * 30)
    print(f"Done! Extracted {len(results)} locations.")
    print(f"Saved to: {output_file}")
    
else:
    print("\nNo coordinates extracted.")