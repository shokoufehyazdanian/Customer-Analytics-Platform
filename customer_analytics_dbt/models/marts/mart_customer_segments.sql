with customer_orders as (

    select

        orders.customer_id,

        count(distinct orders.order_id) as frequency,

        sum(order_items.item_price) as monetary

    from {{ ref('stg_orders') }} orders

    join {{ ref('stg_order_items') }} order_items

    using(order_id)

    group by orders.customer_id

)

select

    customer_id,

    frequency,

    monetary,

    case

        when monetary > 1000
        and frequency >= 5
        then 'VIP'

        when frequency >= 3
        then 'Loyal'

        when frequency = 1
        then 'New'

        else 'Regular'

    end as customer_segment

from customer_orders
