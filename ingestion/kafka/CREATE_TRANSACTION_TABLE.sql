CREATE TABLE `totemic-courage-473402-r9.bronze.yorb_transaction` (
  transaction_id   INT64,
  sender_account_id STRING,
  receiver_account_id STRING,
  amount     FLOAT64,
  transaction_type STRING,
  description STRING,
  status STRING,
  occurred_at STRING
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description = "Transactions streamed from FastAPI via Confluent Kafka"
);
