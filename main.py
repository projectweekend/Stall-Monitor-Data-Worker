#!/usr/bin/env python

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from pika_pack import Listener


RABBIT_URL = os.getenv('RABBIT_URL', None)
assert RABBIT_URL

MONGO_URL = os.getenv('MONGO_URL', None)
assert MONGO_URL

EXCHANGE = 'gpio_broadcast'

DEVICE_KEY = 'stall_monitor'


def connect_to_mongo():
    client = MongoClient(MONGO_URL)
    return client.get_default_database()


def main():
    mongo_db = connect_to_mongo()

    def log_stall_activity(message):
        mongo_db.activity.insert({
            'is_open': message['door_open'],
            'date': datetime.fromtimestamp(message['timestamp'])
        })

    rabbit_listener = Listener(
        rabbit_url=RABBIT_URL,
        exchange=EXCHANGE,
        routing_key=DEVICE_KEY,
        request_action=log_stall_activity)

    try:
        rabbit_listener.start()
    except:
        sys.exit(1)


if __name__ == '__main__':
    main()
