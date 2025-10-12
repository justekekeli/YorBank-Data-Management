from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python  import BranchPythonOperator
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

default_args = {"owner": "airflow", 
                "retries": 0}

with DAG(
    "master_orchestrator_dag",
    description="Orchestrates all dbt silver models",
    start_date=datetime(2025, 10, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    from airflow.operators.python import ShortCircuitOperator

    ################################ SLIVER MODELS ##########################
    check_profiles_run = ShortCircuitOperator(
        task_id="check_profiles_run",
        python_callable=lambda **context: not has_profiles_run(**context),
    )

    trigger_profiles_once = TriggerDagRunOperator(
        task_id="trigger_profiles_once",
        trigger_dag_id="staging_profiles_dag",
        wait_for_completion=True,
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

    ################################ GOLD MODELS ##########################

    trigger_customer_mart = TriggerDagRunOperator(
        task_id="trigger_customer_mart",
        trigger_dag_id="customer_mart_dag",
        wait_for_completion=True,
    )

    trigger_transaction_mart = TriggerDagRunOperator(
        task_id="trigger_transaction_mart",
        trigger_dag_id="transaction_mart_dag",
        wait_for_completion=True,
    )

    trigger_customer_withdrawal_mart = TriggerDagRunOperator(
        task_id="trigger_customer_withdrawal_reached_mart",
        trigger_dag_id="customer_withdrawal_reached_mart_dag",
        wait_for_completion=True,
    )


    def is_first_of_month(**context):
        return "trigger_customer_overdraft_mart" if datetime.today().day == 1 else "skip_customer_overdraft_mart"

    check_overdraft = BranchPythonOperator(
        task_id="check_first_day_of_month",
        python_callable=is_first_of_month,
    )

    trigger_customer_overdraft_mart = TriggerDagRunOperator(
        task_id="trigger_customer_overdraft_mart",
        trigger_dag_id="customer_overdraft_mart_dag",
        wait_for_completion=True,
    )
    skip_customer_overdraft_mart = EmptyOperator(task_id="skip_customer_overdraft_mart")

    ################################ ORCHESTRATION CHAIN ##########################

    check_profiles_run >> trigger_profiles_once
    [trigger_profiles_once, trigger_transactions] >> trigger_eod_balance >> trigger_customers
    trigger_customers >> [trigger_customer_mart, trigger_customer_overdraft_mart, trigger_customer_withdrawal_mart]
    trigger_transactions >> trigger_transaction_mart
    check_overdraft >> [trigger_customer_overdraft_mart, skip_customer_overdraft_mart]

