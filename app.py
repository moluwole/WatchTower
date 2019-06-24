#!/usr/bin/env python
import os
import logging

from vibora import Vibora

from routes.views import create_server

app = Vibora()

if __name__ == '__main__':
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = 5000
    debug = os.getenv('APP_DEBUG', False)

    app = create_server(app)
    logging.info("Starting WatchDog...")

    app.run(host=host, port=port, debug=debug)
