import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

# Redis URL setting in env REDISTOGO_URL or REDISTOGO_URL or default to localhost
REDIS_URL = os.environ.get('REDISTOGO_URL',
                           os.environ.get('REDIS_URL', 'localhost:6379'))

redis_server = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(redis_server):
        worker = Worker(map(Queue, listen))
        worker.work()
