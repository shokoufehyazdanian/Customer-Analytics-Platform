with source_reviews as (

    select

        review_id,

        order_id,

        review_score::integer as review_score,

        review_comment_title,

        review_comment_message,

        review_creation_date::timestamp as review_created_at,

        review_answer_timestamp::timestamp as review_answered_at,

        row_number() over (
            partition by review_id
            order by review_creation_date desc
        ) as rn

    from {{ source('ecommerce', 'olist_order_reviews_dataset') }}

)

select

    review_id,

    order_id,

    review_score,

    review_comment_title,

    review_comment_message,

    review_created_at,

    review_answered_at

from source_reviews

where rn = 1
