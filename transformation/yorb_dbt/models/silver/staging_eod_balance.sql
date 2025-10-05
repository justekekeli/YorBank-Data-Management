{{ config(materialized='table') }}

select
    account_id,
    cast('{{ var("reference_date") }}' as date) as reference_date,
    customer_id,
    balance
from {{ source('bronze', 'raw_banking_accounts') }}
where account_type='normal'