CREATE TABLE IF NOT EXISTS `silver.staging_transactions` (
  transaction_id   int64,
  sender_id string,
  receiver_id string,
  amount     float64,
  transaction_type string,
  description string,
  status string,
  occurred_at timestamp
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Transactions cleaned with dbt"
);
ALTER TABLE `silver.staging_transactions` ADD PRIMARY KEY (transaction_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `silver.staging_eod_balance` (
  balance		numeric,
  account_id		string,	
  reference_date		date,	
  customer_id		string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers'end of day balance on normal accounts"
);
ALTER TABLE `silver.staging_eod_balance` ADD PRIMARY KEY (account_id,reference_date) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `silver.staging_customers` (
  email		string,
  last_name		string,
  advisor_first_name		string,
  advisor_last_name		string,
  advisor_email		string,
  created_at		datetime,
  first_name		string,	
  profile_id		string,	
  customer_id		string
  )
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers details enriched"
);
ALTER TABLE `silver.staging_customers` ADD PRIMARY KEY (customer_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `silver.staging_profiles` (
  max_loan		numeric,
  created_at		datetime,
  profile_id		string,
  profile_type		string,
  max_withdrawal		numeric,
  maintenance_fee		numeric
  )
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers's profiles types"
);
ALTER TABLE `silver.staging_profiles` ADD PRIMARY KEY (profile_id) NOT ENFORCED;