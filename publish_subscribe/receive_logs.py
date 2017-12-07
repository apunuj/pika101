import pika, requests, json, datetime

from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import PrettyPrinter

RABBITMQ_URL = 'amqp://igjlkqzn:9wOZFQjDlt-sfCA4UA0RTuODb69ioDSR@elephant.rmq.cloudamqp.com/igjlkqzn'
MONGO_URL = 'mongodb://devteam:dev786786@ds021663.mlab.com:21663/referyodb'

db = MongoClient(MONGO_URL).referyodb

params = pika.URLParameters(RABBITMQ_URL)
params.socket_timeout = 5


connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                        exchange_type = "fanout")

channel.queue_declare("Hello1")

channel.queue_bind(exchange="logs", queue="Hello1")

print("[*] waiting for logs. To exit press CTRL+C")

def updateCampaignAnalytics(campaignId, key):

    print("[x]: Event to be updated is %r" %key)

    if key == "delivered":
        attr = "aly.d"
    elif key == "clicked":
        attr = "aly.c"
    elif key == "opened":
        attr = "aly.o"
    elif key == "bounced":
        attr = "aly.b"
    elif key == "unsubscribed":
        attr = "aly.u"
    elif key == "spam":
        attr = "aly.s"
    else:
        attr = "aly.f"

    db.emailcampaigns.update({"_id":ObjectId(campaignId)}, {'$inc': {attr:1}})
    print("Analytics is Updated")

def saveEvents(campaignId, bodyObject):
    time_stamp = int(bodyObject["timestamp"])
    dateString = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d')

    try:
        updatedDoc = db.campaignEvents.update({'cid': campaignId, 't': dateString},
                                    {'$push': {'ev': bodyObject}},
                                    upsert=True)
        print("Event is saved in the database")
    except Exception as e:
        print("The following error happened while saving the event:")
        print(e)

    
def callback(channel, method, properties, body):
    body = body.decode("utf-8")
    try:
        bodyObject = json.loads(body)
    except Exception as e:
        print("This mail can't be parsed into json. Ignoring!")
        print(e)
        return

    print("[x]: new email object received at the queue")
    PrettyPrinter(indent = 4).pprint(bodyObject)

    if "campaignInfo" in bodyObject.keys():
        campaignInfo = json.loads(bodyObject["campaignInfo"])
        event = bodyObject["event"]
        updateCampaignAnalytics(campaignInfo["id"], event)
        saveEvents(campaignInfo["id"], bodyObject)


def main():
    channel.basic_consume(callback, queue="Hello1", no_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
