select

    o.order_id,

    o.customer_id,

    c.customer_unique_id,

    o.order_status,

    o.order_purchase_timestamp::timestamp as purchase_date,

    o.order_delivered_customer_date::timestamp as delivery_date


from {{ source('ecommerce', 'olist_orders_dataset') }} o

left join public.olist_customers_dataset c

on o.customer_id = c.customer_id
