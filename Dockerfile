FROM python:3.6

EXPOSE 5000

WORKDIR /usr/src/www

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs

COPY . /usr/src/www

RUN pip install --editable . && chmod u+x app.py && npm install -g nodemon

CMD ["./app.py"]