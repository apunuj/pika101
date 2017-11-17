import pika

# TODO: Connect to rabbitmq channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn



# TODO: pickup the message containing encrypted tracking event



# TODO: decode the message



#TODO: parse the message to return a object containing all the parameters to be extracted



#TODO: process the message and tell the queue it has been processed
