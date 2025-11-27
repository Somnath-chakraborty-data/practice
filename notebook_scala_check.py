# Scala Compatibility Check for PySpark Notebook
# Add this cell to your notebook to check Scala compatibility

from pyspark.sql import SparkSession
import re

# Initialize SparkSession (reuse if already exists)
spark = SparkSession.builder \
    .appName("ScalaCompatibilityCheck") \
    .getOrCreate()

# Get versions
spark_version = spark.version
scala_version_str = spark.sparkContext._jvm.scala.util.Properties.versionString()
hadoop_version = spark.sparkContext._gateway.jvm.org.apache.hadoop.util.VersionInfo.getVersion()
java_version = spark.sparkContext._gateway.jvm.System.getProperty("java.version")

# Parse Scala version
match = re.search(r'(\d+\.\d+\.\d+)', str(scala_version_str))
if match:
    full_scala_version = match.group(1)
    scala_binary_version = '.'.join(full_scala_version.split('.')[:2])
else:
    scala_binary_version = "unknown"

# Display results
print("="*60)
print("PYSPARK ENVIRONMENT VERSIONS")
print("="*60)
print(f"Spark Version:   {spark_version}")
print(f"Scala Version:   {scala_binary_version} (Full: {full_scala_version})")
print(f"Hadoop Version:  {hadoop_version}")
print(f"Java Version:    {java_version}")
print("="*60)

# Compatibility matrix
compatibility_matrix = {
    "4.0": {"scala": "2.13", "hadoop": "3.4+", "java": "17 or 21"},
    "3.5": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
    "3.4": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
    "3.3": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
}

spark_major_minor = '.'.join(spark_version.split('.')[:2])

if spark_major_minor in compatibility_matrix:
    expected = compatibility_matrix[spark_major_minor]
    print(f"\nFor Spark {spark_major_minor}, recommended versions:")
    print(f"  • Scala:  {expected['scala']}")
    print(f"  • Hadoop: {expected['hadoop']}")
    print(f"  • Java:   {expected['java']}")
    
    # Check compatibility
    if scala_binary_version in expected['scala']:
        print(f"\n✅ Your Scala {scala_binary_version} is COMPATIBLE with Spark {spark_version}")
    else:
        print(f"\n⚠️  Your Scala {scala_binary_version} may not be optimal for Spark {spark_version}")
        print(f"   Recommended: {expected['scala']}")
else:
    print(f"\nNote: Compatibility info not available for Spark {spark_major_minor}")

print("="*60)
