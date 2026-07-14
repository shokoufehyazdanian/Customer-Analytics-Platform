import great_expectations as gx

context = gx.get_context()

connection_string = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/customer_analytics"
)

data_source = context.data_sources.add_sql(
    name="postgres_customer_db", connection_string=connection_string
)

print(data_source)
