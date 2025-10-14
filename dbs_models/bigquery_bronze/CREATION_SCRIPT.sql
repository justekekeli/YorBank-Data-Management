CREATE TABLE IF NOT EXISTS `bronze.yorb_transaction` (
  transaction_id   int64,
  sender_account_id string,
  receiver_account_id string,
  amount     float64,
  transaction_type string,
  description string,
  status string,
  occurred_at string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Transactions streamed from FastAPI via Confluent Kafka"
);
ALTER TABLE `bronze.yorb_transaction` ADD PRIMARY KEY (transaction_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `bronze.raw_banking_accounts` (
  balance		float64,
  account_id		string,	
  created_at		datetime,	
  customer_id		string,	
  account_type		string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers'accounts details"
);
ALTER TABLE `bronze.raw_banking_accounts` ADD PRIMARY KEY (account_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `bronze.raw_banking_advisors` (
  email		string,
  last_name		string,
  advisor_id		string,	
  first_name		string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank's advisors details"
);
ALTER TABLE `bronze.raw_banking_advisors` ADD PRIMARY KEY (advisor_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `bronze.raw_banking_customers` (
  email		string,
  last_name		string,
  advisor_id		string,
  created_at		datetime,
  first_name		string,	
  profile_id		string,	
  customer_id		string
  )
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers details"
);
ALTER TABLE `bronze.raw_banking_customers` ADD PRIMARY KEY (customer_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `bronze.raw_banking_loans` (
  status		string,
  loan_id		string,	
  end_date		date,	
  principal		float64,	
  start_date		date,	
  customer_id		string,	
  interest_rate		float64,
  outstanding_balance		float64
  )
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers's loans details"
);
ALTER TABLE `bronze.raw_banking_loans` ADD PRIMARY KEY (loan_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `bronze.raw_banking_profiles` (
  max_loan		float64,
  created_at		datetime,
  profile_id		string,
  profile_type		string,
  max_withdrawal		float64,
  maintenance_fee		float64
  )
OPTIONS(
  description = "Yorbank customers's profiles types"
);
ALTER TABLE `bronze.raw_banking_profiles` ADD PRIMARY KEY (profile_id) NOT ENFORCED;