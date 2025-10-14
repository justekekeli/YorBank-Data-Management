# 🏦 YorBank-Data-Management

This project simulates a **modern data platform** for **Yorbank**, a FinTech company offering online banking services for private individuals.  
Customers can have **normal, savings, and investment accounts**, request **loans**, and are supported by **financial advisors**.  
I integrate both **banking transaction data (via API)** and **customers data (via postgreSQL)** into a **BigQuery data warehouse**, and use **dbt** to build **Bronze → Silver → Gold** layers following the **Medallion Architecture**.

---

## 🚀 Project Objectives

1. **Advisor Use Case**
   - Daily report of customers with:
     - Overdrawn balances for 3 consecutive months  
     - Customers reaching max withdrawal limits over the last 3 months  
   - Advisors only see **their customers’ alerts**.

2. **Business Use Case**
   - Dashboard for revenue:
     - Commission on account maintenance  
     - Profit on loans  
     - number of customers
     - amount of transactions
     - number of transactions

---

## 🏗️ Architecture Overview

![image](media/Architecture.png)

## 📂 Data Sources

- Banking API :Transactions stream (deposit, withdrawal, loan_repayment, etc.)
```
**[
    {
        "transaction_id": "Integer",
        "sender_account_id": "String",
        "receiver_account_id": "String",
        "amount": "Decimal",
        "transaction_type": "String",
        "description" : "String" ,
        "status": "String",
        "occurred_at": "YYYY-MM-DDTHH:MM:SSZ"
    }

]**
```
- Accounts details on PostgreSQL

![image](media/yorbank_postgres_db.png)

🧱 Medallion Architecture

![image](media/yorbank_bigquery_dw.png)


## ⚙️ Tech Stack
1. Ingestion
   1. Kafka on Confluent Cloud for real-time streaming (transactions API)
   2. Airbyte for batch ingestion
2. Warehouse
   1. Big Query
3. Transformation
   1. dbt
4. Orchestration
   1. Airglow to schedule dbt flow and data export
5. Visualizattion
   1. Power BI dashboards for business team
   2. CSV/Excel exports for advisors

## Airflow orchestration 

| Gold Model                         | Schedule          | Dependencies                                                            | dbt Variables                                                                                               |
| ---------------------------------- | ----------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `customer_withdrawal_reached_mart` | Daily             | After both `staging_customers` and `staging_transactions` tests succeed | `reference_date={{ ds }}`                                                                                   |
| `customer_overdraft_mart`          | Monthly (1st day) | After `staging_customers` tests succeed                                 | `overdraft_first_month`, `overdraft_second_month`, `overdraft_third_month` = last days of previous 3 months |
| `customer_mart`                    | Daily             | After `staging_customers` tests succeed                                 | `reference_date={{ ds }}`                                                                                   |
| `transaction_mart`                 | Daily             | After `staging_transactions` tests succeed                              | `reference_date={{ ds }}`                                                                                   |

![image](media/airflow_orchestration.png)

## 📈💰📊 PowerBI reports

### Business Dashboard

![image](media/yorbank_dashboard.png)

### Advisor Report

![image](media/advisor_report_page_1.png)

![image](media/advisor_report_page_2.png)

## 𖣂 Folder Structure
```
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── folder_tree.py
├── airflow
│   ├── dags
│   │   ├── .gitignore
│   │   ├── __pycache__
│   │   ├── customer_mart_dag.py
│   │   ├── customer_overdraft_mart_dag.py
│   │   ├── customer_withdrawal_reached_mart_dag.py
│   │   ├── orchestrator.py
│   │   ├── staging_customers_dag.py
│   │   ├── staging_eod_balance_dag.py
│   │   ├── staging_profiles_dag.py
│   │   ├── staging_transactions_dag.py
│   │   └── transaction_mart_dag.py
│   ├── db
│   ├── logs
│   │   ├── dag_id=customer_mart_dag
│   │   ├── dag_id=customer_withdrawal_reached_mart_dag
│   │   ├── dag_id=dbt_pipeline
│   │   ├── dag_id=master_orchestrator_dag
│   │   ├── dag_id=staging_customers_dag
│   │   ├── dag_id=staging_eod_balance_dag
│   │   ├── dag_id=staging_transactions_dag
│   │   ├── dag_id=transaction_mart_dag
│   │   ├── dag_processor_manager
│   │   └── scheduler
│   └── plugins
├── dataviz
│   ├── advisor_report.pbit
│   ├── advisor_report.pbix
│   ├── business_dashboard.pbit
│   └── business_dashboard.pbix
├── dbs_models
│   ├── banking_db
│   │   ├── CREATION_SCRIPT.sql
│   │   └── TRUNCATE_SCRIPT.sql
│   ├── bigquery_bronze
│   │   └── CREATION_SCRIPT.sql
│   ├── bigquery_gold
│   │   ├── CREATION_SCRIPT.sql
│   │   └── INSERT_FAKE_DATA.sql
│   ├── bigquery_silver
│   │   └── CREATION_SCRIPT.sql
│   └── transaction-api
│       └── TRANSACTION_MODEL.json
├── ingestion
│   ├── abctl-v0.30.1-windows-amd64
│   │   ├── LICENSE
│   │   ├── README.md
│   │   └── abctl.exe
│   ├── airbyte_yorbank_db_banking_source_connector.json
│   ├── airbyte_yorbank_db_erp_source_connector copy.json
│   └── kafka
│       ├── api_connector.json
│       └── big_query_connector.json
├── media
├── requirements.txt
├── simulator
│   ├── app.py
│   ├── customer.json
│   ├── data_faker.py
│   ├── get_db_connection.py
│   ├── gold_fake_data_for_powerbi.py
│   └── insert.py
└── yorb_dbt
    ├── .gitignore
    ├── .user.yml
    ├── README.md
    ├── analyses
    │   └── .gitkeep
    ├── dbt_packages
    │   ├── codegen
    │   └── dbt_utils
    ├── dbt_project.yml
    ├── logs
    │   └── dbt.log
    ├── macros
    │   ├── .gitkeep
    │   └── generate_schema_name.sql
    ├── models
    │   ├── gold
    │   ├── schema.yml
    │   └── silver
    ├── package-lock.yml
    ├── packages.yml
    ├── profiles.yml
    ├── seeds
    │   └── .gitkeep
    ├── snapshots
    │   └── .gitkeep
    ├── target
    └── tests
        ├── .gitkeep
        └── transaction_count.sql
```

