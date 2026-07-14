import great_expectations as gx

context = gx.get_context()

datasource = context.data_sources.get("postgres_customer_db")

asset = datasource.get_asset("olist_orders")

batch_request = asset.build_batch_request()

validator = context.get_validator(batch_request=batch_request)


validator.expect_table_row_count_to_be_between(min_value=1000, max_value=200000)


validator.expect_column_values_to_not_be_null(column="order_id")


validator.expect_column_values_to_be_unique(column="order_id")


validator.save_expectation_suite()

print("Expectations saved")
