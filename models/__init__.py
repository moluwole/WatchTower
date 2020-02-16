"""

Collection of SQLALchemy Database utilities to be used in WatchTower.

"""
import os

from sqlalchemy import *

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (scoped_session, sessionmaker, aliased, joinedload_all)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from core.utils import uuid, json_dumps
from core.config import app_config

dev_env = app_config[os.getenv('APP_ENV', 'development')]

engine = create_engine(dev_env.SQLALCHEMY_DATABASE_URI, echo=False, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables Created")


def drop_db():
    Base.metadata.drop_all(bind=engine)


class Helper(object):
    """Our Mixin class for defining declarative table models
        in SQLAlchemy. We use this class to define consistent table
        args, methods, etc."""

    def __init__(self, **kwargs):
        """Override default __init__, if the mapper has an id
        column and it isn't set, set it to a new uuid."""
        for k, v in kwargs.items():
            setattr(self, k, v)

        if hasattr(self, 'id') and not self.id:
            self.id = uuid()

    def __repr__(self):
        if hasattr(self, 'id'):
            return '%s(%s) Address: %s' % (self.__class__, self.id, id(self))
        else:
            return '%s Address: %s' % (self.__class__, id(self))

    def __str__(self):
        return self.to_json()

    @classmethod
    def all(self):
        return Session.query(self).all()

    @classmethod
    def count(self):
        from sqlalchemy import func
        return Session.query(func.count(self.id)).scalar()

    def delete(self):
        Session.delete(self)

    @classmethod
    def filter(self, *args, **kwargs):
        return Session.query(self).filter(*args, **kwargs)

    @classmethod
    def filter_by(self, *args, **kwargs):
        return Session.query(self).filter_by(*args, **kwargs)

    @classmethod
    def first(self):
        return Session.query(self).first()

    @classmethod
    def get(self, primary_key, preload=[]):
        result = None
        if primary_key is not None:
            result = Session.query(self)
            for name in preload:
                result = result.options(joinedload_all(name))
            result = result.get(primary_key)
        return result

    def insert(self, return_key='id', return_attr='id'):
        Session.add(self)
        Session.merge(self)

        return json_dumps({return_key: getattr(self, return_attr)})

    @property
    def is_valid(self):
        return self.validate().get('success', False)

    @classmethod
    def join(self, *args, **kwargs):
        return Session.query(self).join(*args, **kwargs)

    @classmethod
    def max(self, column_name):
        return Session.query(func.max(getattr(self, column_name))).scalar()

    @classmethod
    def min(self, column_name):
        return Session.query(func.min(getattr(self, column_name))).scalar()

    @classmethod
    def order_by(self, *args, **kwargs):
        return Session.query(self).order_by(*args, **kwargs)

    @classmethod
    def outerjoin(self, *args, **kwargs):
        return Session.query(self).outerjoin(*args, **kwargs)

    @classmethod
    def random(self):
        return Session.query(self).order_by(func.random()).first()

    def validate(self):
        return {'success': True, 'message': 'The record is valid.'}

    def commit(self):
        try:
            Session.commit()
        except (Exception, SQLAlchemyError):
            Session.rollback()
            Session.connection.invalidate()
            session.close()


class Model(Base, Helper):
    __abstract__ = True

    id = Column(u'id', CHAR(length=36), default=uuid, primary_key=True, nullable=False)
    date_added = Column('dateAdded', TIMESTAMP(), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    date_updated = Column(u'dateUpdated', TIMESTAMP(), nullable=False, server_onupdate=text('CURRENT_TIMESTAMP'),
                          server_default=text('CURRENT_TIMESTAMP'))