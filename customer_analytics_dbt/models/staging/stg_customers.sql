select

    customer_id,

    customer_unique_id,

    customer_zip_code_prefix::varchar as zip_code,

    customer_city,

    customer_state

from {{ source('ecommerce', 'olist_customers_dataset') }}
