from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable

KAFKA_BROKER: str = os.environ[KAFKA_BROKER]
KAFKA_TOPIC: str = os.environ[KAFKA_TOPIC]
EMAIL: str = os.environ[EMAIL]

default_args = {
    'owner': 'nimbus',
    'depends_on_past': False,
    'email': [EMAIL],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(dag_id='data_producer',
          default_args=default_args,
          catchup=False,
          schedule_interval="@once")

bashCommand = f"python3 src/main/kafka/producer.py {KAFKA_BROKER} {KAFKA_TOPIC}" 

data_producer = BashOperator(task_id='data_producer',
                                       task_id='templated',
                                       depends_on_past=False,
                                       bash_command=bashCommand,
                                       dag=dag
                                       )
