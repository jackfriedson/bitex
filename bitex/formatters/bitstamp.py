# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class BtstFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], data['open'],
                None, data['last'], data['volume'], data['timestamp'])

    @staticmethod
    def balance(data, *args, **kwargs):
        return {
            cur: data[cur.lower() + '_available']
            for cur in ['BTC', 'ETH', 'LTC', 'XRP', 'USD', 'EUR']
        }

    @staticmethod
    def deposit(data, *args, **kwargs):
        if kwargs.get('currency') != 'BTC':
            data = data['address']
        return data

    @staticmethod
    def withdraw(data, *args, **kwargs):
        if not data:
            return False

        return {
            'currency': kwargs.get('currency'),
            'amount': args[1],
            'target_address': args[2]
        }

    @staticmethod
    def order(data, *args, **kwargs):
        status = data.get('status')
        if status and status == 'error':
            return False

        return data['id']
