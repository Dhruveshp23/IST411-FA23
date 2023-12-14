import pika

try:
    print("Connection established.")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    print("Queue ist411 created.")
    channel.queue_declare(queue='ist411')

    def callback(ch, method, properties, body):
        print("Received: %r" % body)

    channel.basic_consume('ist411', callback, auto_ack=True)
    print("Waiting for messages. Press Ctrl+C to exit.")
    
    try:
        # Keep the script running until Ctrl+C is pressed
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting gracefully...")

except Exception as e:
    print(e)
