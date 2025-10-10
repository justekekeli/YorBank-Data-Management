{{ config(
    materialized = 'incremental',
    incremental_strategy='merge',
    unique_key = ['reference_date','transaction_type','status']
) }}

select
    cast('{{ var("reference_date") }}' as date) as reference_date,
    transaction_type,
    status,
    round(sum( case when transaction_type='maintenance_fee' then abs(amount)
              when transaction_type='loan_repayment' then abs(amount)
              else  0 end),2) as revenue,
    count(transaction_id) as nb_transaction,
    round(sum(abs(amount)),2) as total_amount
from {{ ref('staging_transactions') }} 
where occurred_at>= date_sub(cast('{{ var("reference_date") }}' as timestamp), interval 1 day)
          and occurred_at< cast('{{ var("reference_date") }}' as timestamp) 
group by cast('{{ var("reference_date") }}' as date), transaction_type,status

