import os
from sys import argv
from pyspark.sql import SparkSession, DataFrame
from main.spark.DataConsumer import DataConsumer
from main.spark.SparkDBConnection import SparkDBConnection

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Spark data extractor") \
        .getOrCreate()

    [KAFKA_BROKER, MYSQL_URL, MYSQL_DB, MYSQL_RAW_TABLE, MYSQL_UNIQUE_STAGE_TABLE,
        MYSQL_DUPLICATE_STAGE_TABLE, MYSQL_DECISION_TABLE, MYSQL_DECISION_TABLE, MYSQL_USER, MYSQL_PASSWORD] = argv[1:]

    dbConenction: SparkDBConnection = SparkDBConnection(
        MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD)

    # Read stage2 from mysql
    stage2: DataFrame = dbConenction.read(
        spark, MYSQL_DB, MYSQL_DUPLICATE_STAGE_TABLE)

    # Read decision table from mysql
    decision: DataFrame = dbConenction.read(
        spark, MYSQL_DB, MYSQL_DECISION_TABLE)

    stage3: DataFrame = stage2.join(decision, on="id").select(
        stage2["id"], stage2["address1"], stage2["city"], stage2["postcode"], stage2["decision"], decision["isGoodDecision"])

    dbConenction.write(stage3, MYSQL_DB, )
