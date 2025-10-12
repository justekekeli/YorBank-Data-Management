from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

DBT_DIR = "/opt/airflow/dbt_project"

default_args = {
    "owner": "airflow",
    "email": ["data-team@example.com"],
    "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="customer_overdraft_mart_dag",
    description="Run customer_overdraft_mart monthly after staging_customers",
    start_date=datetime(2025, 10, 1),
    schedule_interval="0 0 1 * *", 
    catchup=False,
) as dag:

    wait_for_customers = ExternalTaskSensor(
        task_id="wait_for_staging_customers",
        external_dag_id="staging_customers_dag",
        external_task_id="dbt_test_staging_customers",
        timeout=600,
    )

    def last_day_of_month(date):
        next_month = date.replace(day=28) + timedelta(days=4)
        return (next_month - timedelta(days=next_month.day)).strftime("%Y-%m-%d")

    def build_vars(**context):
        exec_date = context["ds"]
        ref = datetime.strptime(exec_date, "%Y-%m-%d")
        m1 = last_day_of_month(ref - relativedelta(months=1))
        m2 = last_day_of_month(ref - relativedelta(months=2))
        m3 = last_day_of_month(ref - relativedelta(months=3))
        return f"--vars '{{overdraft_first_month: \"{m1}\", overdraft_second_month: \"{m2}\", overdraft_third_month: \"{m3}\"}}'"

    build_vars = PythonOperator(
        task_id="build_dbt_vars",
        python_callable=build_vars,
    )
    dbt_run = BashOperator(
        task_id="dbt_run_customer_overdraft_mart",
        bash_command=(
            f"cd {DBT_DIR} && dbt run --select gold.customer_overdraft_mart {{ ti.xcom_pull(task_ids='build_dbt_vars') }}"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test_customer_overdraft_mart",
        bash_command=f"cd {DBT_DIR} && dbt test --select gold.customer_overdraft_mart",
    )


    wait_for_customers >> build_vars >> dbt_run >> dbt_test
