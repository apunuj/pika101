import pika

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue = "Hello")

def callback(ch, method, properties, body):
    print("[x] Received %r" %body)


channel.basic_consume(callback, queue = 'Hello', no_ack = True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
