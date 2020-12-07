#!/usr/bin/env python3
import argparse
import pika


def consume(args, autoack):
    """
    Consume messages from rabbit
    :param args: container object for the arguments
    :param autoack: flag whether we are manual ack or auto ack
    """
    credentials = pika.PlainCredentials(args.username, args.password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=args.host,
        port=args.port,
        credentials=credentials))
    channel = connection.channel()

    response = channel.basic_get(queue=args.queue, auto_ack=autoack)
    print(response[2])


def main(args):
    print(' [*] Waiting for bunnos. CTRL+C to exit')
    # blocking connection is not thread safe; need to use either; SelectConnection; AsyncioConnection
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    #channel1 = connection.channel()
    #channel2 = connection.channel()

    consume(args, True)


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

    main(parser.parse_args())
