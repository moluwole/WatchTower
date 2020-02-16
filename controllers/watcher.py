#!/usr/bin/env python

"""
This controller would contain all the modules of the WatchTower
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

from models.watcher import Logs


def get_engine(param):
    watcher = Watcher(param)
    return watcher


class Watcher(object):
    def __init__(self, param=None):
        self.document_id = param if param is not None else "watcher"

    def save(self, client_ip, service, error_message, stack_trace, client_id):
        log = Logs()

        log.client_id = client_id
        log.client_ip = client_ip
        log.service = service
        log.error_message = error_message
        log.stack_trace = stack_trace

        log.insert()

        log.commit()

        self.save_item(log)
        return "Logger saved successfully"

    def save_item(self, watcher):
        client = Client("watcher", port=6379, host=os.getenv('REDIS_HOST'))

        client.add_document(watcher.id,
                            clientIp=watcher.client_ip,
                            service=watcher.service,
                            errorMessage=watcher.error_message,
                            stackTrace=watcher.stack_trace,
                            clientId=watcher.client_id,
                            dateTime=watcher.date_added)

        payload = {
            "clientIp": watcher.client_ip,
            "service": watcher.service,
            "errorMessage": watcher.error_message,
            "stackTrace": watcher.stack_trace,
            "clientId": watcher.client_id,
            "dateTime": watcher.date_added
        }

        if os.getenv('ENABLE_SLACK') == 'true':
            self.send_to_slack(payload)

    @staticmethod
    def send_to_slack(payload):
        url = os.getenv("SLACK_URL")
        headers = {'content-type': 'application/json'}

        message = {"attachments": [
                {
                    "fallback": payload['errorMessage'],
                    "color": "danger",
                    "pretext": "Error from domain {0}".format(payload['clientId']),
                    "author_name": "Watcher Tower",
                    "author_link": os.getenv('SLACK_URL'),
                    "author_icon": os.getenv('SLACK_AUTHOR_IMAGE'),
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
                            "text": "Open WatchTower 🛫",
                            "url": os.getenv('SLACK_URL')
                        }],
                    "footer": "WatchTower",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    "ts": datetime.datetime.now().timestamp()
                }
            ]
        }

        requests.post(url, data=json.dumps(message), headers=headers)


    @classmethod
    def create_index(cls):
        error_message = "Unable to create Index. Try Again"
        redis_enabled = os.getenv("REDIS_SEARCH", False)
        if redis_enabled:
            client = Client("watcher", port=6379, host=os.getenv('REDIS_HOST'))
            try:
                client.create_index(document)
                cls.build_index(client)
                print("Watcher Index created successfully")
            except ResponseError as err:
                print(err)
        else:
            print(error_message)

    @classmethod
    def delete_index(cls):
        client = Client("watcher", port=6379, host=os.getenv('REDIS_HOST'))
        client.drop_index()

    @classmethod
    def build_index(cls, client):
        start_time = time.time()
        all_logs = Logs.all()
        for log in all_logs:
            client.add_document(log.id,
                                clientIp=log.client_ip,
                                service=log.service,
                                errorMessage=log.error_message,
                                stackTrace=log.stack_trace,
                                clientid=log.client_id,
                                dateTime=log.date_time)
        print("----Watcher took {0} seconds to build index------".format(time.time() - start_time))
        print("{0} number of documents in index".format(len(all_logs)))


    @classmethod
    def search(cls, query, offset=0, paginate=10):
        client = Client("watcher", port=6379, host=os.getenv('REDIS_HOST'))
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
        Watcher.delete_index()
    else:
        Watcher.create_index()
