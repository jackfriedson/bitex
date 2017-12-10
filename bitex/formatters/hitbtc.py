# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class HitBtcFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], data['open'],
                None, data['last'], data['volume'], None)

    @staticmethod
    def balance(data, *args, **kwargs):
        return {x['currency']: x['available'] for x in data}

    @staticmethod
    def deposit(data, *args, **kwargs):
        return data['address']

    @staticmethod
    def withdrawal(data, *args, **kwargs):
        if 'id' not in data:
            return False

        return {
            'currency': kwargs.get('currency'),
            'amount': args[1],
            'target_address': args[2],
        }

    @staticmethod
    def order(data, *args, **kwargs):
        return data.get('id')
