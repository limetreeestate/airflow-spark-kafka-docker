import os
from sys import argv
from pyspark.sql import SparkSession, DataFrame
from main.spark.DataConsumer import DataConsumer

spark = SparkSession \
        .builder \
        .appName("Spark streaming Kafka consumer") \
        .getOrCreate()

consumer: DataConsumer = DataConsumer(spark, 'localhost:9092')
rawData: DataFrame = consumer.consumeAll("purchases")
rawData.show(10)