#!/usr/bin/env python

import os
import json
import pika


def main():
    job_id = str(os.getpid())

    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='download_queue', durable=True)

    message = dict()
    message['request'] = dict()
    message['request']['job-id'] = job_id
    message['request']['url'] = 'http://happy'
    message['request']['destination'] = '/tmp/butter'
    message_json = json.dumps(message, ensure_ascii=False)

    channel.basic_publish(exchange='',
                          routing_key='download_queue',
                          body=message_json,
                          properties=pika.BasicProperties(delivery_mode=2))

    print(" [x] Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    main()
