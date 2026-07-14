import great_expectations as gx

context = gx.get_context()


suite_name = "orders_quality_suite"


suite = gx.ExpectationSuite(name=suite_name)


context.suites.add(suite)


print(f"Suite '{suite_name}' created successfully")


import great_expectations as gx

context = gx.get_context()


datasource = context.data_sources.get("postgres_customer_db")


asset = datasource.get_asset("olist_orders")


batch_request = asset.build_batch_request()


suite = context.suites.get("orders_quality_suite")


validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)


# Rule 1: تعداد رکوردها
validator.expect_table_row_count_to_be_between(min_value=1000, max_value=200000)


# Rule 2: order_id نباید خالی باشد
validator.expect_column_values_to_not_be_null(column="order_id")


# Rule 3: order_id باید unique باشد
validator.expect_column_values_to_be_unique(column="order_id")


# Rule 4: وضعیت سفارش فقط مقادیر مشخص
validator.expect_column_values_to_be_in_set(
    column="order_status",
    value_set=[
        "delivered",
        "shipped",
        "canceled",
        "processing",
        "unavailable",
        "invoiced",
        "created",
        "approved",
    ],
)


validator.save_expectation_suite()


print("Orders quality rules saved")
