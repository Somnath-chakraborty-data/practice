from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Hello PySpark") \
    .master("local[*]") \
    .getOrCreate()

# Create simple DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])

print("✅ PySpark is working!")
df.show()

spark.stop()
