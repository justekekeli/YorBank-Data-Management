{{ config(
    materialized = 'incremental',
    incremental_strategy='merge',
    unique_key = ['reference_date','account_id']
) }}

select
    account_id,
    cast('{{ var("reference_date") }}' as date) as reference_date,
    customer_id,
    balance
from {{ source('bronze', 'raw_banking_accounts') }}
where account_type='normal'