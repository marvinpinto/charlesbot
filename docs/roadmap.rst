Roadmap
=======

``python-slackclient``
----------------------

Charlesbot currently uses the python-slackclient__ library to handle the
underlying websocket communication. I am not *entirely* a fan of this library
and I intend on replacing it with a native asyncio solution.

__ https://github.com/slackhq/python-slackclient

Plugin Architecture
-------------------

The plugin architecture for this project has come a long way since the first
few iterations. It is designed such that plugins can be dropped in place
without having to modify the core code-base.

This is what the `current architecture`__ looks like.

__ architecture.html

The "queue + worker" system of delivering messages to each plugin is an
experiment in how much this design will scale, before it starts hogging
resources and being generally slow. We'll see how it goes!

Configuration Management
------------------------

One thing that I would like to axe eventually is the way configuration is
read/written to. I am *not* a fan of supplying config files on the command
line.

Another alterative to supplying config files on the command line is the
"everything gets configured through environment variables" (`12 factor-ish`__)
approach. I feel like this approach is taking it to the other extreme and there
must be a middle ground somewhere.

I feel like relying on an operator to supply a slew of environment variables on
the command line can get unwieldy fast! (imagine a chain of 50+ ``-e
"VAR=foo"`` docker arguments!)

I am hoping to explore an architecture where the basic amount of information
needed to get going is read from environment variables, and the rest are read
from a key-value store of sorts. This would allow for things such as
post-launch configuration and this approach scales nicely if/when Charlesbot is
restarted as users would not need to go in and reconfigure their
plugin-specific settings.

__ http://12factor.net
