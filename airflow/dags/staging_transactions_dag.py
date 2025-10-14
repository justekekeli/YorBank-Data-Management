from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries":0,
    #"retry_delay": timedelta(minutes=2),
}

with DAG(
    "staging_transactions_dag",
    default_args=default_args,
    description="Run dbt staging_transactions model every 15min",
    #schedule_interval="*/15 * * * *",  # every 15 min
    schedule_interval="@daily",
    start_date=datetime(2025, 10, 11),
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="run_staging_transactions",
        bash_command=f"cd {DBT_DIR} && dbt run --select silver.staging_transactions --vars '{{reference_date: \"{{{{ ds }}}}\"}}'",
    )
    dbt_test = BashOperator(
        task_id="dbt_test_staging_transactions",
        bash_command=f"cd {DBT_DIR} && dbt test --select silver.staging_transactions",
    )

    dbt_run >> dbt_test
