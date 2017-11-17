import pika, time

URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'

params = pika.URLParameters(URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare("task_queue", durable = True)

print("[*] waiting for messages; to exit press CTRL+C")

def callback(ch, method, properties, body):
    print("[x] received %r" %body)
    time.sleep(body.count(b'.'))
    print("[x] done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1)

channel.basic_consume(callback, queue = "task_queue")

channel.start_consuming()
