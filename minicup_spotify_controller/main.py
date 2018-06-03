# coding=utf-8
import logging

from minicup_spotify_controller.controller import SpotifyController

try:
    import thread
except ImportError:
    import _thread as thread

LIVE_SERVICE_URL = 'wss://live.minicup.tatranlitovel.cz/ws/live'
LIVE_SERVICE_URL = 'ws://localhost:8888/ws/live'

if __name__ == "__main__":
    controller = SpotifyController(
        url=LIVE_SERVICE_URL,
        category_id=11
    )

    ws_logger = logging.getLogger('websocket')
    ws_logger.disabled = True

    controller.run()
