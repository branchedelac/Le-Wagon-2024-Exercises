import pandas as pd

from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path

from taxifare.params import *


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by
    - assigning correct dtypes to each column
    - removing buggy or irrelevant transactions
    """
    # Compress raw_data by setting types to DTYPES_RAW
    DTYPES_RAW = {
        "fare_amount": "float32",
        "pickup_datetime": "datetime64[ns, UTC]",
        "pickup_longitude": "float32",
        "pickup_latitude": "float32",
        "dropoff_longitude": "float32",
        "dropoff_latitude": "float32",
        "passenger_count": "int16",
    }

    df = df.astype(dtype=DTYPES_RAW)

    # Remove buggy transactions
    df = df.dropna(how="any", axis=0)
    df = df[df.passenger_count > 0]
    df = df[df.fare_amount > 0]

    # Remove geographically irrelevant transactions (rows)
    df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
    df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
    df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]

    print("✅ data cleaned")

    return df
