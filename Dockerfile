FROM apache/airflow:2.9.3

USER airflow
RUN pip install dbt-core dbt-bigquery
