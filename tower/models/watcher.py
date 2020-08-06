"""
Model for Watcher
@author: Oluwole Majiyagbe
@email: oluwole564@gmail.com
"""

from sqlalchemy import *
from models import Model


class Logs(Model):
    __tablename__ = 'logs'

    client_ip = Column('clientIp', VARCHAR(length=20))
    service = Column('service', VARCHAR(length=250))
    date_occurred = Column('dateOccurred', TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    error_message = Column('errorMessage', TEXT)
    stack_trace = Column('stackTrace', TEXT)
    number_range = Column('numberRange', INTEGER)

class Users(Model):
    __tablename__ = "users"

    username = Column('username', VARCHAR(100), nullable=False)
    password = Column('password',VARCHAR(200), nullable=False)
    last_login = Column('last_login', VARCHAR(200))