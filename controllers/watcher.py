#!/usr/bin/env python

"""
This controller would contain all the modules of WatchDog
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion
"""
import os
import time
import datetime

import json
import argparse
import requests
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
        self.date_time = str(datetime.datetime.today().strftime('%Y-%m-%d'))

        save_item(self)
        return "Logger saved successfully"

    @staticmethod
    def search(query, offset=0, paginate=10):
        return search(query, offset, paginate)


def send_to_slack(payload):
    url = 'https://hooks.slack.com/services/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'
    headers = {'content-type': 'application/json'}

    message = {"attachments": [
            {
                "fallback": payload['errorMessage'],
                "color": "danger",
                "pretext": "Error from domain https://{0}.eduquestpro.com".format(payload['clientId']),
                "author_name": "WatchDog",
                "author_link": "https://watchdog.eduquestpro.com",
                "author_icon": "https://watchdog.eduquestpro.com/static/img/watch_dog.png",
                "title": "{0} Microservice Error".format(payload['service']),
                "text": payload['stackTrace'],
                "fields": [
                    {
                        "title": "Priority",
                        "value": "Critical",
                        "short": False
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": "Open WatchDog 🛫",
                        "url": "https://watchdog.eduquestpro.com"
                    }],
                "footer": "WatchDog",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": datetime.datetime.now().timestamp()
            }
        ]
    }

    requests.post(url, data=json.dumps(message), headers=headers)


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
    client = Client("watcher", port=6379, host='redisearch')
    client.drop_index()


def build_index(client):
    start_time = time.time()
    all_logs = Logs.all()
    for log in all_logs:
        client.add_document(log.id, clientIp=log.client_ip, service=log.service, errorMessage=log.error_message,
                            stackTrace=log.stack_trace, clientid=log.client_id, dateTime=log.date_time)
    print("----Watcher took {0} seconds to build index------".format(time.time() - start_time))
    print("{0} number of documents in index".format(len(all_logs)))


def save_item(watcher):
    client = Client("watcher", port=6379, host='redisearch')

    client.add_document(watcher.id, clientIp=watcher.client_ip, service=watcher.service,
                        errorMessage=watcher.error_message, stackTrace=watcher.stack_trace,
                        clientId=watcher.client_id, dateTime=watcher.date_time)

    payload = {
        "clientIp": watcher.client_ip,
        "service": watcher.service,
        "errorMessage": watcher.error_message,
        "stackTrace": watcher.stack_trace,
        "clientId": watcher.client_id,
        "dateTime": watcher.date_time
    }
    send_to_slack(payload)


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
            'client_id': doc.clientId,
            'datetime': doc.dateTime
        }
        result.append(value_dict)
    print(res)
    return result


document = [
    TextField('clientIp', weight=5.0),
    TextField('service', weight=1.0),
    TextField('errorMessage', weight=10.0),
    TextField('stackTrace'),
    TextField('clientId', weight=10.0),
    TextField('dateTime', weight=10.0)
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build the Search Index for RediSearch")
    parser.add_argument('-d', '--delete', dest='del_index', help="Deletes the former index. Must only be used if there is an index already",
                        required=False, const=True, default=False, nargs='?')

    args = parser.parse_args()

    if args.del_index:
        delete_index()

    create_index()
