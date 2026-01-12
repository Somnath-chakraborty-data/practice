from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def extract_and_upload():
    # Connect to Local Postgres
    pg_hook = PostgresHook(postgres_conn_id='postgres_local')
    df = pg_hook.get_pandas_df("SELECT * FROM raw_sales")
    
    # Save to local CSV temporarily
    local_path = "/tmp/sales_data.csv"
    df.to_csv(local_path, index=False)
    
    # Note: In a production scenario, you'd use boto3 or Databricks CLI 
    # to move the file to DBFS. For this project, we assume the file is accessible.
    print(f"Data extracted to {local_path}")

with DAG(
    dag_id='postgres_to_databricks_flow',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_from_postgres',
        python_callable=extract_and_upload
    )

    # Trigger the Databricks Notebook (Job ID found in Databricks Job UI)
    transform_task = DatabricksRunNowOperator(
        task_id='transform_in_databricks',
        databricks_conn_id='databricks_default',
        job_id=123456 # Replace with your Job ID
    )

    extract_task >> transform_task