from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pymongo import MongoClient

# Function to insert data into MongoDB
def insert_mongo_data():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.testdb
    collection = db.testcollection
    collection.insert_one({
        "name": "Airflow DAG Test",
        "status": "success",
        "timestamp": datetime.now()
    })
    print("Document inserted successfully!")

# Function to read data from MongoDB
def read_mongo_data():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client.testdb
    collection = db.testcollection
    for doc in collection.find():
        print(doc)

# Define the DAG
with DAG(
    "mongo_test_dag",
    start_date=datetime(2025, 9, 7),
    schedule_interval=None,  # Run manually
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

    insert_task >> read_task  # Insert first, then read
