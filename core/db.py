"""

Collection of SQLALchemy Database utilities to be used in EduQuest.

"""
import os
import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (scoped_session, sessionmaker, aliased, joinedload_all)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from .utils import uuid, camelcase_to_underscore, underscore_to_camelcase, json_dumps
from .config import app_config

dev_env = app_config[os.getenv('APP_ENV', 'development')]

print(dev_env.SQLALCHEMY_DATABASE_URI)

engine = create_engine(dev_env.SQLALCHEMY_DATABASE_URI, echo=True, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


class OurMixin(object):
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
    def aliased(self, name=None):
        """Convenience method to alias a table under another name."""
        return aliased(self) if name is None else aliased(self, name=name)

    @classmethod
    def all(self):
        """Convenience method to return all the records in a table.

        @return: The model with the passed primary key."""
        return Session.query(self).all()

    def clone(self, source, new_item=True, skip=None):
        skip = skip or []

        if not new_item:
            skip.append('id')

        for column in source.__table__.c:
            column_attribute = camelcase_to_underscore(column.name)
            if column_attribute not in skip:
                setattr(self, column_attribute, getattr(source, column_attribute))

        if new_item:
            self.id = uuid()

    @classmethod
    def count(self):
        from sqlalchemy import func
        return Session.query(func.count(self.id)).scalar()

    def delete(self):
        """Convenience method to remove a model from the session
        and ultimately from the database upon commit."""
        Session.delete(self)

    @classmethod
    def filter(self, *args, **kwargs):
        """Convenience method to return a Query object with the
        passed SQLAlchemy Clause statement a filter.

        @return: A SQLALchemy Query object."""
        return Session.query(self).filter(*args, **kwargs)

    @classmethod
    def filter_by(self, *args, **kwargs):
        """Convenience method to return a Query object with the
        passed args & kwargs to Query.filter_by.

        @return: A SQLALchemy Query object."""
        return Session.query(self).filter_by(*args, **kwargs)

    @classmethod
    def first(self):
        """Convenience method to return a single record in a table.

        @return: The first model from the table."""
        return Session.query(self).first()

    def from_dict(self, the_dict, strict=False):
        """
        Convenience method to populate a model from a dict. It will automatically convert camel case keys
        to underscore equivalents.

        @param: the_dict: A dictionary of values to be set in the model.
        @param: strict: A boolean switch to throw an exception if the corresponding key is not found

        @return: An instance of the model with the keys set.
        """
        for key in the_dict:
            us_key = camelcase_to_underscore(key)
            if hasattr(self, us_key):
                setattr(self, us_key, the_dict[key])
            else:
                if strict:
                    raise UserWarning('from_dict() error: The %s model does not have a %s key.' % (self.__class__, us_key))
        return self

    @classmethod
    def get(self, primary_key, preload=[]):
        """Convenience method to take a primary key of the model
        and return a single model instance or None if the model
        couldn't be found using the key.

        @param primary_key: The primary key for the model.
        @return: The model with the passed primary key.
        @param preload: """
        result = None
        if primary_key is not None:
            result = Session.query(self)
            for name in preload:
                result = result.options(joinedload_all(name))
            result = result.get(primary_key)
        return result

    @classmethod
    def get_enum_values(self, column):
        """ Convenience method to programmatically retrieve
            the available values of an enum column."""
        vals = ()
        try:
            vals = getattr(self, column).property.columns[0].type.enums
        except:
            pass

        return vals

    def insert(self, merge=True, return_key='id', return_attr='id'):
        """Convenience method to add a model to the session
        and ultimately insert in the database permanently upon commit."""
        Session.add(self)
        Session.merge(self)

        return json_dumps({return_key: getattr(self, return_attr)})

    @property
    def is_valid(self):
        return self.validate().get('success', False)

    @classmethod
    def join(self, *args, **kwargs):
        """Convenience method to return a Query object
        by using the Query.join object.

        @return: A SQLALchemy Query object."""
        return Session.query(self).join(*args, **kwargs)

    @classmethod
    def max(self, column_name):
        from sqlalchemy import func
        return Session.query(func.max(getattr(self, column_name))).scalar()

    @classmethod
    def min(self, column_name):
        from sqlalchemy import func
        return Session.query(func.min(getattr(self, column_name))).scalar()

    @classmethod
    def order_by(self, *args, **kwargs):
        """Convenience method to return a Query object with the
        passed args & kwargs to Query.order_by.

        @return: A SQLALchemy Query object."""
        return Session.query(self).order_by(*args, **kwargs)

    @classmethod
    def outerjoin(self, *args, **kwargs):
        """Convenience method to return a Query object
        by using the Query.outerjoin object.

        @return: A SQLALchemy Query object."""
        return Session.query(self).outerjoin(*args, **kwargs)

    @classmethod
    def random(self):
        # Postgres
        return Session.query(self).order_by(func.random()).first()

    @classmethod
    def select_from(self, *args, **kwargs):
        """Convenience method to return a Query object
        via a call to Query.select_from().

        @return: A SQLAlchemy Query Object."""
        return Session.query(self).select_from(*args, **kwargs)

    @classmethod
    def columns(self, *columns):
        """Convenience method to return a Query object
        to select specific columns.
        NOTE: columns must be fully specified from model:
            > MyModel.columns(MyModel.id, OtherModel.name)

        @return: A SQLAlchemy Query Object."""
        return Session.query(*columns)

    def set(self, **kwargs):
        """
        Use each key in kwargs to set the appropriate value in self
        """
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise UserWarning('%s has no attribute %s' % (self.__class__, key))

    def find_type(self, colname):
        if colname in self.__table__.c:
            return self.__table__.c[colname].type

        raise NameError(colname)

    def doc_dict(self, camel_case=False, columns=None):
        '''
        Convenience method to generate a dict from a model instance. It can automatically convert camel case keys
        to underscore equivalents.

        @param: camel_case: A boolean switch to convert the resulting dict keys to camel case.
        @param: columns: A list of (camelCased) columns that should be included in the result as keys.
        @param: renames: A dictionary of {'column_name': 'myCoolNewColumnName'} to use used like AS

        @return: An dict with all the columns of the model as keys and values.
        '''
        the_dict = self.to_dict(camel_case=camel_case, columns=columns)
        for key in the_dict:
            cc_key = underscore_to_camelcase(key) if not camel_case else key
            sqltype = self.find_type(cc_key)
            the_dict[key] = sqltype

        return the_dict

    def doc_dict_string(self, camel_case=False, columns=None):
        def _tabs(in_str):
            return in_str.replace('[t]', '    ')

        doc_dict = self.doc_dict(camel_case=camel_case, columns=columns)
        ret =  _tabs('A dict containing the following data representation. ::\n[t][t][t]{\n')
        for key in doc_dict:
            ret += _tabs('[t][t][t][t]{}.{} ({})\n'.format(self.__table__, camelcase_to_underscore(key), doc_dict[key]))
        ret += _tabs('[t][t][t]}')
        return(ret)

    def to_dict(self, camel_case=False, columns=None, renames={}):
        '''
        Convenience method to generate a dict from a model instance. It can automatically convert camel case keys
        to underscore equivalents.

        @param: camel_case: A boolean switch to convert the resulting dict keys to camel case.
        @param: columns: A list of (camelCased) columns that should be included in the result as keys.
        @param: renames: A dictionary of {'column_name': 'myCoolNewColumnName'} to use used like AS

        @return: An dict with all the columns of the model as keys and values.
        '''
        return_dict = {}
        for column in self.__table__.c:
            us_column_name = camelcase_to_underscore(column.name)
            if not columns or column.name in columns:
                if camel_case:
                    if renames.get(us_column_name):
                        return_dict[renames[us_column_name]] = getattr(self, us_column_name)
                    else:
                        return_dict[column.name] = getattr(self, us_column_name)
                else:
                    if renames.get(us_column_name):
                        return_dict[renames[us_column_name]] = getattr(self, us_column_name)
                    else:
                        return_dict[us_column_name] = getattr(self, us_column_name)

        return return_dict

    def to_json(self, columns=None):
        """
        Convenience method to generate a JSON object from a model instance. It will automatically convert camel case keys
        to underscore equivalents.

        @param: columns: A list of (camelCased) columns that should be included in the result as keys.

        @return: A JSON object with all the columns of the model as keys and values.
        """
        from json import loads # We need this import because our json_loads doesn't throw exceptions!
        my_dict = self.to_dict(camel_case=True, columns=columns)
        for key in my_dict:
            try:
                loaded = loads(my_dict[key])
                my_dict[key] = loaded
            except (TypeError, ValueError):
                # Not JSON... keep going.
                pass
        return json_dumps(my_dict)

    def update(self, **kwargs):
        """
        Convenience method for updating the attributes of a model instance using keyword-arguments. It will
        automatically convert camel-case keys to snake-case as needed, if a key still doesn't match an existing
        attribute after conversion then it is ignored.
        """
        for attr, value in kwargs.iteritems():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                snake_attr = camelcase_to_underscore(attr)
                if hasattr(self, snake_attr):
                    setattr(self, snake_attr, value)

        return self

    def validate(self):
        return {'success': True, 'message': 'The record is valid.'}


def execsql(query, params=(), session=None, log_query=False, return_rowcount=False, auto_commit=True):
    """Use self's dictionary cursor to run the query string with the params
    tuple. This method provides exception handling and returns a result
    based on the fetchall parameter.

    @param query: String SQL command (SELECT, INSERT, etc) that is to be
                  executed. Must contain any string format replacements
                  if they are required.
    @param params: Data structure which contains all string format
                   replacement values.
    @param session: An Optional SQLAlchemy Session to use.
    @param log_query: Boolean saying whether or not to log the executed query
                      to log/db.log.
    @param return_rowcount: Boolean, that if true, will return the number of
                            rows found in a tuple along with the result.
    @param auto_commit: Commit Changes to the databases
    @return: When fetchall=True, a list of dictionaries is returned (or
             []). Otherwise, a single dictionary is returned (or {}).
             If return_rowcount is True, then a tuple is returned with
             the first element being the result & the second being the
             number of rows or pages (if pagesize isn't 1)."""
    if session is None:
        session = Session

    conn = session.connection()
    result = conn.execute(query, params)

    rowcount = 0

    if log_query:
        try:
            last_executed = result.cursor._last_executed
            logging.info(last_executed)
        except AttributeError:
            logging.info('Could not log last query because cursor was not present.')

    if auto_commit:
        safe_commit(session)

    return (result, rowcount) if return_rowcount else result


def safe_commit(session=None, close_after=False):
    """This commit function will rollback the transaction if
    committing goes awry. Also will close the connection if
    boolean is passed.

    @param session: A SQLAlchemy Session instance to commit.
    @param close_after: Boolean saying whether or not to close the SQLAlchemy's
                        Session connection after committing."""
    global Session
    if session is None:
        session = Session

    try:
        session.commit()
    except (Exception, SQLAlchemyError):
        logging.exception("Session commit error")
        session.rollback()
        session.connection().invalidate()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        raise

    if close_after:
        session.close()