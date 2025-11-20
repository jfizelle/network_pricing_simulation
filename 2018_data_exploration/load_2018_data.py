import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
print("WORKING DIRECTORY:", os.getcwd())

file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"

# ------------------------------------------------------
# Correct skiprows value based on inspection:
# header row is Pandas row 9 → so skip rows 0–8.
# ------------------------------------------------------
df = pd.read_excel(file_path, sheet_name="2018_NSW", skiprows=9)

print("Columns:", df.columns)

# Rename columns we care about
df = df.rename(columns={
    "SETTLEMENTDATE": "timestamp",
    "TOTALDEMAND": "demand"
})

# Keep only timestamp + demand
df = df[["timestamp", "demand"]]

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

df = df.dropna(subset=["timestamp"])

print(df.head())
print("Rows loaded:", len(df))

