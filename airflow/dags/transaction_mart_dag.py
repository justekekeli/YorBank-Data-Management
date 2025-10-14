from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries": 0
}

with DAG(
    dag_id="transaction_mart_dag",
    description="Run transaction_mart daily after staging_transactions",
    start_date=datetime(2025, 10, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run_transaction_mart",
        bash_command=(
            f"cd {DBT_DIR} && dbt run --select gold.transaction_mart --vars '{{reference_date: \"{{{{ ds }}}}\"}}'"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test_transaction_mart",
        bash_command=f"cd {DBT_DIR} && dbt test --select gold.transaction_mart",
    )

    dbt_run >> dbt_test