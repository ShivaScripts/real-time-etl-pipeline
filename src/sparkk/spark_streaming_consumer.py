import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, window, avg, max as spark_max,
    when, expr
)
from pyspark.sql.types import (
    StructType, StringType, IntegerType, DoubleType
)

BASE_DIR       = "/Users/Shivam/Documents/real_time_data_pipeline"
RAW_OUTPUT     = os.path.join(BASE_DIR, "data/processed_logs")
CHECKPOINT     = os.path.join(BASE_DIR, "data/spark_checkpoints")

# Ensure directories exist
os.makedirs(RAW_OUTPUT, exist_ok=True)
os.makedirs(CHECKPOINT, exist_ok=True)

schema = StructType() \
    .add("event_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("level", StringType()) \
    .add("service", StringType()) \
    .add("message", StringType()) \
    .add("user_id", StringType()) \
    .add("response_time_ms", IntegerType()) \
    .add("error_code", IntegerType()) \
    .add("payload_size_kb", DoubleType())

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingConsumer") \
    .master("local[*]") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "logs") \
    .option("startingOffsets", "latest") \
    .load()

logs = raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json("json_str", schema).alias("data")) \
    .select("data.*") \
    .withColumn("ts", expr("timestamp"))

clean = logs.filter(
    col("event_id").isNotNull() &
    col("timestamp").isNotNull() &
    col("service").isNotNull()
)

enriched = clean.withColumn(
    "is_slow",
    when(col("response_time_ms") > 1000, True).otherwise(False)
)

metrics = enriched \
    .withColumn("event_time", expr("CAST(timestamp AS timestamp)")) \
    .withWatermark("event_time", "2 minutes") \
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("service")
    ) \
    .agg(
        avg("response_time_ms").alias("avg_resp_ms"),
        spark_max("response_time_ms").alias("max_resp_ms"),
        expr("sum(case when is_slow then 1 else 0 end)").alias("slow_count"),
        expr("count(*)").alias("total_count")
    )

# Sink 1: cleaned events → JSON
clean_query = enriched.writeStream \
    .format("json") \
    .option("path", RAW_OUTPUT + "/cleaned") \
    .option("checkpointLocation", CHECKPOINT + "/cleaned") \
    .outputMode("append") \
    .trigger(once=True) \
    .start()

# Sink 2: windowed metrics → Parquet (append mode)
metrics_query = metrics.writeStream \
    .format("parquet") \
    .option("path", RAW_OUTPUT + "/metrics") \
    .option("checkpointLocation", CHECKPOINT + "/metrics") \
    .outputMode("append") \
    .trigger(once=True) \
    .start()

# Wait for both to finish
clean_query.awaitTermination(timeout=600)
metrics_query.awaitTermination(timeout=600)
