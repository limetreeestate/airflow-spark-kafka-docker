from datetime import datetime, timedelta
import os
import pendulum
from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.models import Variable

KAFKA_BROKER: str = os.environ["KAFKA_BROKER"]
KAFKA_TOPIC: str = os.environ["KAFKA_TOPIC"]
MYSQL_URL: str = os.environ["MYSQL_URL"]
MYSQL_DB: str = os.environ["MYSQL_DB"]
MYSQL_USER: str = os.environ["MYSQL_USER"]
MYSQL_PASSWORD: str = os.environ["MYSQL_PASSWORD"]
MYSQL_RAW_TABLE: str = os.environ["MYSQL_RAW_TABLE"]
MYSQL_UNIQUE_TABLE: str = os.environ["MYSQL_UNIQUE_TABLE"]
MYSQL_DUPLICATE_TABLE: str = os.environ["MYSQL_DUPLICATE_TABLE"]
MYSQL_DECISION_TABLE: str = os.environ["MYSQL_DECISION_TABLE"]
EMAIL: str = os.environ["EMAIL"]


default_args = {
    'owner': 'nimbus',
    'depends_on_past': False,
    'email': [EMAIL],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create dag to run every 5 minutes
dag = DAG(dag_id='data_load_dag',
          default_args=default_args,
          schedule_interval='*/5 * * * *',
          dagrun_timeout=timedelta(seconds=5))

params = [KAFKA_BROKER,
          KAFKA_TOPIC,
          MYSQL_URL,
          MYSQL_DB,
          MYSQL_USER,
          MYSQL_PASSWORD,
          MYSQL_RAW_TABLE,
          MYSQL_UNIQUE_TABLE,
          MYSQL_DUPLICATE_TABLE,
          MYSQL_DECISION_TABLE]

data_loader = SparkSubmitOperator(task_id='data_loader',
                                              conn_id='spark_master_container',
                                              application=f'src/main/spark/load-data.py',
                                              total_executor_cores=4,
                                              packages="io.delta:delta-core_2.12:0.7.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0",
                                              executor_cores=2,
                                              executor_memory='5g',
                                              driver_memory='5g',
                                              name='data_loader',
                                              application_args=params,
                                              dag=dag
                                              )
