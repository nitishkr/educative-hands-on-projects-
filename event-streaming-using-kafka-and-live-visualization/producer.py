from kafka import KafkaProducer
import time
import psutil
topic_name = 'test-topic'
kafka_server = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=kafka_server)
for i in range(1000):
     time.sleep(0.5)
     cpu_percentage = int(psutil.cpu_percent())
     print(cpu_percentage)
     cpu_percentage_bytes = cpu_percentage.to_bytes(2, 'big')
     producer.send(topic_name, cpu_percentage_bytes)
     