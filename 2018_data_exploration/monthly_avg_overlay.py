import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# 1. Set working directory to project root
# --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
print("WORKING DIRECTORY:", os.getcwd())

# --------------------------------------------------------------
# 2. Load the 2018 NSW demand data from Excel
# --------------------------------------------------------------
file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"

# skiprows=9 skips the blank + metadata rows
df = pd.read_excel(file_path, sheet_name="2018_NSW", skiprows=9)

# Rename to simple column names
df = df.rename(columns={
    "SETTLEMENTDATE": "timestamp",
    "TOTALDEMAND": "demand"
})

# Keep only the two columns we need
df = df[["timestamp", "demand"]]

# Make sure timestamp is datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Drop any rows where timestamp failed to parse
df = df.dropna(subset=["timestamp"])

print("Rows loaded:", len(df))

# --------------------------------------------------------------
# 3. Add helper columns: date, month, minutes since midnight
# --------------------------------------------------------------

# Pure calendar date (used for grouping by day if needed)
df["date"] = df["timestamp"].dt.date

# Month number (1–12)
df["month"] = df["timestamp"].dt.month

# Minutes since midnight:
#   - timestamp.dt.normalize() gives same date at 00:00
#   - subtracting -> time-of-day as a timedelta
#   - total_seconds()/60 -> convert to minutes
df["minutes"] = (
    (df["timestamp"] - df["timestamp"].dt.normalize())
    .dt.total_seconds() / 60.0
)

# --------------------------------------------------------------
# 4. Compute average daily profile for each month
# --------------------------------------------------------------
# Group by month and time-of-day (in minutes),
# then take the mean demand at each half-hour slot.
monthly_profiles = (
    df.groupby(["month", "minutes"])["demand"]
      .mean()
      .reset_index()
)

# Dictionary to map month number to short name
month_names = {
    1: "Jan",  2: "Feb",  3: "Mar",  4: "Apr",
    5: "May",  6: "Jun",  7: "Jul",  8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# --------------------------------------------------------------
# 5. Plot the 12 average daily profiles
# --------------------------------------------------------------
plt.figure(figsize=(14, 7))

for m in range(1, 13):
    df_m = monthly_profiles[monthly_profiles["month"] == m]
    if df_m.empty:
        continue  # skip months with no data (should not happen for 2018)

    # Plot average demand vs minutes since midnight
    plt.plot(
        df_m["minutes"],
        df_m["demand"],
        linewidth=2,
        alpha=0.9,
        label=month_names[m]
    )

# Set x-axis ticks at key times of day
plt.xticks(
    [0, 360, 720, 1080, 1440],
    ["00:00", "06:00", "12:00", "18:00", "24:00"]
)

plt.title("Typical Daily Demand Profile for Each Month (NSW 2018)")
plt.xlabel("Time of Day")
plt.ylabel("Demand (MW)")
plt.legend(ncol=3)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
