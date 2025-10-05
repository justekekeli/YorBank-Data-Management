CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.yorb_transaction` (
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
ALTER TABLE `totemic-courage-473402-r9.bronze.yorb_transaction` ADD PRIMARY KEY (transaction_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.raw_banking_accounts` (
  balance		numeric,
  account_id		string,	
  created_at		datetime,	
  customer_id		string,	
  account_type		string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers'accounts details"
);
ALTER TABLE `totemic-courage-473402-r9.bronze.raw_banking_accounts` ADD PRIMARY KEY (account_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.raw_banking_advisors` (
  email		string,
  last_name		string,
  advisor_id		string,	
  first_name		string
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank's advisors details"
);
ALTER TABLE `totemic-courage-473402-r9.bronze.raw_banking_advisors` ADD PRIMARY KEY (advisor_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.raw_banking_customers` (
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
ALTER TABLE `totemic-courage-473402-r9.bronze.raw_banking_customers` ADD PRIMARY KEY (customer_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.raw_banking_loans` (
  status		string,
  loan_id		string,	
  end_date		date,	
  principal		numeric,	
  start_date		date,	
  customer_id		string,	
  interest_rate		numeric,
  outstanding_balance		numeric
  )
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Yorbank customers's loans details"
);
ALTER TABLE `totemic-courage-473402-r9.bronze.raw_banking_loans` ADD PRIMARY KEY (loan_id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.bronze.raw_banking_profiles` (
  max_loan		numeric,
  created_at		datetime,
  profile_id		string,
  profile_type		string,
  max_withdrawal		numeric,
  maintenance_fee		numeric
  )
OPTIONS(
  description = "Yorbank customers's profiles types"
);
ALTER TABLE `totemic-courage-473402-r9.bronze.raw_banking_profiles` ADD PRIMARY KEY (profile_id) NOT ENFORCED;