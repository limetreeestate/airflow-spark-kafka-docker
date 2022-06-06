import pyspark
from pyspark.sql import SparkSession, DataFrame


class SparkDBConnection:
    def __init__(self, url: str, user: str, pw: str):
        self.__url = url
        self.__user = user
        self.__pw = pw

    def write(self, data: DataFrame, db: str, table: str, mode=""):
        writeStream = data.write \
            .format("jdbc") \
            .option("url", f"jdbc:mysql://{self.__url}/{db}&useUnicode=true&characterEncoding=UTF-8&useSSL=false") \
            .option("driver", "com.mysql.jdbc.Driver") \
            .option("dbtable", table) \
            .option("user", self.__user) \
            .option("password", self.__pw)
        
        if mode == "overwrite":
            writeStream = writeStream.option("truncate", "true").mode("overwrite")
        
        writeStream.save()

    def read(self, spark: SparkSession, db: str, table: str) -> DataFrame:
        return spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:mysql://{self.__url}/{db}&useUnicode=true&characterEncoding=UTF-8&useSSL=false") \
            .option("dbtable", f"{db}.{table}") \
            .option("user", self.__user) \
            .option("password", self.__pw) \
            .load()
