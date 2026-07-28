{% set snapshot_date = "2018-06-01" %}

with customer_orders as (

    select

        customer_unique_id,
        order_id,
        purchase_date

    from {{ ref('stg_orders') }}

    where order_status = 'delivered'
      and purchase_date < '{{ snapshot_date }}'

),


customer_value as (

    select

        order_id,

        sum(item_price) as order_value

    from {{ ref('stg_order_items') }}

    group by order_id

),


customer_features as (

    select

        co.customer_unique_id,

        count(distinct co.order_id) as frequency,

        sum(cv.order_value) as monetary,

        max(co.purchase_date) as last_purchase_date,

        min(co.purchase_date) as first_purchase_date


    from customer_orders co


    left join customer_value cv

    using(order_id)


    group by co.customer_unique_id

)


select

    cf.customer_unique_id,

    cf.frequency,

    cf.monetary,


    (
        '{{ snapshot_date }}'::date
        -
        cf.last_purchase_date::date
    ) as recency,


    round(
        (
            cf.monetary::numeric
            /
            nullif(cf.frequency,0)
        ),
        2
    ) as avg_order_value,


    (
        cf.last_purchase_date::date
        -
        cf.first_purchase_date::date
    ) as customer_lifetime_days,


    case

        when (
            '{{ snapshot_date }}'::date
            -
            cf.last_purchase_date::date
        ) > 120

        then 1

        else 0

    end as churn


from customer_features cf
