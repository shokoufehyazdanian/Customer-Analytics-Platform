with orders as (

    select *

    from {{ ref('stg_orders') }}

),

order_items as (

    select *

    from {{ ref('stg_order_items') }}

)


select

    count(distinct orders.order_id) as total_orders,

    count(distinct orders.customer_id) as total_customers,

    sum(order_items.item_price) as revenue,


    round(

        (

        sum(order_items.item_price)

        /

        count(distinct orders.order_id)

        )::numeric,

        2

    ) as average_order_value


from orders

join order_items

using(order_id)
