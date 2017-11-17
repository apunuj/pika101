import pika, sys

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare("task_queue", durable = True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange = "",
                    routing_key = 'task_queue',
                    body = message,
                    properties = pika.BasicProperties(delivery_mode = 2))

print("[x] sent %r" %message)

connection.close()
