from pyspark.sql import SparkSession
spark = (SparkSession.builder.appName("QualityGateEnvironmentTest").master("local[1]").getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
df = spark.createDataFrame([(1, "Alice"), (2, "bB")], ["id", "name"])
df.show()
print(spark.version)
print("Row Count:", df.count())
spark.stop()
