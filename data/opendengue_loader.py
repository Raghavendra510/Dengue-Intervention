"""
OpenDengue & Environmental Ingestion Pipeline (Milestone 2 Adapter)
Prepares real-world OpenDengue / NOAA benchmark datasets for the
Surveillance & Intervention Coordinator modules.
"""

import os
import pandas as pd

def ingest_opendengue_raw(raw_csv_path: str, output_csv_path: str = None) -> pd.DataFrame:
    """
    Parses real OpenDengue CSV schema:
      Expected columns: adm_1_name / adm_2_name, year, calendar_start_date, dengue_cases, population
    Standardizes into the project's district-level format.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_csv_path}")

    df_raw = pd.read_csv(raw_csv_path)

    # Standardize column naming
    clean_df = pd.DataFrame()
    district_col = next((c for c in ['adm_2_name', 'adm_1_name', 'district', 'city'] if c in df_raw.columns), None)
    cases_col = next((c for c in ['dengue_cases', 'total_cases', 'reported_cases'] if c in df_raw.columns), None)
    pop_col = next((c for c in ['population', 'pop'] if c in df_raw.columns), None)

    if district_col and cases_col:
        clean_df['District_Name'] = df_raw[district_col].unique()
        clean_df['District_ID'] = [f"D{i+1:02d}" for i in range(len(clean_df))]
        
        # Aggregate latest cases
        latest_cases = df_raw.groupby(district_col)[cases_col].sum().reset_index()
        clean_df = clean_df.merge(latest_cases, left_on='District_Name', right_on=district_col, how='left')
        clean_df.rename(columns={cases_col: 'Reported_Cases'}, inplace=True)
        if district_col in clean_df.columns:
            clean_df.drop(columns=[district_col], inplace=True)

        if pop_col and pop_col in df_raw.columns:
            pop_map = df_raw.groupby(district_col)[pop_col].mean().to_dict()
            clean_df['Population'] = clean_df['District_Name'].map(pop_map).fillna(50000).astype(int)
        else:
            clean_df['Population'] = 75000

        # Compute baseline risk
        clean_df['Baseline_Risk'] = clean_df['Reported_Cases'].apply(lambda x: 'High' if x > 50 else 'Low')

    if output_csv_path:
        clean_df.to_csv(output_csv_path, index=False)
        print(f"[OK] Ingested real OpenDengue dataset saved to {output_csv_path}")

    return clean_df

if __name__ == "__main__":
    print("OpenDengue Loader initialized. Ready to ingest real datasets for Milestone 2.")

