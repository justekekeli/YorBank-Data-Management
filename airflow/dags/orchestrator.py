from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import DagRun
from airflow.utils.session import provide_session
from datetime import datetime

@provide_session
def has_profiles_run(session=None, **context):
    """Return True if staging_profiles_dag has already succeeded at least once."""
    dr = (
        session.query(DagRun)
        .filter(DagRun.dag_id == "staging_profiles_dag")
        .filter(DagRun.state == "success")
        .first()
    )
    return bool(dr)

default_args = {"owner": "airflow", "retries": 0}

with DAG(
    "master_orchestrator_dag",
    description="Orchestrates all dbt silver models",
    start_date=datetime(2025, 10, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    from airflow.operators.python import ShortCircuitOperator

    check_profiles_run = ShortCircuitOperator(
        task_id="check_profiles_run",
        python_callable=lambda **context: not has_profiles_run(**context),
    )

    trigger_profiles_once = TriggerDagRunOperator(
        task_id="trigger_profiles_once",
        trigger_dag_id="staging_profiles_dag",
        wait_for_completion=True,
        poke_interval=300,
    )
    trigger_transactions = TriggerDagRunOperator(
        task_id="trigger_transactions",
        trigger_dag_id="staging_transactions_dag",
        wait_for_completion=False, 
    )
    trigger_eod_balance = TriggerDagRunOperator(
        task_id="trigger_eod_balance",
        trigger_dag_id="staging_eod_balance_dag",
        wait_for_completion=True,
    )

    trigger_customers = TriggerDagRunOperator(
        task_id="trigger_customers",
        trigger_dag_id="staging_customers_dag",
        wait_for_completion=True,
    )

    check_profiles_run >> trigger_profiles_once >> [trigger_transactions, trigger_eod_balance] >> trigger_customers

