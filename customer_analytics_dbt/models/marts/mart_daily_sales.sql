with daily_sales as (

    select

        date(o.purchase_date) as sales_date,

        count(distinct o.order_id) as orders,

        sum(oi.item_price) as revenue

    from {{ ref('fact_orders') }} o

    join {{ ref('stg_order_items') }} oi

    using(order_id)

    group by 1

)

select *

from daily_sales
