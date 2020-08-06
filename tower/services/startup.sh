#!/bin/bash

#cd into the Code directory
cd /usr/src/www || exit

# Install the Python package
pip install --editable .

mkdir /var/log/supervisord/

while true; do
  # Run Migrations
  watchshell run:migration
  RESULT=$?
  if [[ $RESULT -eq 0 ]]; then
    # Create RediSearch Index
    python controllers/tower.py
    break
  fi

   echo Unable to create Database at this time. Trying again in 5 seconds
   sleep 5
done

if [ "$1" == 'prod' ]; then
  exec export FLASK_ENV = production
fi

# execute Supervisor to launch the wsgi app with gunicorn
exec /usr/local/bin/supervisord -c /etc/supervisor/supervisord.conf
