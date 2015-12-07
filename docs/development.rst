Development
===========

Requirements
------------

- Python 3.4.3
- pyvenv__

__ https://docs.python.org/3.4/library/venv.html

Running Charlesbot locally
--------------------------

Clone the Charlesbot source code locally:

.. code-block:: text

    git clone https://github.com/marvinpinto/charlesbot.git

Inside the ``charlesbot`` source tree, create a ``development.yaml`` file that
looks something like:

.. code-block:: yaml

    main:
      slackbot_token: 'xoxb-...'
      enabled_plugins:

Note that you will need a valid `Slack Bot Token`__, if you don't already have
one.

__ https://my.slack.com/services/new/bot

Install Charlesbot in a virtualenv:

.. code-block:: text

    make install

Run Charlesbot in debug mode:

.. code-block:: text

    make run

Contributing
------------

#. Fork the Charlesbot__ repository on GitHub

#. Write some cool stuff! (fix some bugs, add new features, update
   documentation, etc)

#. Write some (relevant) tests!

#. Submit a `Pull Request`__

__ https://github.com/marvinpinto/charlesbot.git
__ https://help.github.com/articles/using-pull-requests/

Running tests locally
---------------------

Check for style violations:

.. code-block:: text

    make checkstyle

Run the unit tests locally:

.. code-block:: text

    make test
