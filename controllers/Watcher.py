"""
This controller would contain all the modules of WatchDog
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion
"""
import os

from redisearch import Client, TextField, NumericField, Query
from redis.exceptions import ResponseError

from core import db
from core.utils import uuid
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
    def search(query):
        return search(query)


def create_index():
    error_message = "Unable to create Index. Try Again"
    redis_enabled = os.getenv("REDIS_SEARCH", False)
    if redis_enabled:
        client = Client("watcher", port=6379, host='redisearch')
        try:
            client.create_index(document)
            return client
        except ResponseError as err:
            return err
    else:
        return error_message


def save_item(watcher):
    client = Client("watcher", port=6379, host='redisearch')

    if type(client) != str:
        client.add_document(watcher.id, clientIp=watcher.client_ip, service=watcher.service,
                        errorMessage=watcher.error_message, stackTrace=watcher.stack_trace, clientId=watcher.client_id)


def search(query, offset=0, paginate=10):
    client = Client("watcher", port=6379, host='redisearch')
    q = Query(query).verbatim().no_content().paging(offset, paginate)
    res = client.search(q)
    result = {}
    # for doc in res.docs:
    #     result[doc.]
    print(res.docs[0].payload)
    return res


document = [
    TextField('clientIp', weight=5.0),
    TextField('service', weight=1.0),
    TextField('errorMessage', weight=10.0),
    TextField('stackTrace'),
    TextField('clientId', weight=10.0)
]


if __name__ == '__main__':
    create_index()
