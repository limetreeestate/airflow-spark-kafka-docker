import os
from pyspark.sql import SparkSession, DataFrame
from main.spark.Consumer import Consumer
from main.spark.SparkDBConnection import SparkDBConnection

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Spark streaming Kafka consumer") \
        .getOrCreate()

    KAFKA_BROKER: str = os.environ["KAFKA_BROKER"]
    MYSQL_URL: str = os.environ["MYSQL_URL"]
    MYSQL_DB: str = os.environ["MYSQL_DB"]
    MYSQL_RAW_TABLE: str = os.environ["MYSQL_RAW_TABLE"]
    MYSQL_UNIQUE_STAGE_TABLE: str = os.environ["MYSQL_UNIQUE_STAGE_TABLE"]
    MYSQL_DUPLICATE_STAGE_TABLE: str = os.environ["MYSQL_DUPLICATE_STAGE_TABLE"]
    MYSQL_USER: str = os.environ["MYSQL_USER"]
    MYSQL_PASSWORD: str = os.environ["MYSQL_PASSWORD"]

    # Read data from Kafka topic
    consumer: Consumer = Consumer(spark, KAFKA_BROKER)
    rawData: DataFrame = consumer.consumeAll("purchases")

    # Save raw data to mysql
    dbConenction: SparkDBConnection = SparkDBConnection(
        MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD)
    dbConenction.write(rawData, MYSQL_DB, MYSQL_RAW_TABLE)

    # Select data entries
    uniqueEntries: DataFrame = rawData.distinct()

    # Save unique entries to mysql
    dbConenction.write(uniqueEntries, MYSQL_DB, MYSQL_UNIQUE_STAGE_TABLE)

    # Filter dulicate entries
    currentDuplicates: DataFrame = rawData.exceptAll(uniqueEntries)

    # Load existing duplicate entries
    existingDuplicates: DataFrame = dbConenction.read(spark, MYSQL_DB, MYSQL_DUPLICATE_STAGE_TABLE)

    # Update duplicate count
    cols = ["uid","address1","city","postcode","decision"]
    allDuplicates: DataFrame = existingDuplicates.select(cols).union(currentDuplicates)
    countDuplicates: DataFrame = allDuplicates.groupBy(cols).count()

    # Write back to mysql
    dbConenction.write(countDuplicates, MYSQL_DB, MYSQL_DUPLICATE_STAGE_TABLE, "overwrite")

    spark.stop()
