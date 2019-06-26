"""
Model for Watcher
@author: Oluwole Majiyagbe
@email: oluwole.majiyagbe@firstpavitech.com
@organisation: First Pavilion
"""

from sqlalchemy import *
from core import db
from core.utils import uuid


class Watcher(db.OurMixin, db.Base):
    __tablename__ = 'watcher'

    id = Column(u'id', CHAR(length=36), default=uuid, primary_key=True, nullable=False)
    client_ip = Column(u'clientIp', VARCHAR(length=20))
    service = Column(u'service', VARCHAR(length=250))
    date_occurred = Column(u'dateOccurred', TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    error_message = Column(u'errorMessage', TEXT)
    stack_trace = Column(u'stackTrace', TEXT)
    client_id = Column('clientId', CHAR(length=36))
