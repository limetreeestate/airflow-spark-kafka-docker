from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('nimbus1')
for msg in consumer:
    print (json.loads(msg.value))