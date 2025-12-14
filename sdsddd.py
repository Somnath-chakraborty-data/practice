from pyspark.sql import SparkSession

# Step 1: Create a Spark session
spark = SparkSession.builder.appName("SimpleTest").getOrCreate()

# Step 2: Create some sample data
data = [("Somnath", 27), ("Nandini", 25), ("Noorjahan", 26)]

# Step 3: Define column names
columns = ["Name", "Age"]

# Step 4: Create DataFrame
df = spark.createDataFrame(data, columns)

# Step 5: Show DataFrame
df.show()

# Step 6: Print Schema
df.printSchema()