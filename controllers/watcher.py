#!/usr/bin/env python

"""
This controller would contain all the modules of WatchDog
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion
"""
import os
import time

import argparse
from redisearch import Client, TextField, Query
from redis.exceptions import ResponseError

from core import db
from models.watcher import Watcher as Logs


def get_engine(param):
    watcher = Watcher(param)
    return watcher


class Watcher(object):
    def __init__(self, param=None):
        self.document_id = param if param is not None else "watcher"

    def save(self, client_ip, service, error_message, stack_trace, client_id):
        error_log = Logs(client_ip=client_ip, service=service, error_message=error_message, stack_trace=stack_trace,
                         client_id=client_id)
        error_id = error_log.insert()

        db.safe_commit()

        self.client_ip = client_ip
        self.service = service
        self.error_message = error_message
        self.stack_trace = stack_trace
        self.client_id = client_id
        self.id = error_id

        save_item(self)
        return "Logger saved successfully"

    @staticmethod
    def search(query, offset=0, paginate=10):
        return search(query, offset, paginate)


def create_index():
    error_message = "Unable to create Index. Try Again"
    redis_enabled = os.getenv("REDIS_SEARCH", False)
    if redis_enabled:
        client = Client("watcher", port=6379, host='redisearch')
        try:
            client.create_index(document)
            build_index(client)
            print("Watcher Index created successfully")
        except ResponseError as err:
            print(err)
    else:
        print(error_message)


def delete_index():
    client = Client('watcher', port=6379, host='redisearch')
    client.drop_index()


def build_index(client):
    start_time = time.time()
    for log in Logs.all():
        client.add_document(log.id, clientIp=log.client_ip, service=log.service, errorMessage=log.error_message,
                            stackTrace=log.stack_trace, clientid=log.client_id)
    print("----Watcher took {0} seconds to build index------".format(time.time() - start_time))
    info = client.info()
    print("{0} number of documents in index".format(len(info.items())))


def save_item(watcher):
    client = Client("watcher", port=6379, host='redisearch')

    client.add_document(watcher.id, clientIp=watcher.client_ip, service=watcher.service,
                        errorMessage=watcher.error_message, stackTrace=watcher.stack_trace,
                        clientId=watcher.client_id)


def search(query, offset=0, paginate=10):
    client = Client("watcher", port=6379, host='redisearch')
    q = Query(query).paging(offset, paginate)
    res = client.search(q)
    result = []
    for doc in res.docs:
        value_dict = {
            'id': doc.id,
            'client_ip': doc.clientIp,
            'service': doc.service,
            'error_message': doc.errorMessage,
            'stack_trace': doc.stackTrace,
            'client_id': doc.clientid
        }
        result.append(value_dict)
    return result


document = [
    TextField('clientIp', weight=5.0),
    TextField('service', weight=1.0),
    TextField('errorMessage', weight=10.0),
    TextField('stackTrace'),
    TextField('clientId', weight=10.0)
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build the Search Index for RediSearch")
    parser.add_argument('-d', '--delete', dest='del_index', help="Deletes the former index. Must only be used if there is an index already",
                        required=False, const=True, default=False, nargs='?')

    args = parser.parse_args()

    if args.del_index:
        delete_index()

    create_index()
