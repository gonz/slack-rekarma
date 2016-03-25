# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import datetime
import time
from collections import defaultdict
from itertools import chain

from slacker import Slacker
import redis


# TODO: Make this configurable to include custom emojis and define better defaults
DEFAULT_REACTION_KARMA = 1
CUSTOM_REACTION_KARMA = {
    # Very positive reactions
    '+1': +2,
    'heart': +2,
    'clap': +2,
    'joy': +2,
    # Negative reactions
    '-1': -2,
    'broken_heart': -1,
}

DEFAULT_RESPONSE_CACHE_TTL = 60 * 5


def get_reaction_karma(reaction_name):
    return CUSTOM_REACTION_KARMA.get(reaction_name, DEFAULT_REACTION_KARMA)


def get_rekarma(slack_api_key=None, message_max_days=None):
    if slack_api_key is None:
        slack_api_key = os.environ.get('SREK_SLAK_API_KEY')
    if message_max_days is None:
        message_max_days = os.environ.get('SREK_MESSAGE_MAX_DAYS', 30)

    slack = Slacker(slack_api_key)

    username_map = {m['id']: m['name'] for m in slack.users.list().body['members']}
    since = time.mktime(
        (datetime.datetime.utcnow() - datetime.timedelta(days=message_max_days)).timetuple()
    )
    user_reactions = defaultdict(lambda : defaultdict(int))

    for channel in slack.channels.list().body['channels']:
        latest = None
        has_more = True
        while has_more:
            m =  slack.channels.history(channel['id'], oldest=since,
                                        latest=latest, count=1000).body
            for message in m['messages']:
                latest = message['ts']
                if not 'user' in message or not 'reactions' in message:
                    continue
                for r in message['reactions']:
                    user_reactions[message['user']][r['name']] += r['count']
            has_more = m['has_more']

    user_rekarma = defaultdict(int)
    for user_id, reactions in user_reactions.iteritems():
        for rname, rcount in reactions.iteritems():
            user_rekarma[user_id] += get_reaction_karma(rname) * rcount

    return [
        {'username': username_map[user_id],
         'rekarma': user_rekarma[user_id],
         'reactions': sorted(user_reactions[user_id].keys())}
        for user_id, rekarma in user_rekarma.iteritems()
    ]



def get_rekarma_text():
    redis_server = redis.from_url(os.environ.get("REDIS_URL"))
    if not redis_server.get('rekarma:cache:text'):
        rekarma = get_rekarma()
        rekarma_text = '\n'.join(chain(
            ['Karma for all users:'],
            ('  #{i} *{username}* {rekarma} points reactions: '.format(i=i + 1, **r) +
             ' '.join([':{}:'.format(name) for name in r['reactions']])
             for i, r in enumerate(sorted(rekarma, reverse=True, key=lambda x: x['rekarma'])))
        ))
        redis_server.set('rekarma:cache:text', rekarma_text)
        redis_server.expire('rekarma:cache:text', DEFAULT_RESPONSE_CACHE_TTL)
    return redis_server.get('rekarma:cache:text')
