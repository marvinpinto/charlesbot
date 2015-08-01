# CharlesBOT

![CharlesBOT][3]

CharlesBOT is a Python bot written to take advantage of Slack's [Real Time
Messaging][1] API. It is very much in development at the moment so bear with me
and it'll get there eventually :)

[![Build Status](https://travis-ci.org/marvinpinto/charlesbot.svg?branch=master)](https://travis-ci.org/marvinpinto/charlesbot)



## What does this thing even do?!

Well, not very much so far. Poor robot :(

#### Broadcast Message

Send a `!wall` broadcast message to all channels Charles has been invited to!

![wall][4]

#### Get some `!help`

![help][5]



## Cool! So how do I run this thing??

This part is a bit hairy at the moment since it involves cloning this repo and
running from source :(

I plan on publishing this to PyPI and also creating a Docker container so you
don't need to worry about the source unless you want to!  (That's what I hope)

#### Things you'll need:

- Python 3.4.3 (and related tooling including `pyvenv`)
- [Slack Bot Token][2]

#### Running CharlesBOT locally:

First create a localy `development.ini` file using the `config.ini.example`
file as a reference.

```bash
make install
make run
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



## The Why's

My original motivation behind this project was to get my hands dirty with
Python 3 + asyncio and it's been a neat learning experience. This currently
uses the [python-slackclient][7] library to handle the underlying websocket
communication but I intend on replacing that with an asyncio native websocket
solution eventually.

The "plugin" architecture was designed to be drop-in-place without having to
touch the core system, but it isn't where I would like it to be and still needs
a bit of work. And that's okay!

The "queue + worker" system of delivering messages to each plugin is an
experiment in how much this design will scale before it starts hogging CPU
resources and just being generally slow. Let's see how it goes!



## License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (MIT).



[1]: https://api.slack.com/rtm
[2]: https://my.slack.com/services/new/bot
[3]: /images/logo.png?raw=true
[4]: /images/wall.png?raw=true
[5]: /images/help.png?raw=true
[6]: http://i.giphy.com/5xtDarmwsuR9sDRObyU.gif
[7]: https://github.com/slackhq/python-slackclient
