import pandas as pd              # pandas handles reading and manipulating data tables
import matplotlib.pyplot as plt  # matplotlib creates graphs and visualisations


# -----------------------------------------------------------
# LOAD CLEANED SYSTEM LOAD DATA
# -----------------------------------------------------------

# Read the cleaned CSV file we previously generated.
# This file contains timestamps and 5-minute operational demand values.
df = pd.read_csv("data/processed/system_load_clean_5min.csv")

# Convert the timestamp column from plain text into a true datetime object.
# This allows filtering by dates and better plotting control.
df["INTERVAL_DATETIME"] = pd.to_datetime(df["INTERVAL_DATETIME"])


# -----------------------------------------------------------
# SELECT ONE DAY TO PLOT
# -----------------------------------------------------------

# Pick a sample day to visualise. Here we simply take the earliest date in the dataset.
sample_date = df["INTERVAL_DATETIME"].dt.date.min()

# Filter the dataset so it contains only rows matching that date.
# This gives us one full day of 5-minute system demand data.
one_day = df[df["INTERVAL_DATETIME"].dt.date == sample_date]


# -----------------------------------------------------------
# PLOT SYSTEM LOAD FOR ONE DAY
# -----------------------------------------------------------

plt.figure(figsize=(12, 5))                     # Create a new chart with a nice wide size

# Plot system demand (y-axis) against time (x-axis)
plt.plot(one_day["INTERVAL_DATETIME"],          # x-axis: timestamps across the day
         one_day["OPERATIONAL_DEMAND"])         # y-axis: MW demand values

plt.xlabel("Time")                              # Label x-axis so viewer knows what it shows
plt.ylabel("Operational Demand (MW)")           # Label y-axis clearly
plt.title(f"NSW System Load – {sample_date}")   # Title including the selected date
plt.tight_layout()                              # Avoid overlapping text labels
plt.show()                                      # Display the plot on screen


# -----------------------------------------------------------
# BUILD LOAD DURATION CURVE (LDC)
# -----------------------------------------------------------

# A Load Duration Curve sorts all demand values from highest to lowest.
# This lets us see how often the system is under high stress.
sorted_load = df["OPERATIONAL_DEMAND"] \
                .sort_values(ascending=False) \
                .reset_index(drop=True)

plt.figure(figsize=(12, 5))                      # Create a wide figure for readability

# Plot the sorted demand values.
# The highest demand appears on the left, then drops toward the right.
plt.plot(sorted_load)

plt.xlabel("Interval Rank (sorted highest → lowest)")   # Explain x-axis terms clearly
plt.ylabel("Operational Demand (MW)")                   # Explain y-axis units
plt.title("Load Duration Curve – NSW 5-Minute Operational Demand")  # Chart title
plt.tight_layout()
plt.show()                                              # Display LDC graph
