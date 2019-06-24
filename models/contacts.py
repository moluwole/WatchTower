import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import relationship, validates

from core import db
from core.utils import uuid


class Contacts(db.OurMixin, db.Base):
    __tablename__ = "contact"

    id = Column(u'id', CHAR(length=36), default=uuid, primary_key=True, nullable=False)
    username = Column(u'username', VARCHAR(length=20))
    password = Column(u'password', VARCHAR(length=250))

    @property
    def username(self):
        return self.username
