# coding=utf-8
import sys

sys.path.append('/usr/lib/python3/dist-packages')

import logging
from datetime import datetime
from json import dumps, loads
from operator import itemgetter
from time import sleep
from typing import Dict

import websocket
from pytify.strategy import get_pytify_class_by_platform
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

        self._spotify = get_pytify_class_by_platform()()
        self._spotify_playing = False

    def run(self):
        while True:
            self._client.run_forever()

            sleep(1)

    def _on_message(self, ws: WebSocketApp, message):
        data = loads(message)

        if data.get('matches'):
            self._matches = data.get('matches')  # type: Dict[int, Dict]

        if data.get('match'):
            match = data.get('match')
            self._matches[match.get('id')] = match

        if not self.can_play_music():
            logger.info('{} please stop the music'.format(datetime.now()))
            self._toggle_spotify_play(state=False)
        else:
            logger.info('{} little party never killed nobody!'.format(datetime.now()))
            self._toggle_spotify_play(state=True)

    def _toggle_spotify_play(self, state):
        if self._spotify_playing == state:
            return

        try:
            self._spotify.play_pause()
            self._spotify_playing = state
        except Exception as e:
            logger.exception(e)
            self._spotify = get_pytify_class_by_platform()()
            try:
                self._spotify.play_pause()
                self._spotify_playing = state
            except Exception:
                logger.error('Cannot connect to spotify.')

    def can_play_music(self):
        states = set(map(itemgetter('state'), self._matches.values()))
        logger.info(states)
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
