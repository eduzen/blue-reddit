[![Build Status](https://travis-ci.org/eduzen/blue-reddit.svg?branch=master)](https://travis-ci.org/eduzen/blue-reddit)
# blue-reddit

Hello! Welcome to this news crawler from Reddit. In order to use this project you will need [Python](http://python.org)
and [Redis](https://redis.io).
I've chosen `Django` and `Django-rest-framework` because I agree with two topics of Django:
> The web framework for perfectionists with deadlines.
and
> Django makes it easier to build better Web apps more quickly and with less code.

First of all, there is not a supreme framework, each framework has lots of advantages and disadvantages.
So, why do I choose Django? Because it has a big community that helps you to develop fast and with the confidence
of standing over the shoulders of a robust framework with a lot of capabilities. So if you know that
your project will grow and you don't want to invent the wheel every time, Django is a good choice.

Django-rest-framework is one of the most popular plugins for API REST in Django and it comes with
Web browsable API, a lot of documentation, serializations and it fits the philosophy of the Django community.

But if you need to crawl a big site like Reddit.com you can't do it with the times of the web.
You have to wait too much to try to get what you want. So, you need to do it with concurrency or parallelism.
And not only that, you need to do it well, because it can be a stressful task for your machine.
That's why I've chosen `Celery` and `Redis`. I didn't chose Rabbitmq, because I think it's too much for
this repo.


## Installation

If you already have `Python 3.6`. You need to create a virtualenv with python 3:
```
virtualenv -p python3.6 venv
```

With the virtualenv activated, you will need to install our dependecies:
```
pip install -r requirements.txt

# or for developers:

pip install -r requirements_dev.txt
```

This project works with redis, so you need to install it:
```
# for OSX
brew install redis
brew services start redis

# ubuntu
sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server
```

To test if redis is up:
```
redis-cli ping
```
For other OS, you can dowload it from: [https://redis.io/download](https://redis.io/download)

## Configuration:

You have to change `bproject/bproject/settings.py` and add your own reddit credentials.
```python
# PRAW CONFIG

CLIENT_ID = "fruta"
CLIENT_SECRET = "foo"
USER_AGENT = "my user agent"
USERNAME = 'bar'
PASSWORD = 'anypass'
```

## Usage:

You can read documentation in `localhost:8000/docs` (also you can interact with the API):
![Image](docs/docs.png?raw=true)

and it also you can use the browsable API thanks to `django-rest-framework`:
![Image](docs/rest.png?raw=true)
