import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

FILE_IN = r"C:\Users\fiz001\Downloads\cdintervalreadingallnoquotes.csv\CD_INTERVAL_READING_ALL_NO_QUOTES.csv"
FILE_OUT = r"C:\Users\fiz001\PycharmProjects\SmartGridData_Parse\nov_2025_a0_output\sgsc.parquet"

CHUNKSIZE = 5_000_000                                                                      # constant variable assigned to 5 mil - pandas to read the file 5mil lines at a times - manage ram
COMPRESSION = "snappy"                                                                     # constant variable assigned to snappy (fast compression algorithm)

def clean_column_names(df):
    df.columns = [c.strip().upper() for c in df.columns]                                   # list comprehension: for each column name remove leading and trailing whitespace and converts all letters to uppercase
    return df

def normalise_units(df):
    kwh_cols = [c for c in df.columns if c.endswith("_KWH")]                               # list comprehension: for each column ending with _KWH
    for col in kwh_cols:                                                                   # loop through all KWH columns
        wh_col = col.replace("_KWH", "_WH")                                                # replace _KWH with _Wh: wh_col -> new column to store watt hours
        df[wh_col] = (df[col] * 1000).astype("int32")                                      # multiply every value by 1000 (kwh->wh) /
        df.drop(columns=[col], inplace=True)
    return df

def parse_time(df):
    df["READING_DATETIME"] = pd.to_datetime(df["READING_DATETIME"], errors="coerce", format="mixed")
    return df

def add_total_load(df):
    needed = ["GENERAL_SUPPLY_WH", "CONTROLLED_LOAD_WH", "OTHER_WH"]
    df["TOTAL_LOAD_WH"] = df[needed].sum(axis=1).astype("int32")
    return df

def transform(df):
    return (
        df.pipe(clean_names)
          .pipe(normalise_units)
          .pipe(parse_time)
          .pipe(add_total_load)
    )

def write_parquet(df, writer):
    table = pa.Table.from_pandas(df)
    if writer is None:
        writer = pq.ParquetWriter(FILE_OUT, table.schema, compression=COMPRESSION)
    writer.write_table(table)
    return writer

def run():
    if os.path.exists(FILE_OUT):
        os.remove(FILE_OUT)

    writer = None
    for i, chunk in enumerate(pd.read_csv(FILE_IN, chunksize=CHUNKSIZE)):
        print(f"→ Chunk {i}")
        processed = transform(chunk)
        writer = write_parquet(processed, writer)

    if writer:
        writer.close()

if __name__ == "__main__":
    run()

