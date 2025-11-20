import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# Set the working directory to your project root
# --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

# --------------------------------------------------------------
# Load cleaned dataset using skiprows=9 (correct header position)
# --------------------------------------------------------------
file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"
df = pd.read_excel(file_path, sheet_name="2018_NSW", skiprows=9)

# Rename to simpler names
df = df.rename(columns={
    "SETTLEMENTDATE": "timestamp",
    "TOTALDEMAND": "demand"
})

# Keep only the relevant columns
df = df[["timestamp", "demand"]]

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

# --------------------------------------------------------------
# Select the day you want to plot
# --------------------------------------------------------------
DAY_TO_PLOT = "2018-01-01"  # change this to any date in 2018

df_day = df[df["timestamp"].dt.date == pd.to_datetime(DAY_TO_PLOT).date()]

print(f"Rows for {DAY_TO_PLOT}: {len(df_day)}")  # should be 48 rows

# --------------------------------------------------------------
# Create the plot
# --------------------------------------------------------------
plt.figure(figsize=(12, 5))
plt.plot(df_day["timestamp"], df_day["demand"])

plt.title(f"NSW Electricity Demand on {DAY_TO_PLOT}")
plt.xlabel("Time of Day")
plt.ylabel("Demand (MW)")

plt.grid(True)
plt.tight_layout()
plt.show()

