from pyspark.sql import SparkSession
import os

# Set Java home
os.environ['JAVA_HOME'] = 'C:\\Program Files\\Java\\jdk-17'

# Create Spark session
spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

print("✓ Spark is working!")
print(f"Spark Version: {spark.version}")
spark.stop()