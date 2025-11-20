import pandas as pd

def clean_aemo_5min(raw_path, save_path):
    # load rawa AEMO 5min operational demand data
    # clean columns, filter for data rows

    df_raw = pd.read_csv(raw_path)        # load raw file

    # Rename columns
    df_raw.columns = [
        "TYPE", "TABLE", "MEASURE", "VERSION", "REGIONID",
        "INTERVAL_DATETIME", "OPERATIONAL_DEMAND", "ADJUSTMENT",
        "WDR_ESTIMATE", "LASTCHANGED"
    ]

    # Keep only data rows (TYPE="D")
    df = df_raw[df_raw["TYPE"] == "D"].copy()

    # Convert timestamp to datetime object
    df["INTERVAL_DATETIME"] = pd.to_datetime(df["INTERVAL_DATETIME"])

    # Convert demand to numeric
    df["OPERATIONAL_DEMAND"] = pd.to_numeric(df["OPERATIONAL_DEMAND"], errors="coerce")

    # Sort chronologically
    df = df.sort_values("INTERVAL_DATETIME")

    # Reset index
    df = df.reset_index(drop=True)

    # Save cleaned file
    df.to_csv(save_path, index=False)

    return df

import os
print(os.listdir("data/raw"))



if __name__ == "__main__":
    clean_aemo_5min(
        "data/raw/PUBLIC_ACTUAL_OPERATIONAL_DEMAND_5MIN_202511150905_20251115093540.CSV",
        "data/processed/system_load_clean_5min.csv"
    )

