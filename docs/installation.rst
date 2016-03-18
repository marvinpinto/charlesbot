Installation
============

.. note::

    Since Charlesbot is a published PyPI package, you have the choice of
    installing and running it whichever way works for you. If you already have
    a Docker__ environment setup, I highly recommend you use that to run your
    Charlesbot instance. It will make your life a whole lot easier.

    The PyPI way is perfectly reasonable, too, should you choose!

__ https://www.docker.com

Config File
-----------

You will first need to create a ``config.yaml`` file similar to:

.. code-block:: yaml

    main:
      slackbot_token: 'xoxb-...'
      enabled_plugins:

You will also need a valid `Slack Bot Token`__, if you don't already have one.

__ https://my.slack.com/services/new/bot

For the most up-to-date example, see the config.yaml.example__ file in the
Charlesbot source tree.

__ https://github.com/marvinpinto/charlesbot/blob/master/config.yaml.example


Plugins
-------

By default, Charlesbot does not ship with any useful plugins. You will need to
install and enable these plugins separately.


Installation Using PyPI
-----------------------

Requirements
^^^^^^^^^^^^

- Python 3.4.3
- pyvenv__

__ https://docs.python.org/3.4/library/venv.html

Base Installation
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    export CHARLESBOT_SETTINGS_FILE=/path/to/your/config.yaml
    pyvenv-3.4 charlesbot-env
    charlesbot-env/bin/pip install charlesbot
    # charlesbot-env/bin/pip install charlesbot-plugin-xx..
    charlesbot-env/bin/charlesbot

Installation Using Docker
-------------------------

Requirements
^^^^^^^^^^^^

- Docker__

__ https://www.docker.com

Sample Dockerfile
^^^^^^^^^^^^^^^^^

.. code-block:: Dockerfile

    FROM ubuntu:14.04

    # Add the trusty-proposed repo
    RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty-proposed restricted main multiverse universe" >> /etc/apt/sources.list

    # Set up the environment
    RUN mkdir /src

    # Install python
    RUN apt-get update \
      && apt-get install -y g++ git python3 python3-dev libmysqlclient-dev python3.4-venv \
      && apt-get clean autoclean \
      && apt-get autoremove -y --purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
      && rm -rf /var/lib/{apt,dpkg,cache,log}/

    # Install charlesbot
    RUN cd /src \
      && pyvenv-3.4 env \
      && env/bin/pip install charlesbot \
      # && env/bin/pip install charlesbot-plugin-xx... \
      && echo "Installation complete"

    ENTRYPOINT ["/src/env/bin/charlesbot"]

Build and run your local docker container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    docker build -t local/charlesbot .
    docker run \
      -d \
      -e "CHARLESBOT_SETTINGS_FILE=/config.yaml" \
      -v /path/to/your/config.yaml:/config.yaml \
      -v /etc/localtime:/etc/localtime:ro  \
      --name="charlesbot" \
      local/charlesbot
