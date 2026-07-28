with product_sales as (

    select

        product_id,

        count(distinct order_id) as total_orders,

        sum(item_price) as total_revenue,

        avg(item_price) as average_price

    from {{ ref('stg_order_items') }}

    group by product_id

),


product_info as (

    select

        product_id,

        product_category_name

    from {{ ref('stg_products') }}

),


reviews as (

    select

        oi.product_id,

        avg(r.review_score) as average_review_score

    from {{ ref('stg_reviews') }} r

    join {{ ref('stg_orders') }} o

        using(order_id)

    join {{ ref('stg_order_items') }} oi

        using(order_id)

    group by oi.product_id

)


select

    ps.product_id,

    pi.product_category_name,

    ps.total_orders,

    ps.total_revenue,

    ps.average_price,

    r.average_review_score

from product_sales ps

left join product_info pi

using(product_id)

left join reviews r

using(product_id)
