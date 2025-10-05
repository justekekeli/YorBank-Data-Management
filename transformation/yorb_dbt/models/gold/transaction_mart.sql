{{ config(materialized='table') }}

select
    cast('{{ var("reference_date") }}' as date) as reference_date,
    transaction_type,
    status,
    sum( case when transaction_type='maintenance_fee' then amount 
              when transaction_type='loan_repayment' then amount 
              else  0 end) as revenue,
    sum(transaction_id) as nb_transaction,
    sum(amount) as total_amount,
    count(cust.customer_id) as total_number
from {{ ref('staging_transactions') }} cust
where occurred_at>= date_sub(cast('{{ var("reference_date") }}' as timestamp), interval 1 day)
          and occurred_at< cast('{{ var("reference_date") }}' as timestamp) 
group by cast('{{ var("reference_date") }}' as date), transaction_type,status

