from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="customer_analytics_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    ingestion = BashOperator(
        task_id="data_ingestion",
        bash_command="python /opt/airflow/src/ingestion.py"
    )

    dbt_run = BashOperator(
        task_id="dbt_transform",
        bash_command="cd /opt/customer_analytics_dbt && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/customer_analytics_dbt && dbt test"
    )

    ingestion >> dbt_run >> dbt_test