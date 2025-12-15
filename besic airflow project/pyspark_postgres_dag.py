from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.utils.dates import days_ago

# --- Define Paths and Variables ---
# Assumes Airflow Home is the directory containing dags/, jobs/, and jars/
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/home/somnath/airflow_project/airflow_home') 

# Paths to the script and JAR (relative to AIRFLOW_HOME or absolute)
SPARK_JOB_PATH = f"{AIRFLOW_HOME}/jobs/pyspark_job.py"
JAR_PATH = f"{AIRFLOW_HOME}/jars/postgresql.jar"

# The command that spark-submit will run.
# Note: We must pass the DB password via the environment variable for security.
SPARK_SUBMIT_COMMAND = f"""
/opt/spark/bin/spark-submit \
    --master local[*] \
    --jars {JAR_PATH} \
    {SPARK_JOB_PATH} 
"""
# Note: Ensure /opt/spark/bin/spark-submit is the correct path for your installation.

default_args = {
    'owner': 'somnath',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

with DAG(
    dag_id='pyspark_postgres_etl_pipeline',
    default_args=default_args,
    description='A DAG to run a PySpark job to load data into PostgreSQL',
    schedule_interval=None, # Run manually
    tags=['pyspark', 'postgres', 'etl'],
    catchup=False
) as dag:
    
    # Define the task to execute the spark-submit command
    run_spark_job = BashOperator(
        task_id='run_pyspark_etl',
        bash_command=SPARK_SUBMIT_COMMAND,
        # NOTE: Pass the DB password securely as an environment variable
        # This assumes you have the DB password stored in an Airflow connection 
        # or loaded into the worker's environment.
        env={'PG_PASS': '1110897'}, # Replace with your actual password or a secure reference
        dag=dag,
    )

    # In this simple DAG, the job just runs once
    # run_spark_job