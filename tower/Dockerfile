FROM python:3.8

EXPOSE 5000

RUN apt-get -y update && apt-get -y clean

RUN apt-get install -y libpq-dev

RUN adduser --disabled-password --home=/home/ubuntu --gecos "" ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo 'ubuntu:docker' | chpasswd

RUN mkdir -p /tmp/logs/watchtower && touch /tmp/logs/watchtower/watch.log
RUN mkdir /var/log/supervisord/

WORKDIR /usr/src/www

COPY services/supervisord.conf /etc/supervisor/supervisord.conf
COPY services/watchtower.conf /etc/supervisor/conf.d/watchtower.conf

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/www