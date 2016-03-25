# -*- coding: utf-8 -*-
import os
from flask import Flask
import redis

# Redis URL setting in env REDISTOGO_URL or REDISTOGO_URL or default to localhost
REDIS_URL = os.environ.get('REDISTOGO_URL',
                           os.environ.get('REDIS_URL', 'localhost:6379'))

app = Flask(__name__)
redis_server = redis.from_url(REDIS_URL)

import rekarma.views
