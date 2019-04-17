import uuid


def format(message):
    return message.replace('${uuid}', str(uuid.uuid4()))
