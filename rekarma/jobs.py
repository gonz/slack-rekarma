# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests

from rekarma.slack import get_rekarma_text


def send_delayed_response(response_url=None):
    rekarma_text = get_rekarma_text()
    if response_url:
        requests.post(response_url, json={'text': rekarma_text})
    return rekarma_text
