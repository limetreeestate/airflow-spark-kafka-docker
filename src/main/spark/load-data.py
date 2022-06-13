import os
from sys import argv
from h11 import Data
from pyspark.sql import SparkSession, DataFrame
from main.spark.DataConsumer import DataConsumer
from main.spark.SparkDBConnection import SparkDBConnection

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Spark data extractor") \
        .getOrCreate()

    [KAFKA_BROKER, KAFKA_TOPIC, MYSQL_URL, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_RAW_TABLE,
        MYSQL_UNIQUE_TABLE, MYSQL_DUPLICATE_TABLE, MYSQL_DECISION_TABLE] = argv[1:]

    # Read data from Kafka topic
    consumer: DataConsumer = DataConsumer(spark, KAFKA_BROKER)
    rawData: DataFrame = consumer.consumeAll(KAFKA_TOPIC)

    # Save raw data to mysql
    dbConenction: SparkDBConnection = SparkDBConnection(
        MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD)
    dbConenction.write(rawData, MYSQL_DB, MYSQL_RAW_TABLE)

    # Select data entries
    uniqueEntries: DataFrame = rawData.distinct()

    # Fetch stage 2 table
    stage2: DataFrame = dbConenction.read(
        spark, MYSQL_DB, MYSQL_DUPLICATE_TABLE)

    totalUniqueEntries: DataFrame = stage2.union(uniqueEntries).distinct()

    # Save unique entries to mysql
    dbConenction.write(totalUniqueEntries, MYSQL_DB,
                       MYSQL_UNIQUE_TABLE, "overwrite")

    # Load existing duplicate entries
    existingDuplicates: DataFrame = dbConenction.read(
        spark, MYSQL_DB, MYSQL_DUPLICATE_TABLE)

    # Update duplicate count
    cols = ["uid", "address1", "city", "postcode", "decision"]
    allDuplicates: DataFrame = existingDuplicates.select(cols).union(rawData)
    countDuplicates: DataFrame = allDuplicates.groupBy(
        "uid").count().withColumnRenamed("count", "duplicateCount")

    # Write back to mysql
    dbConenction.write(countDuplicates, MYSQL_DB,
                       MYSQL_DUPLICATE_TABLE, "overwrite")

    # Write decisions to mysql
    totalUniqueEntries["isGoodDecision"] = totalUniqueEntries["decision"] == "A"
    decisions: DataFrame = countDuplicates.select(
        ["id", "decision", "isGoodDecision"])
    dbConenction.write(decisions, MYSQL_DB, MYSQL_DECISION_TABLE, "overwrite")

    spark.stop()
