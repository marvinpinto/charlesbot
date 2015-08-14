# CharlesBOT

![CharlesBOT][3]

CharlesBOT is a Python bot written to take advantage of Slack's [Real Time
Messaging][1] API. It is very much in development at the moment so bear with me
and it'll get there eventually :)

[![Build Status](https://travis-ci.org/marvinpinto/charlesbot.svg?branch=master)](https://travis-ci.org/marvinpinto/charlesbot)
[![Coverage Status](https://coveralls.io/repos/marvinpinto/charlesbot/badge.svg?branch=master&service=github)](https://coveralls.io/github/marvinpinto/charlesbot?branch=master)
[![Docker Repository on Quay.io](https://quay.io/repository/marvin/charlesbot/status "Docker Repository on Quay.io")](https://quay.io/repository/marvin/charlesbot)



## What does this thing even do?!

Well, not very much so far. Poor robot :(

#### Broadcast Message

Send a `!wall` broadcast message to all channels Charles has been invited to!

![wall][4]

#### Get some `!help`

![help][5]

#### Who's `!oncall`

![oncall][10]



## Cool! So how do I run this thing??

First off, create a `config.ini` file similar to [config.ini.example][8].
You'll need a [Slack Bot Token][2], if you don't already have one.

You have two options to run CharlesBOT:

1. Using PyPI
1. Docker

If you already have a [Docker][9] based infrastructure, that might be the easiest
option for you to get going!


### PyPI

#### Prerequisites

- Python 3.4.3 (and related tooling including `pyvenv`)

#### Installing from PyPI

```bash
export CHARLESBOT_SETTINGS_FILE=/path/to/your/config.ini
pyvenv-3.4 charlesbot-env
charlesbot-env/bin/pip install git+https://github.com/slackhq/python-slackclient.git@ba71b24603f63e54e704d0481812efcd9f7b8c14
charlesbot-env/bin/pip install charlesbot
```

The reason for installing `slackclient` straight from GitHub here is because
the published (PyPI) version of `slackclient` does not contain the
modifications necessary to work with Python 3.x. I'll get this updated as and
when they publish a newer version of `slackclient`.

#### Running CharlesBOT

```bash
export CHARLESBOT_SETTINGS_FILE=/path/to/your/config.ini
charlesbot-env/bin/charlesbot
```

### Docker

```bash
docker run \
  --rm \
  -it \
  -e "CHARLESBOT_SETTINGS_FILE=/config.ini" \
  -v /path/to/your/config.ini:/config.ini \
  quay.io/marvin/charlesbot
```



## How can I contribute to this awesome project?!

First off:

![Thank You][6]

Now get to work!

1. Fork this repo
1. Add some cool stuff!
1. Write some tests!
1. Submit a PR

A few make targets that might be useful to you:
- `make checkstyle`
- `make test`
- `make run`



## The Why's

My original motivation behind this project was to get my hands dirty with
Python 3 + asyncio and it's been a neat learning experience.

#### `python-slackclient`

This currently uses the [python-slackclient][7] library to handle the
underlying websocket communication but I intend on replacing that with an
asyncio native websocket solution eventually.

#### Plugin system

The "plugin" architecture was designed to be drop-in-place without having to
touch the core system, but it isn't where I would like it to be and still needs
a bit of work. And that's okay!

The "queue + worker" system of delivering messages to each plugin is an
experiment in how much this design will scale before it starts hogging CPU
resources and just being generally slow. Let's see how it goes!

#### Configuration management

One thing that I would like to axe eventually is the way configuration is
read/written to. I am *not* a fan of supplying config files on the command
line, and the other option of "everything gets configured through environment
variables" is also a bit extreme. Relying on a user to supply a million
environment variables can get quite ugly (imagine a chain of 50 + `-e
"VAR1=foo"` docker arguments!).

I am hoping to explore an architecture where the basic amount of information
needed to get go is read from environment variables, and the rest is read from
a key-value store of sorts (DynamoDB perhaps?). This would allow for things
such as post-launch configuration and scales nicely if/when the robot is
restarted as users would not need to go in and reconfigure their
plugin-specific settings.



## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (MIT).



[1]: https://api.slack.com/rtm
[2]: https://my.slack.com/services/new/bot
[3]: /images/logo.png?raw=true
[4]: /images/wall.png?raw=true
[5]: /images/help.png?raw=true
[6]: http://i.giphy.com/5xtDarmwsuR9sDRObyU.gif
[7]: https://github.com/slackhq/python-slackclient
[8]: /config.ini.example
[9]: https://www.docker.com
[10]: /images/oncall.png?raw=true
