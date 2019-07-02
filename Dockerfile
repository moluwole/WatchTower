FROM python:3

EXPOSE 5000

EXPOSE 5050

WORKDIR /usr/src/www

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs

COPY . /usr/src/www

RUN cp .env.example .env

RUN apt-get install -y libpq-dev

RUN chmod u+x app.py && npm install -g nodemon

RUN export FLASK_APP=app.py && pip install --editable .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5050"]