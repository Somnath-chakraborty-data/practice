from pyspark.sql import SparkSession

def check_spark_scala_compatibility():
    """
    Check Spark, Scala, Hadoop versions and their compatibility.
    """
    spark = None
    try:
        # Initialize SparkSession
        spark = SparkSession.builder \
            .appName("ScalaCompatibilityCheck") \
            .getOrCreate()

        # Get Spark Version
        spark_version = spark.version
        print(f"[OK] Spark Version: {spark_version}")

        # Get Scala Version (multiple methods for compatibility)
        try:
            scala_version = spark.sparkContext._jvm.scala.util.Properties.versionString()
        except:
            scala_version = "Unable to retrieve full version string"
        
        # Extract Scala binary version from the version string
        scala_binary_version = "unknown"
        if "version" in str(scala_version).lower():
            # Parse from version string like "version 2.13.16"
            import re
            match = re.search(r'(\d+\.\d+\.\d+)', str(scala_version))
            if match:
                full_version = match.group(1)
                scala_binary_version = '.'.join(full_version.split('.')[:2])
        
        print(f"[OK] Scala Version: {scala_binary_version}")
        print(f"     Full Scala Info: {scala_version}")

        # Get Hadoop Version
        hadoop_version = spark.sparkContext._gateway.jvm.org.apache.hadoop.util.VersionInfo.getVersion()
        print(f"[OK] Hadoop Version: {hadoop_version}")

        # Get Java Version
        java_version = spark.sparkContext._gateway.jvm.System.getProperty("java.version")
        print(f"[OK] Java Version: {java_version}")

        print("\n" + "="*60)
        print("COMPATIBILITY CHECK")
        print("="*60)

        # Check compatibility based on Spark version
        spark_major_minor = '.'.join(spark_version.split('.')[:2])
        
        compatibility_matrix = {
            "4.0": {"scala": "2.13", "hadoop": "3.4+", "java": "17 or 21"},
            "3.5": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
            "3.4": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
            "3.3": {"scala": "2.12 or 2.13", "hadoop": "3.3+", "java": "8, 11, or 17"},
            "3.2": {"scala": "2.12 or 2.13", "hadoop": "3.2+", "java": "8 or 11"},
            "3.1": {"scala": "2.12", "hadoop": "3.2+", "java": "8 or 11"},
            "3.0": {"scala": "2.12", "hadoop": "2.7+ or 3.2+", "java": "8 or 11"},
        }

        if spark_major_minor in compatibility_matrix:
            expected = compatibility_matrix[spark_major_minor]
            print(f"\nFor Spark {spark_major_minor}, the recommended versions are:")
            print(f"  • Scala: {expected['scala']}")
            print(f"  • Hadoop: {expected['hadoop']}")
            print(f"  • Java: {expected['java']}")
            
            # Check Scala compatibility
            scala_major_minor = '.'.join(scala_binary_version.split('.')[:2])
            print(f"\n[CHECK] Your Scala version ({scala_major_minor}) is ", end="")
            if scala_major_minor in expected['scala']:
                print("COMPATIBLE")
            else:
                print(f"NOT in the recommended range!")
                print(f"  Consider using Scala {expected['scala']}")
        else:
            print(f"\nNote: Compatibility information not available for Spark {spark_major_minor}")
            print("Please check the official Apache Spark documentation.")

        print("\n" + "="*60)
        print("For detailed compatibility information, visit:")
        print("https://spark.apache.org/docs/latest/")
        print("="*60)

    except Exception as e:
        print(f"[ERROR] Error checking versions: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if spark:
            spark.stop()

if __name__ == "__main__":
    check_spark_scala_compatibility()
