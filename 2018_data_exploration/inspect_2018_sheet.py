import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

file_path = "data/raw/2018_NSW_20210618_simplified.xlsx"

# Load FIRST 20 rows with header=None so Pandas doesn't guess
df = pd.read_excel(file_path, sheet_name="2018_NSW", nrows=20, header=None)

print(df)
