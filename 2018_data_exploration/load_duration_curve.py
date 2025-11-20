import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------
# 1. Set working directory to project root
# --------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
print("WORKING DIRECTORY:", os.getcwd())

# --------------------------------------------------------------
# 2. Load and clean the NSW 2018 demand data
# --------------------------------------------------------------
file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="2018_NSW",
    skiprows=9  # remove metadata rows
)

# Rename columns
df = df.rename(columns={
    "SETTLEMENTDATE": "timestamp",
    "TOTALDEMAND": "demand"
})

# Keep only useful columns
df = df[["timestamp", "demand"]]

# Convert to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Drop missing timestamps
df = df.dropna(subset=["timestamp"])

print("Rows loaded:", len(df))

# --------------------------------------------------------------
# 3. Build the Load Duration Curve
# --------------------------------------------------------------

# Step 1: Extract the demand values
demand_values = df["demand"].values

# Step 2: Sort them in descending order
sorted_demand = np.sort(demand_values)[::-1]

# Step 3: Build an "hours" or "sample index" axis (x-axis)
# NOTE: This data is half-hourly.
N = len(sorted_demand)
duration_axis = range(N)   # 0 to N-1 duration steps

# --------------------------------------------------------------
# 4. Plot the Load Duration Curve
# --------------------------------------------------------------
plt.figure(figsize=(12, 6))

plt.plot(duration_axis, sorted_demand, linewidth=2)

plt.title("Load Duration Curve — NSW 2018")
plt.xlabel("Ranked interval (0 = highest demand)")
plt.ylabel("Demand (MW)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
