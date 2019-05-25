#!/usr/bin/env python3
import argparse
import pika
import threading


def handler(channel, method, properties, body, autoack):
    """
    Process a message from the queue
    :param channel: rabbit channel
    :param method: rabbit method
    :param properties: message properties
    :param body: message body
    :param autoack: flag whether we are manual ack or auto ack
    """
    print(str(method.consumer_tag) + ' : ' + str(method.delivery_tag) + ' - %r' % body)

    if not autoack:
        channel.basic_ack(method.delivery_tag)


def consume(args, tag, autoack):
    """
    Consume messages from rabbit
    :param args: container object for the arguments
    :param tag: base tag to identify the consumer
    :param autoack: flag whether we are manual ack or auto ack
    """
    credentials = pika.PlainCredentials(args.username, args.password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=args.host,
        port=args.port,
        credentials=credentials))
    channel = connection.channel()

    ctag = tag + str(channel.channel_number)
    print('starting consumer ' + ctag)

    channel.basic_consume(queue=args.queue,
                          on_message_callback=lambda c, m, p, b: handler(c, m, p, b, autoack),
                          auto_ack=autoack,
                          consumer_tag=ctag)
    channel.start_consuming()


def main(args):
    print(' [*] Waiting for bunnos. CTRL+C to exit')
    # blocking connection is not thread safe; need to use either; SelectConnection; AsyncioConnection
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    #channel1 = connection.channel()
    #channel2 = connection.channel()

    for i in range(args.threads):
        t = threading.Thread(name='consumed-' + str(i),
                             target=consume,
                             args=(args, 'ctag.bc-' + str(i) + '-', False),
                             daemon=True)
        t.start()
        t.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bunny consume is a python utility to consume '
                                                 'messages from a rabbitmq queue.')

    parser.add_argument('-H', '--host', metavar='HOST', type=str, default='localhost',
                        help='Rabbitmq hostname to connect to. Defaults to `localhost`')
    parser.add_argument('-p', '--password', metavar='PASSWORD', type=str, default='guest',
                        help='Rabbitmq password to connect with. Defaults to `guest`')
    parser.add_argument('-P', '--port', metavar='PORT', type=str, default='5672',
                        help='Rabbitmq port to connect to. Defaults to `5672`')
    parser.add_argument('-q', '--queue', metavar='QUEUE', type=str,
                        help='Queue to consume messages from')
    parser.add_argument('-u', '--username', metavar='USERNAME', type=str, default='guest',
                        help='Rabbitmq username to connect with. Defaults to `guest`')
    parser.add_argument('-t', '--threads', metavar='NUM', type=int, default=1,
                        help='Number of threads to launch messages with')

    main(parser.parse_args())
