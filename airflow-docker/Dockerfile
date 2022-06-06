FROM apache/airflow

USER root

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y default-jdk && \
    apt-get install -y default-jre && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME

USER airflow

# Copy source files into container
WORKDIR /app/src/main
COPY ../src/main /app/src/main

WORKDIR /app
COPY requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt