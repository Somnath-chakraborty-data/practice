from pyspark.sql import SparkSession

def check_versions():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("Check Spark and Hadoop Versions") \
        .getOrCreate()

    try:
        # Get Spark Version
        spark_version = spark.version
        print(f"Spark Version: {spark_version}")

        # Get Hadoop Version
        # Accessing Hadoop version via the JVM gateway
        hadoop_version = spark.sparkContext._gateway.jvm.org.apache.hadoop.util.VersionInfo.getVersion()
        print(f"Hadoop Version: {hadoop_version}")

    except Exception as e:
        print(f"Error checking versions: {str(e)}")
    
    finally:
        spark.stop()

if __name__ == "__main__":
    check_versions()
