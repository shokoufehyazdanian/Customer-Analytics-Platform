from pathlib import Path

import pandas as pd

from database import get_engine

DATA_PATH = Path("/opt/airflow/data/raw")


def load_csv_to_postgres():

    engine = get_engine()

    csv_files = DATA_PATH.glob("*.csv")

    for file in csv_files:

        table_name = file.stem

        print(f"Loading {table_name}")

        df = pd.read_csv(file)

        df.to_sql(table_name, engine, if_exists="replace", index=False)

        print(f"{table_name} loaded: {len(df)} rows")


if __name__ == "__main__":
    load_csv_to_postgres()
