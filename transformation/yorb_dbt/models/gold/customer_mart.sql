{{ config(
    materialized = 'incremental',
    incremental_strategy='merge',
    unique_key = ['reference_date','advisor_email','profile_type']
) }}

select
    cast('{{ var("reference_date") }}' as date) as reference_date,
    prf.profile_type,
    cust.advisor_email,
    count(cust.customer_id) as total_number
from {{ ref('staging_customers') }} cust
inner join {{ ref('staging_profiles') }} prf on cust.profile_id = prf.profile_id
group by cast('{{ var("reference_date") }}' as date), prf.profile_type,cust.advisor_email

