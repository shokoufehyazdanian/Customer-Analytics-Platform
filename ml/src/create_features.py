import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/customer_analytics"
)


query = """

SELECT *

FROM public_analytics.mart_customer_rfm

LIMIT 5

"""


df = pd.read_sql(query, engine)


print(df.head())
