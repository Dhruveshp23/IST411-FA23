import pika
import json

try:
    with open('payloadPatelD.json', 'r') as json_data:
        msg = json.load(json_data)
        msg = json.dumps(msg)
        msgBytes = msg.encode()
        print("Connecting to Localhost Queue")
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        print("Channel Connected")
        channel.queue_declare(queue='ist411')
        channel.basic_publish(exchange='', routing_key='ist411', body=msgBytes)
        print("Sent: " + msg)
        connection.close()
except Exception as e:
    print(e)
