"""
Synthetic Data Generator for Dengue Surveillance & Intervention Coordinator
Synthesizes district-level epidemiologic, environmental, and mobility graph data
compatible with OpenDengue and G-SEIR/ST-GNN benchmarks.
"""

import os
import random
import pandas as pd
import numpy as np

def generate_mock_datasets(data_dir: str = None):
    if data_dir is None:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(data_dir, exist_ok=True)

    np.random.seed(42)
    random.seed(42)

    districts = [
        {"District_ID": "D01", "District_Name": "Central Downtown", "Population": 125000, "Hospital_Beds": 120, "Neighbors": "D02,D03,D05"},
        {"District_ID": "D02", "District_Name": "Riverside Slums",   "Population": 98000,  "Hospital_Beds": 45,  "Neighbors": "D01,D04,D06"},
        {"District_ID": "D03", "District_Name": "North Hill",        "Population": 64000,  "Hospital_Beds": 50,  "Neighbors": "D01,D05,D07"},
        {"District_ID": "D04", "District_Name": "East Marshlands",   "Population": 82000,  "Hospital_Beds": 40,  "Neighbors": "D02,D06,D08"},
        {"District_ID": "D05", "District_Name": "Greenfield Suburbs", "Population": 110000, "Hospital_Beds": 80,  "Neighbors": "D01,D03,D09"},
        {"District_ID": "D06", "District_Name": "Industrial Park",   "Population": 53000,  "Hospital_Beds": 30,  "Neighbors": "D02,D04,D10"},
        {"District_ID": "D07", "District_Name": "West End Valley",   "Population": 76000,  "Hospital_Beds": 60,  "Neighbors": "D03,D08,D09"},
        {"District_ID": "D08", "District_Name": "Lakeview Basin",    "Population": 89000,  "Hospital_Beds": 55,  "Neighbors": "D04,D07,D10"},
        {"District_ID": "D09", "District_Name": "Old Town Heritage",  "Population": 105000, "Hospital_Beds": 70,  "Neighbors": "D05,D07,D10"},
        {"District_ID": "D10", "District_Name": "Harbor Port Area",  "Population": 91000,  "Hospital_Beds": 50,  "Neighbors": "D06,D08,D09"}
    ]

    rainfall_levels = ["Low", "High", "High", "High", "Low", "Low", "High", "High", "Low", "High"]
    mosquito_indices = [0.42, 0.88, 0.31, 0.95, 0.25, 0.38, 0.72, 0.84, 0.45, 0.79]
    reported_cases = [34, 112, 18, 145, 12, 22, 67, 89, 41, 76]
    mobility_levels = ["High", "High", "Low", "Medium", "Medium", "High", "Low", "High", "High", "High"]

    for i, d in enumerate(districts):
        d["Rainfall_Level"] = rainfall_levels[i]
        d["Mosquito_Index"] = mosquito_indices[i]
        d["Reported_Cases"] = reported_cases[i]
        d["Mobility_Level"] = mobility_levels[i]
        # Baseline risk rating
        d["Baseline_Risk"] = "High" if d["Reported_Cases"] > 70 or d["Mosquito_Index"] > 0.75 else "Low"
        d["Spraying_Cost"] = random.choice([1000, 1200, 1500])
        d["Testing_Cost"] = random.choice([300, 400, 500])

    df_districts = pd.DataFrame(districts)
    districts_csv_path = os.path.join(data_dir, "districts_mock.csv")
    df_districts.to_csv(districts_csv_path, index=False)
    print(f"[OK] Created synthetic district data: {districts_csv_path} ({len(df_districts)} districts)")

    # Timeseries weather and ovitrap counts
    weather_records = []
    days = 14
    for day in range(1, days + 1):
        for d in districts:
            base_temp = 28.0 + (1.5 if d["Rainfall_Level"] == "Low" else -1.0)
            temp = round(base_temp + random.uniform(-2.0, 2.0), 1)
            humidity = round(75.0 + (12.0 if d["Rainfall_Level"] == "High" else -10.0) + random.uniform(-5.0, 5.0), 1)
            rain_mm = round(random.uniform(25.0, 85.0) if d["Rainfall_Level"] == "High" else random.uniform(0.0, 8.0), 1)
            ovitrap_count = int(d["Mosquito_Index"] * 50 + random.randint(-5, 10))
            ovitrap_count = max(0, ovitrap_count)
            weather_records.append({
                "Day": day,
                "District_ID": d["District_ID"],
                "Temperature_C": temp,
                "Humidity_Pct": humidity,
                "Rainfall_mm": rain_mm,
                "Ovitrap_Larvae_Count": ovitrap_count
            })

    df_weather = pd.DataFrame(weather_records)
    weather_csv_path = os.path.join(data_dir, "weather_timeseries.csv")
    df_weather.to_csv(weather_csv_path, index=False)
    print(f"[OK] Created synthetic timeseries data: {weather_csv_path} ({len(df_weather)} records)")

    return districts_csv_path, weather_csv_path

if __name__ == "__main__":
    generate_mock_datasets()
