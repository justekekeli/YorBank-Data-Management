{{ config(materialized='table') }}

with last_third_month_balance as (
    select
        {{ dbt_utils.surrogate_key(['month_value','year_value','customer_id']) }} as id,
        month(reference_date) as month_value,
        year(reference_date) as year_value,
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
    ls.id,
    ls.month_value,
    ls.year_value,
    ls.customer_id,
    cust.first_name as customer_first_name,
    cust.last_name as customer_last_name,
    cust.email as customer_email,
    advisor_email
from last_third_month_balance ls inner join {{ ref('staging_customers') }} as cust 
on ls.customer_id = cust.customer_id
group by ls.id,
    ls.month_value,
    ls.year_value,
    ls.customer_id,
    cust.first_name as customer_first_name,
    cust.last_name as customer_last_name,
    cust.email as customer_email,
    advisor_email
having bool_and(is_overdraft)
