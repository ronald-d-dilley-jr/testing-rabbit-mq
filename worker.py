#!/usr/bin/env python
import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(10)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='download_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='download_queue')

    channel.start_consuming()


if __name__ == '__main__':
    main()
