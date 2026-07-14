import great_expectations as gx

context = gx.get_context()


datasource = context.data_sources.get("postgres_customer_db")


asset = datasource.get_asset("olist_orders")


batch_request = asset.build_batch_request()


suite = context.suites.get("default")


validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)


result = validator.validate()


print(result)
