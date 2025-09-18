from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pymongo import MongoClient

def insert_mongo_data():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.testdb
    collection = db.testcollection
    collection.insert_one({
        "name": "Scheduled DAG Test",
        "status": "success",
        "timestamp": datetime.now()
    })
    print("Scheduled document inserted!")

def read_mongo_data():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.testdb
    collection = db.testcollection
    for doc in collection.find():
        print(doc)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "scheduled_mongo_dag",
    default_args=default_args,
    start_date=datetime(2025, 9, 7),
    schedule_interval="0 9 * * *",  # Every day at 9 AM
    catchup=False
) as dag:

    insert_task = PythonOperator(
        task_id="insert_task",
        python_callable=insert_mongo_data
    )

    read_task = PythonOperator(
        task_id="read_task",
        python_callable=read_mongo_data
    )

    insert_task >> read_task
