{{ config(materialized='table') }}

select
    customer_id,
    concat(
        upper(substring(adv.first_name, 1, 1)),
        lower(substring(adv.first_name, 2, LENGTH(name)))
    ) as advisor_first_name,
    upper(adv.last_name) as advisor_last_name,
    adv.email as advisor_email,
    cust.profile_id as profile_id,
    cust.first_name as first_name,
    cust.last_name as last_name,
    cust.email as email,
    cust.created_at as created_at,
from {{ source('bronze', 'raw_banking_customers') }} as cust
left join {{ source('bronze', 'raw_banking_advisors') }} as adv
on cust.advisor_id = adv.advisor_id