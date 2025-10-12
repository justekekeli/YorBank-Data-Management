from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="customer_mart_dag",
    description="Run customer_mart daily after staging_customers",
    start_date=datetime(2025, 10, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    wait_for_customers = ExternalTaskSensor(
        task_id="wait_for_staging_customers",
        external_dag_id="staging_customers_dag",
        external_task_id="dbt_test_staging_customers",
        timeout=600,
    )

    dbt_run = BashOperator(
        task_id="dbt_run_customer_mart",
        bash_command=(
            f"cd {DBT_DIR} && dbt run --select gold.customer_mart --vars '{{reference_date: \"{{{{ ds }}}}\"}}'"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test_customer_mart",
        bash_command=f"cd {DBT_DIR} && dbt test --select gold.customer_mart",
    )

    wait_for_customers >> dbt_run >> dbt_test
