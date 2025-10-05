```
├── .gitignore
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
        ├── requirements.txt
        ├── seeds
        │   └── .gitkeep
        ├── snapshots
        │   └── .gitkeep
        ├── target
        └── tests
            └── .gitkeep
```
