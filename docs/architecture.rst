Architecture
============

At its core, Charlesbot essentially works as follows:

.. image:: _static/images/charlesbot_architecture.png
   :alt: Charlesbot Architecture

When a message comes in through a Slack websocket, ``robot.py`` delivers a copy
of the message to each Charlesbot plugin. This is done by pushing this message
onto each plugin's queue, at which point the plugin is free to consume the
message on its own schedule.

This approach decouples the processing of a message from the receiving of a
message, which helps in a scenario where a channel is flooded with more
incoming messages than a plugin is able to handle (in a timely manner).

Abstract Base Class
-------------------

The abstract base class ``BasePlugin`` handles the bulk of the message
coordination which allows you to write your plugins with minimum boiler plate.

In order for this to work, you will need to inherit from ``BasePlugin`` and
implement the plugin logic using at minimum the following two abstract methods:

.. code-block:: python

    def get_help_message(self):
        pass

    def process_message(self, message):
        pass
