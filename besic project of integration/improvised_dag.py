import os
from airflow import DAG
from airflow.models import Variable # Airflow's built-in Secret store

# Method 1: Get from OS Environment
db_token = os.getenv('DATABRICKS_TOKEN')

# Method 2: Get from Airflow Variables (Set in UI under Admin > Variables)
# Best for non-sensitive config like "environment_name"
target_schema = Variable.get("sales_schema_name", default_var="dev")

with DAG(...) as dag:
    # Use the connection ID only - Airflow handles the rest
    task = DatabricksRunNowOperator(
        task_id='transform',
        databricks_conn_id='databricks_default', 
        job_id=os.getenv('DATABRICKS_JOB_ID') 
    )