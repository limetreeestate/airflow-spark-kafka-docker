FROM apache/airflow

USER root

ARG USER_EMAIL=test@gmail.com

# Create man dir required for java installation
RUN mkdir -p /usr/share/man/man1

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME

USER airflow

# Copy source files into container
WORKDIR /app/src/main
COPY src/main/ /app/src/main

WORKDIR /app
COPY airflow-docker/requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN airflow db init

RUN airflow connections add 'spark_master_container' --conn-json '{"conn_type": "Spark", "host": "spark://spark","port": 7077}'

RUN airflow users  create --role Admin --username nimbus --email $USER_EMAIL --firstname admin --lastname admin --password nimbus