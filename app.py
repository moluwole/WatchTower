#!/usr/bin/env python

import os

from flask import Flask

from routes import api
from core.config import app_configuration

app = Flask(__name__)
app_configuration(app)
app.secret = os.getenv('APP_KEY', '')


host = os.getenv('APP_HOST', '0.0.0.0')
port = 5000
debug = os.getenv('APP_DEBUG', False)

if __name__ == '__main__':
    app.register_blueprint(api)

    app.run(host=host, port=port, debug=debug)
