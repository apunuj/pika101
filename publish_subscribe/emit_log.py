import pika, sys

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange = 'logs',
                        exchange_type = 'fanout')

channel.queue_declare("Hello1" )

channel.queue_bind(exchange = 'logs', queue="Hello1")

message = ' '.join(sys.argv[1:])

channel.basic_publish(exchange = "logs",
                        routing_key = "",
                        body = message)

print("[x] Sent %r" %message)

connection.close()
