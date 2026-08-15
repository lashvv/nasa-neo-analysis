"""
Fetch NASA/JPL Small-Body Database Close-Approach data and save it as a CSV.

Docs: https://ssd-api.jpl.nasa.gov/doc/cad.html
No API key required.
"""

import requests
import pandas as pd

params = {
    "date-min": "1900-01-01",
    "date-max": "2200-01-01",
    "dist-max": "0.05",
    "neo": "true",
    "diameter": "true",
    "fullname": "true",
}
# Note: diameter=true just adds a diameter column - it does NOT filter rows.
# Most rows will have null for diameter since only a small fraction of
# asteroids have a measured/estimated size on file.

URL = "https://ssd-api.jpl.nasa.gov/cad.api"

print("Requesting data from NASA/JPL...")
response = requests.get(URL, params=params)
response.raise_for_status()

payload = response.json()

print(f"Got {payload['count']} records.")
print(f"Fields: {payload['fields']}")

# Convert to a DataFrame
df = pd.DataFrame(payload["data"], columns=payload["fields"])

# Save raw dataset into data/raw (relative to project root)
output_path = "../../data/raw/neo_close_approaches_raw.csv"
df.to_csv(output_path, index=False)

print(f"Saved to {output_path}")
print(df.head())