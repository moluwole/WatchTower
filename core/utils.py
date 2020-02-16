"""

Core.utils is a module that contains several helper functions, 'one-liners'
and other useful miscellaneous functions.

@author: Oluwole Majiyagbe
@email: oluwole564@gmail.com

"""

import re
import simplejson
from uuid import uuid4


def uuid():
    """Returns a string instance of an universally unique identifier (UUID).

    @return: String UUID."""
    return str(uuid4())


def camelcase_to_underscore(name):
    """
    Converts a string to underscore. (Typically from camelcase.)
    @param name: The string to convert.
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)).lower()


def string_to_class_name_format(name):
    """
    Converts a string like 'test name' or 'test_name' to 'TestName'
    @param name: The String to convert
    """
    return ''.join(a.capitalize() for a in re.split('([^a-zA-Z0-9])', name) if a.isalnum())


def underscore_to_camelcase(name):
    """
    Converts a string to camelcase. (Typically from underscore.)
    @param name: The string to convert.
    """
    return re.sub(r'_([a-z])', lambda m: (m.group(1).upper()), name)


def json_dumps(python_object, dents=None, if_err=None, **kwargs):
    try:
        return simplejson.dumps(python_object, default=to_json, indent=dents, namedtuple_as_object=False, **kwargs)
    except (ValueError, TypeError):
        return simplejson.dumps(if_err or {})


def clean_file_name(file_name, remove_spaces=False):
    if not file_name:
        return ''

    elif not isinstance(file_name, str):
        try:
            file_name = str(file_name)
        except:
            return ''

    # Take out invalid characters
    file_name = file_name.translate(str.maketrans('<>:"\/|?*^', '          '))

    # Take out leading and trailing periods and spaces
    file_name = file_name.strip(' .')

    if remove_spaces:
        file_name = file_name.replace(' ', '')

    return file_name
