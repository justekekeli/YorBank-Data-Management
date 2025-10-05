{{ config(materialized='table') }}

select
    profile_id,
    profile_type,
    max_withdrawal,
    max_loan,
    maintenance_fee,
    created_at
from {{ source('bronze', 'raw_banking_profiles') }}