# import python packages here
import os

# import 3rd party or framework level packages here
from flask import Blueprint

api = Blueprint('watchdog', __name__)

from routes import views


@api.before_request
def before_request():
    """Hook which is called before any request is called. Check for JWT here"""
    pass
