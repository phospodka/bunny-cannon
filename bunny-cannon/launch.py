#!/usr/bin/env python3
import argparse
import imp
import json
import pika
import threading
from tqdm import tqdm


def prime(args):
    """
    Entry point for launching. Primes the cannon by loading file contents up front as they are
    static. Initiates the number of threads to launch and starts them all.
    :param args: container object for the arguments
    """
    message = load_message(args.message)
    headers = load_headers(args.headers)

    # replace with importlib for use with 3.5+?
    formatter = imp.load_source('formatter', args.formatter)

    for i in range(args.threads):
        cannon = threading.Thread(name='cannon-' + str(i),
                                  target=launch,
                                  args=(args, message, headers, formatter))

        # start up the thread
        cannon.start()


def launch(args, message, headers, formatter):
    """
    Creates the connection to rabbitmq and sends the requested number of messages to the server.
    The message is passed as input as well as a formatter that can add uniqueness per message.
    :param args: container object for the arguments
    :param message: message to send to rabbitmq
    :param headers: headers to attach to message
    :param formatter: formatter with `format(m)` function to apply to message before sending
    """
    credentials = pika.PlainCredentials(args.username, args.password)
    props = pika.BasicProperties(content_type='application/json',
                                 headers=headers,
                                 delivery_mode=2)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=args.host,
            port=args.port,
            credentials=credentials))
    channel = connection.channel()

    # tqdm the range for pretty metrics
    for i in tqdm(range(args.bunnos)):
        channel.basic_publish(exchange=args.exchange,
                              routing_key=args.routing_key,
                              properties=props,
                              body=formatter.format(message))

    connection.close()


def load_headers(filename):
    """
    Load the headers to be added to the message from the file system. Defaults to look in the
    working directory.
    :param filename: path to the filename to load
    :return: headers from file as a dict
    """
    with open(filename, 'r') as f:
        return json.loads(f.read())


def load_message(filename):
    """
    Load the message that will be launched from the file system. Defaults to look in the
    working directory.
    :param filename: path to the filename to load
    :return: message from file as a string
    """
    with open(filename, 'r') as f:
        return f.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bunny cannon is a python utility to bulk send '
                                                 'messages a rabbitmq exchange.')

    parser.add_argument('bunnos', type=int, help='Number of messages to launch per thread')
    parser.add_argument('-d', '--headers', metavar='FILE', type=str, default='headers.json',
                        help='Filename that holds headers to add to the message. Defaults to '
                             '`headers.json`')
    parser.add_argument('-e', '--exchange', metavar='EXCHANGE', type=str,
                        help='Exchange to send messages to')
    parser.add_argument('-f', '--formatter', metavar='FILE', type=str, default='formatter.py',
                        help='Python script that contains a `def format(message)` method that '
                             'defines how to format, replace, etc defails of the message input '
                             'file. Defaults to `formatter.py` in the working directory')
    parser.add_argument('-H', '--host', metavar='HOST', type=str, default='localhost',
                        help='Rabbitmq hostname to connect to. Defaults to `localhost`')
    parser.add_argument('-m', '--message', metavar='FILE', type=str, default='message.json',
                        help='Filename that holds message template to launch. Defaults to '
                             '`message.json`')
    parser.add_argument('-p', '--password', metavar='PASSWORD', type=str, default='guest',
                        help='Rabbitmq password to connect with. Defaults to `guest`')
    parser.add_argument('-P', '--port', metavar='PORT', type=str, default='5672',
                        help='Rabbitmq port to connect to. Defaults to `5672`')
    parser.add_argument('-r', '--routing_key', metavar='KEY', type=str,
                        help='Routing key to mark message with')
    parser.add_argument('-u', '--username', metavar='USERNAME', type=str, default='guest',
                        help='Rabbitmq usernamee to connect with. Defaults to `guest`')
    parser.add_argument('-t', '--threads', metavar='NUM', type=int, default=1,
                        help='Number of threads to launch messages with')

    prime(parser.parse_args())
