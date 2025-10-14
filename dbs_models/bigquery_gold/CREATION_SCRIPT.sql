CREATE TABLE IF NOT EXISTS `gold.transaction_mart` (
  reference_date date,
  transaction_type string,
  status string,
  revenue float64,
  nb_transaction float64,
  total_amount float64
)
PARTITION BY DATE_TRUNC(reference_date, MONTH)
OPTIONS(
  description = "Transactions KPIs"
);
ALTER TABLE `gold.transaction_mart` ADD PRIMARY KEY (reference_date,transaction_type,status) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `gold.customer_overdraft_mart` (
  id		string,
  reference_date	date,
  customer_id		string,
  customer_first_name string,
  customer_last_name string,
  customer_email string,
  advisor_email string
)
PARTITION BY DATE_TRUNC(reference_date, MONTH)
OPTIONS(
  description = "the customers that overdraft for the last sliding month"
);
ALTER TABLE `gold.customer_overdraft_mart` ADD PRIMARY KEY (id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `gold.customer_withdrawal_reached_mart` (
  reference_date date,
  customer_email		string,
  customer_last_name		string,
  advisor_first_name		string,
  advisor_last_name		string,
  advisor_email		string,
  customer_first_name		string,	
  profile_id		string,	
  max_withdrawal float64,
  customer_id		string
  )
PARTITION BY DATE_TRUNC(reference_date, MONTH)
OPTIONS(
  description = "List of customers who reached the withdrawal limit"
);
ALTER TABLE `gold.customer_withdrawal_reached_mart` ADD PRIMARY KEY (reference_date) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `gold.customer_mart` (
  reference_date		date,
  advisor_email		string,
  profile_type		string,
  total_number		integer
  )
PARTITION BY reference_date
OPTIONS(
  description = "Customers KPIs per profile"
);
ALTER TABLE `gold.customer_mart` ADD PRIMARY KEY (reference_date,advisor_email,profile_type) NOT ENFORCED;