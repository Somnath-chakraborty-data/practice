import os

# Set environment variables
os.environ['JAVA_HOME'] = 'C:\\Program Files\\Java\\jdk-17'
os.environ['SPARK_HOME'] = 'C:\\spark\\spark-4.0.1-bin-hadoop3'
os.environ['HADOOP_HOME'] = 'C:\\spark\\spark-4.0.1-bin-hadoop3'
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Create test DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.show()

print("✓ Spark is working with DataFrames!")
spark.stop()