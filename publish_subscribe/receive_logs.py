import pika

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                        exchange_type = "fanout")

channel.queue_declare("Hello1")

channel.queue_bind(exchange="logs", queue="Hello1")

print("[*] waiting for logs. To exit press CTRL+C")

def callback(channel, method, properties, body):
    print("[x] %r" %body)

channel.basic_consume(callback, queue="Hello1", no_ack=True)

channel.start_consuming()
