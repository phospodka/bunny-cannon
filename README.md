# Bunny Cannon

Bunny cannon is a python utility to bulk send messages a rabbitmq exchange. It provides a way to 
send N number of messages that can be formatted by a user defined function.  This function must
be a python module with a `def format(message)` method defined.  This module will be imported at
runtime and will look for it by default in `formatter.py` from the working directory. 

## Dependencies

Install the requirements with:

`pip install -r requirements.txt`

Tested against python 3.4+

## Usage

```
usage: launch.py [-h] [-d FILE] [-e EXCHANGE] [-f FILE] [-H HOST] [-m FILE]
                 [-p PASSWORD] [-P PORT] [-r KEY] [-u USERNAME] [-t NUM]
                 bunnos

Bunny cannon is a python utility to bulk send messages a rabbitmq exchange.

positional arguments:
  bunnos                Number of messages to launch per thread

optional arguments:
  -h, --help            show this help message and exit
  -d FILE, --headers FILE
                        Filename that holds headers to add to the message.
                        Defaults to `headers.json`
  -e EXCHANGE, --exchange EXCHANGE
                        Exchange to send messages to
  -f FILE, --formatter FILE
                        Python script that contains a `def format(message)`
                        method that defines how to format, replace, etc
                        details of the message input file. Defaults to
                        `formatter.py` in the working directory
  -H HOST, --host HOST  Rabbitmq hostname to connect to. Defaults to
                        `localhost`
  -m FILE, --message FILE
                        Filename that holds message template to launch.
                        Defaults to `message.json`
  -p PASSWORD, --password PASSWORD
                        Rabbitmq password to connect with. Defaults to `guest`
  -P PORT, --port PORT  Rabbitmq port to connect to. Defaults to `5672`
  -r KEY, --routing_key KEY
                        Routing key to mark message with
  -u USERNAME, --username USERNAME
                        Rabbitmq username to connect with. Defaults to
                        `guest`
  -t NUM, --threads NUM
                        Number of threads to launch messages with
```

## License

See [[LICENSE]] file. Apache License 2.0

## Todo

Items to do
* tests
* make installable
* * better readme for message and formatter after that
* replace deprecated imports
* add properties file for configuration instead of all arguments
* add speed throttling / flow control for consistent rate of messaging