import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# Set working directory
# --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

# --------------------------------------------------------------
# Load dataset
# --------------------------------------------------------------
file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"
df = pd.read_excel(file_path, sheet_name="2018_NSW", skiprows=9)

# Rename columns
df = df.rename(columns={
    "SETTLEMENTDATE": "timestamp",
    "TOTALDEMAND": "demand"
})

# Keep only what we need
df = df[["timestamp", "demand"]]

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

# --------------------------------------------------------------
# Select month to plot
# --------------------------------------------------------------
YEAR = 2018
MONTH = 1  # January (change this value to any month 1–12)

# Filter for this month
df_month = df[(df["timestamp"].dt.year == YEAR) &
              (df["timestamp"].dt.month == MONTH)]

print(f"Loaded {len(df_month)} rows for {YEAR}-{MONTH:02d}")

# --------------------------------------------------------------
# Prepare the plot
# --------------------------------------------------------------
plt.figure(figsize=(12, 6))

for day, df_day in df_month.groupby(df_month["timestamp"].dt.date):
    # Convert to time offset (minutes since midnight)
    minutes = (df_day["timestamp"] - df_day["timestamp"].dt.normalize()) \
                  .dt.total_seconds() / 60.0

    plt.plot(minutes, df_day["demand"], alpha=0.4, linewidth=1)

# Format the x-axis ticks
plt.xticks(
    [0, 360, 720, 1080, 1440],
    ["00:00", "06:00", "12:00", "18:00", "24:00"]
)

month_name = df_month["timestamp"].dt.month_name().iloc[0]

plt.title(f"NSW Daily Demand Profiles — {month_name} {YEAR}")
plt.xlabel("Time of Day")
plt.ylabel("Demand (MW)")
plt.grid(True)
plt.tight_layout()
plt.show()
