"""
This controller would contain all the modules of WatchDog
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion
"""

from core import db
from models.watcher import Watcher as Logs

class Watcher(object):
    def __init__(self, client_ip, service, error_message, stack_trace, client_id):
        self.client_ip = client_ip
        self.service = service
        self.error_message = error_message
        self.stack_trace = stack_trace
        self.client_id = client_id

    def save(self):
        error_log = Logs(client_ip=self.client_ip, service=service, error_message=self.error_message, stack_trace=self.stack_trace, client_id=self.client_id)
        error_id = error_log.insert()

        # Prevent Insert DeadLock
        db.safe_commit()