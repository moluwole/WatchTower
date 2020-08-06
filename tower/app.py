#!/usr/local/bin/python

import os
import subprocess
import logging

from flask import Flask, request

from routes import api
from core.config import app_configuration

app = Flask(__name__)
app_configuration(app)
app.secret = os.getenv('APP_KEY', '')

host = os.getenv('APP_HOST', '0.0.0.0')
port = 5000
debug = os.getenv('APP_DEBUG', False)


#######################################################################
#               REGISTER APPLICATION BLUEPRINTS HERE                  #
#######################################################################

app.register_blueprint(api)

#######################################################################
#               END BLUEPRINTS REGISTRATIONS                          #
#######################################################################


########################################################################
#   This is the route for CI/CD. i.e. pulling and pushing to tower    #
#   Do not edit this route in anyway                                   #
########################################################################

@app.route('/ci-route')
def reload():
    repo = request.args.get('repo')
    if request.args.get('entry') == 'XXX':
        try:
            subprocess.call(['git checkout {0}'.format(repo)])

            subprocess.call(['git pull origin {0}'.format(repo)])
            return 'success'
        except OSError as e:
            print(e)
            logging.error(e.strerror)
            return 'fail'
    else:
        return 'Entry Level Error'


#######################################################
#                END CI/CD ROUTE                      #
#######################################################

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
