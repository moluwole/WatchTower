"""

Core.utils is a module that contains several helper functions, 'one-liners'
and other useful miscellaneous functions.

@author: OLuwole Majiyagbe
@contact: oluwole.majiyagbe@firstpavitech.com
@organization: First Pavilion

"""

import re
import collections
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
    """Takes a value (list, dictionary, etc) that is JSON serializable, and
    dumps it as a string. Indentation is set to 4 spaces by default.

    @param python_object: A native Python instance (list, dictionary, etc).
    @param dents: The number of spaces used for indentation in the
                  JSON-formatted string that is returned.
    @param if_err: What is returned if an error occurs.
    @param kwargs: Any other keyworded args are then passed to simplejson.dumps directly.
    @return: A JSON-formatted string."""
    def to_json(an_object):
        """
        Adding in custom serialization for Date objects.

        """
        from datetime import date, datetime, time
        if (isinstance(an_object, date) or
                isinstance(an_object, datetime) or
                isinstance(an_object, time)):
            return str(an_object)
        elif isinstance(an_object, collections.Set):
            return list(an_object)
        elif hasattr(an_object, 'to_dict'):
            return an_object.to_dict()
        elif hasattr(an_object, '__call__'):
            return ''
        raise TypeError(repr(an_object) + ' is not JSON serializable')

    try:
        return simplejson.dumps(python_object, default=to_json, indent=dents, namedtuple_as_object=False, **kwargs)
    except (ValueError, TypeError):
        return simplejson.dumps(if_err or {})


def clean_file_name(file_name, remove_spaces=False):
    """Makes a string safe to use as a file-name
       Removes any characters that are dangerous for file names
       on windows, mac, or linux and replaces them with spaces

       file_name: the ascii string to be cleaned
       returns: a string that is safe to use as a file name"""

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
