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
usage: launch.py [-h] [-e EXCHANGE] [-f FILE] [-m FILE] [-r KEY] [-u URI]
                 bunnos

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
                        defails of the message input file. Defaults to
                        `formatter.py` in the working directory
  -m FILE, --message FILE
                        Filename that holds message template to launch.
                        Defaults to `message.json`
  -o HOST, --host HOST  Rabbitmq hostname to connect to. Defaults to
                        `localhost`
  -p PORT, --port PORT  Rabbitmq port to connect to. Defaults to `5672`
  -P PASSWORD, --password PASSWORD
                        Rabbitmq password to connect with. Defaults to `guest`
  -r KEY, --routing_key KEY
                        Routing key to mark message with
  -u USERNAME, --username USERNAME
                        Rabbitmq usernamee to connect with. Defaults to
                        `guest`
```

## License

See LICENSE file. Apache License 2.0

## Plan

Items to do
* add threads for higher throughput
* tests
* make installable
* * better readme for message and formatter after that
* replace deprecated imports
* add properties file for configuration instead of all arguments