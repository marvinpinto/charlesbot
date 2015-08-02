FROM ubuntu:14.04

# Add the trusty-proposed repo
RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty-proposed restricted main multiverse universe" >> /etc/apt/sources.list

# Install python
RUN apt-get update \
  && apt-get install -y git python3 python3-dev libmysqlclient-dev python3.4-venv \
  && apt-get clean autoclean \
  && apt-get autoremove -y --purge \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Install charlesbot
RUN mkdir /src \
  && cd /src \
  && pyvenv-3.4 env \
  && env/bin/pip install git+https://github.com/slackhq/python-slackclient.git@ba71b24603f63e54e704d0481812efcd9f7b8c14 \
  && env/bin/pip install charlesbot

ADD ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
