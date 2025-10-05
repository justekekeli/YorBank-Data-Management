CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.gold.transaction_mart` (
  reference_date date,
  transaction_type string,
  status string,
  revenue numeric,
  nb_transaction numeric,
  total_amount numeric
)
PARTITION BY DATE_TRUNC(reference_date, MONTH)
OPTIONS(
  description = "Transactions KPIs"
);
ALTER TABLE `totemic-courage-473402-r9.gold.transaction_mart` ADD PRIMARY KEY (reference_date,transaction_type,status) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.gold.customer_overdraft_mart` (
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
ALTER TABLE `totemic-courage-473402-r9.gold.customer_overdraft_mart` ADD PRIMARY KEY (id) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.gold.customer_withdrawal_reached_mart` (
  reference_date date,
  customer_email		string,
  customer_last_name		string,
  advisor_first_name		string,
  advisor_last_name		string,
  advisor_email		string,
  customer_first_name		string,	
  profile_id		string,	
  max_withdrawal numeric,
  customer_id		string
  )
PARTITION BY DATE_TRUNC(reference_date, MONTH)
OPTIONS(
  description = "List of customers who reached the withdrawal limit"
);
ALTER TABLE `totemic-courage-473402-r9.gold.customer_withdrawal_reached_mart` ADD PRIMARY KEY (reference_date) NOT ENFORCED;

CREATE TABLE IF NOT EXISTS `totemic-courage-473402-r9.gold.customer_mart` (
  reference_date		date,
  advisor_email		string,
  profile_type		string,
  total_number		integer
  )
PARTITION BY reference_date
OPTIONS(
  description = "Customers KPIs per profile"
);
ALTER TABLE `totemic-courage-473402-r9.gold.customer_mart` ADD PRIMARY KEY (reference_date,advisor_email,profile_type) NOT ENFORCED;