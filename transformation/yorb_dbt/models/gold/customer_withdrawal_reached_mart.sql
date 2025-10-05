{{ config(materialized='table') }}

with sliding_month_total_withdrawal as (
    select 
        sender_id as customer_id,
        sum(amount) as total_withdrawal
    from {{ ref('staging_transactions') }} 
    where occurred_at>= date_sub(cast('{{ var("reference_date") }}' as timestamp), interval 30 day)
          and occurred_at< cast('{{ var("reference_date") }}' as timestamp) 
          and transaction_type="withdrawal"
    group by sender_id
)
select
    cast('{{ var("reference_date") }}' as date) as reference_date,
    txn.customer_id,
    cust.first_name as customer_first_name,
    cust.last_name as customer_last_name,
    cust.email as customer_email,
    cust.advisor_email,
    prf.max_withdrawal,
    prf.profile_type
from sliding_month_total_withdrawal txn
inner join {{ ref('staging_customers') }} cust on txn.customer_id = cust.customer_id
inner join {{ ref('staging_profiles') }} prf on cust.profile_id = prf.profile_id
where txn.total_withdrawal/prf.max_withdrawal >= 0.99
