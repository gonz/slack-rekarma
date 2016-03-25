# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from flask import Flask, request, Response
from rq import Queue

from rekarma import app, redis_server
from rekarma.jobs import send_delayed_response
from rekarma.slack import get_rekarma_text


@app.route('/rekarma', methods=['GET'])
def rekarma():
    if not redis_server.get('rekarma:cache:text'):
        # Not in cache, this response will take > 3000ms. Using Slack delayed response
        # See: https://api.slack.com/slash-commands#responding_to_a_command
        response_url = request.values.get('response_url')

        queue = Queue(connection=redis_server)
        job = queue.enqueue(send_delayed_response, response_url)

        return Response(u'Karma? OK, give me a second...',
                        content_type='text/plain; charset=utf-8')
    else:
        return Response(get_rekarma_text(), content_type='text/plain; charset=utf-8')
