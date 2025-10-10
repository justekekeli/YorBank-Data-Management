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

COMING SOON

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

## 📈💰📊 PowerBI reports

### Business Dashboard

![image](media/yorbank_dashboard.png)

### Advisor Report

![image](media/advisor_report_page_1.png)

![image](media/advisor_report_page_2.png)

## 𖣂 Folder Strcutures
```
├── .gitignore
├── requirements.txt
├── README.md
├── dbs_models
│   ├── banking_db
│   │   ├── CREATION_SCRIPT.sql
│   │   └── TRUNCATE_SCRIPT.sql
│   ├── bigquery_bronze
│   │   └── CREATION_SCRIPT.sql
│   ├── bigquery_gold
│   │   └── CREATION_SCRIPT.sql
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
│   └── kafka
│       ├── api_connector.json
│       └── big_query_connector.json
├── media
│   ├── airbyte_data_ingestion.png
│   ├── bronze_dataset.png
│   ├── kafka_pipeline.png
│   ├── kafka_topic.png
│   ├── yorbank_bigquery_dw.png
│   └── yorbank_postgres_db.png
├── orchestration
├── simulator
│   ├── app.py
│   ├── data_faker.py
│   ├── get_db_connection.py
│   └── insert.py
└── transformation
    ├── logs
    │   └── dbt.log
    └── yorb_dbt
        ├── .gitignore
        ├── README.md
        ├── analyses
        │   └── .gitkeep
        ├── dbt_packages
        ├── dbt_project.yml
        ├── logs
        │   └── dbt.log
        ├── macros
        │   ├── .gitkeep
        │   └── generate_schema_name.sql
        ├── models
        │   ├── gold
        │   │   ├── customer_mart.sql
        │   │   ├── customer_overdraft_mart.sql
        │   │   ├── customer_withdrawal_reached_mart.sql
        │   │   ├── schema.yml
        │   │   └── transaction_mart.sql
        │   ├── schema.yml
        │   └── silver
        │       ├── schema.yml
        │       ├── staging_customers.sql
        │       ├── staging_eod_balance.sql
        │       ├── staging_profiles.sql
        │       └── staging_transactions.sql
        ├── package-lock.yml
        ├── packages.yml
        ├── seeds
        │   └── .gitkeep
        ├── snapshots
        │   └── .gitkeep
        ├── target
        └── tests
            └── .gitkeep
```




