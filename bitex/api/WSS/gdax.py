# Import Built-Ins
import logging
import json
import threading
import time

# Import Third-Party
from websocket import create_connection, WebSocketTimeoutException
import requests
# Import Homebrew
from bitex.api.WSS.base import WSSAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class GDAXWSS(WSSAPI):
    def __init__(self, pairs=None, channels=None):
        super(GDAXWSS, self).__init__('wss://ws-feed.gdax.com', 'GDAX')
        self.conn = None
        self.channels = channels or []
        self._data_thread = None

        if pairs:
            self.pairs = pairs
        else:
            r = requests.get('https://api.gdax.com/products').json()
            self.pairs = [x['id'] for x in r]

    def start(self):
        super(GDAXWSS, self).start()

        self._data_thread = threading.Thread(target=self._process_data)
        self._data_thread.daemon = True
        self._data_thread.start()

    def stop(self):
        super(GDAXWSS, self).stop()

        self._data_thread.join()

    def _process_data(self):
        self.conn = create_connection(self.addr, timeout=4)
        payload = {
            'type': 'subscribe',
            'product_ids': self.pairs,
        }
        if self.channels:
            payload.update({'channels': self.channels})
        self.conn.send(json.dumps(payload))
        while self.running:
            try:
                data = json.loads(self.conn.recv())
            except (WebSocketTimeoutException, ConnectionResetError) as e:
                log.debug(e)
                self._controller_q.put('restart')

            if 'product_id' in data:
                self.data_q.put((data['type'], data['product_id'],
                                 data, time.time()))
        self.conn = None