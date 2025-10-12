from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries": 0
}


with DAG(
    dag_id="staging_profiles_dag",
    description="Run dbt staging_profiles model only once",
    start_date=datetime(2025, 10, 11),
    schedule_interval=None, 
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="run_staging_profiles",
        bash_command=f"cd {DBT_DIR} && dbt run --select silver.staging_profiles",
    )

    dbt_test = BashOperator(
        task_id="dbt_test_staging_profiles",
        bash_command=f"cd {DBT_DIR} && dbt test --select silver.staging_profiles",
    )

    dbt_run >> dbt_test
