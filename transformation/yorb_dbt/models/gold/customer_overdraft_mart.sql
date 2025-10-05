{{ config(materialized='table') }}

with last_three_months_balance as (
    select
        {{ dbt_utils.generate_surrogate_key(['reference_date','customer_id']) }} as id,
        bal.reference_date,
        bal.customer_id,
        case when bal.balance < 0 then true else false end as is_overdraft 
    from {{ ref('staging_eod_balance') }} as bal 
    where bal.reference_date IN (
        cast('{{ var("overdraft_first_month") }}' as date),
        cast('{{ var("overdraft_second_month") }}' as date),
        cast('{{ var("overdraft_third_month") }}' as date)
    )
)

select
    ls.reference_date,
    ls.id,
    ls.customer_id,
    cust.first_name as customer_first_name,
    cust.last_name as customer_last_name,
    cust.email as customer_email,
    advisor_email
from last_three_months_balance ls inner join {{ ref('staging_customers') }} as cust 
on ls.customer_id = cust.customer_id
group by ls.reference_date,
    ls.id,
    ls.customer_id,
    cust.first_name,
    cust.last_name,
    cust.email,
    advisor_email
having logical_and(is_overdraft)
