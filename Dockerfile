FROM python:3

EXPOSE 5000

RUN adduser --disabled-password --home=/home/ubuntu --gecos "" ubuntu
RUN echo "ubuntu ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo 'ubuntu:docker' | chpasswd

RUN apt-get update && apt-get install -yq git

RUN mkdir -p /tmp/logs/watchtower && touch /tmp/logs/watchtower/watch.log

WORKDIR /usr/src/www

RUN apt-get install -y libpq-dev

RUN pip install supervisor

COPY ./services/supervisord.conf /etc/supervisor/supervisord.conf
COPY services/watchtower.conf /etc/supervisor/conf.d/watchtower.conf
COPY ./services/startup.sh /etc/startup.sh

COPY . /usr/src/www

RUN chmod +x /etc/startup.sh

ENTRYPOINT ["/etc/startup.sh"]