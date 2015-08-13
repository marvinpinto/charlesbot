FROM ubuntu:14.04

# Add the trusty-proposed repo
RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty-proposed restricted main multiverse universe" >> /etc/apt/sources.list

# Set up the environment
RUN mkdir /src
ADD ./requirements.txt /src/requirements.txt

# Install python
RUN apt-get update \
  && apt-get install -y git python3 python3-dev libmysqlclient-dev python3.4-venv \
  && apt-get clean autoclean \
  && apt-get autoremove -y --purge \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Install charlesbot
RUN cd /src \
  && pyvenv-3.4 env \
  && env/bin/pip install -r requirements.txt

ADD ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
