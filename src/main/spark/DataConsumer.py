from pyspark.sql import SparkSession, DataFrame


class DataConsumer:
    def __init__(self, spark: SparkSession, url: str):
        self.__spark = spark
        self.__url = url

    def consumeAll(self, topic: str) -> DataFrame:
        return self.__spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.__url) \
            .option("subscribe", topic) \
            .option("startingOffsets", "earliest") \
            .option("endingOffsets", "latest") \
            .load()
