{{ config(
    materialized = 'incremental',
    incremental_strategy='merge',
    unique_key = ['transaction_id']
) }}

select
    txn.transaction_id as transaction_id,
    sender.customer_id as sender_id,
    receiver.customer_id as receiver_id,
    txn.amount as amount,
    txn.transaction_type as transaction_type,
    txn.description as description,
    txn.status as status,
    cast(txn.occurred_at as timestamp) as occurred_at
from {{ source('bronze', 'yorb_transaction') }} as txn 
inner join {{ source('bronze', 'raw_banking_accounts') }} as receiver on txn.receiver_account_id = receiver.account_id
inner join {{ source('bronze', 'raw_banking_accounts') }} as sender on txn.sender_account_id = sender.account_id
where cast(txn.occurred_at as timestamp)>= date_sub(cast('{{ var("reference_date") }}' as timestamp), interval 1 day)
          and  cast(txn.occurred_at as timestamp)< cast('{{ var("reference_date") }}' as timestamp) 