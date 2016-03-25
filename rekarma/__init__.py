# -*- coding: utf-8 -*-
import os
from flask import Flask
import redis

app = Flask(__name__)
redis_server = redis.from_url(os.environ.get("REDIS_URL"))

import rekarma.views
