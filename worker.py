import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_server = redis.from_url(os.environ.get('REDISTOGO_URL',
                                             os.environ['REDIS_URL']))

if __name__ == '__main__':
    with Connection(redis_server):
        worker = Worker(map(Queue, listen))
        worker.work()
