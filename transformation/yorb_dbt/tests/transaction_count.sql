-- Business test: transaction number can't be null
with count as (
    select count(*) as nb
        from {{ ref('staging_transactions') }} 
        where occurred_at>= date_sub(cast('{{ var("reference_date") }}' as timestamp), interval 1 day)
          and occurred_at< cast('{{ var("reference_date") }}' as timestamp) 
)
select 'staging_transactions table is empty' as error_message
from count
where nb = 0