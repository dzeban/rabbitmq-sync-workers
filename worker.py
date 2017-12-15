#!/usr/bin/env python

import pika
import sys
import argparse

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

ap = argparse.ArgumentParser('Queue worker')
ap.add_argument('-q', '--queue', help='Queue name', required=True)
args = ap.parse_args()

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback,
                      queue=args.queue,
                      no_ack=False)

print(' [*] Waiting for messages from {}...'.format(args.queue))
try:
    channel.start_consuming()
except KeyboardInterrupt:
    pass

connection.close()
