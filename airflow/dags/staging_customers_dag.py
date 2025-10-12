from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "staging_customers_dag",
    default_args=default_args,
    description="Run dbt staging_customers after staging_eod_balance",
    schedule_interval="@daily",
    start_date=datetime(2025, 10, 11),
    catchup=False,
) as dag:

    wait_for_eod_balance = ExternalTaskSensor(
        task_id="wait_for_eod_balance",
        external_dag_id="staging_eod_balance_dag",
        external_task_id="run_staging_eod_balance",
        poke_interval=300,  # check every 5min
        timeout=3600,  # 1 hour max wait
        mode="poke",
    )

    dbt_run = BashOperator(
        task_id="run_staging_customers",
        bash_command=f"cd {DBT_DIR} && dbt run --select silver.staging_customers --vars '{{reference_date: \"{{{{ ds }}}}\"}}'",
    )

    dbt_test = BashOperator(
        task_id="dbt_test_staging_eod_balance",
        bash_command=f"cd {DBT_DIR} && dbt test --select silver.staging_eod_balance",
    )

    wait_for_eod_balance >> dbt_run >> dbt_test
