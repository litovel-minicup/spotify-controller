# coding=utf-8
import logging
from datetime import datetime
from json import dumps, loads
from operator import itemgetter
from time import sleep
from typing import Dict

import websocket
from websocket import WebSocketApp

websocket.enableTrace(True)

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


class SpotifyController(object):
    def __init__(self, url, category_id):
        self._client = WebSocketApp(
            url=url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self._category_id = category_id
        self._matches = {}  # type: Dict[int, Dict]

    def run(self):
        while True:
            self._client.run_forever()

            sleep(1)
            self._client.run_forever()

    def _on_message(self, ws: WebSocketApp, message):
        data = loads(message)

        if data.get('matches'):
            self._matches = data.get('matches')  # type: Dict[int, Dict]

        if data.get('match'):
            match = data.get('match')
            self._matches[match.get('id')] = match

        if not self.can_play_music():
            print(datetime.now(), 'please stop the music')
        else:
            print(datetime.now(), 'little party never killed nobody!')

    def can_play_music(self):
        states = set(map(itemgetter('state'), self._matches.values()))
        logger.debug(states)
        return not ('half_first' in states or 'half_second' in states)

    def _on_error(self, ws: WebSocketApp, error):
        logger.error(error)

    def _on_close(self, ws: WebSocketApp):
        logging.info('Closed.')

    def _on_open(self, ws: WebSocketApp):
        ws.send(dumps(dict(
            action='subscribe_category',
            category=self._category_id
        )))


__all__ = [
    'SpotifyController'
]
