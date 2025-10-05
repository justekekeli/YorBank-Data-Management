{{ config(materialized='table') }}

select
    txn.transaction_id as transaction_id,
    receiver.customer_id as sender_id,
    reciver.customer_id as receiver_id,
    txn.amount as amount,
    txn.transaction_type as transaction_type,
    txn.description as description,
    txn.status as status,
    cast(txn.occurred_at as timestamp) as occurred_at
from {{ source('bronze', 'raw_banking_transactions') }} as txn 
inner join {{ source('bronze', 'raw_banking_account') }} as receiver on txn.receiver_account_id = receiver.account_id
inner join {{ source('bronze', 'raw_banking_account') }} as sender on txn.sender_account_id = sender.account_id