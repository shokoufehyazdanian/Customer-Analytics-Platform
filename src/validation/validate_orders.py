import great_expectations as gx

context = gx.get_context()


def validate_orders():

    batch = context.get_validator(
        datasource_name="postgres_datasource", data_asset_name="olist_orders_dataset"
    )

    batch.expect_table_row_count_to_be_between(min_value=90000, max_value=110000)

    batch.expect_column_values_to_not_be_null(column="order_id")

    result = batch.validate()

    print(result)


if __name__ == "__main__":
    validate_orders()
