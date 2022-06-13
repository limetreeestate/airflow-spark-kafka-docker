#!/usr/bin/env python

import os
from random import choice
import json
from time import sleep
from kafka import KafkaProducer

if __name__ == '__main__':

    [KAFKA_BROKER, KAFKA_TOPIC] = argv[1:]

    with open("src/main/kafka/data.json", "r") as dataFile:
        data: list = json.loads(dataFile.read())

    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # Produce data by selecting a random value from data.
    while(True):

        message: dict = choice(data)
        producer.send(KAFKA_TOPIC, message)
        sleep(1)
