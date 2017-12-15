import pika
import sys

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.confirm_delivery()

props = pika.BasicProperties(content_type='text/plain', delivery_mode=1)
try:
    for line in sys.stdin:
        if channel.basic_publish('amq.topic', 'q', line, props):
            print('confirmed')
        else:
            print('rejected')
except KeyboardInterrupt:
    pass

connection.close()
