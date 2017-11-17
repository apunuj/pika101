import pika

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue = 'Hello')

channel.basic_publish(exchange = "", routing_key = 'Hello', body = "Hello World")

print("[x] message sent to consumer")

connection.close()
