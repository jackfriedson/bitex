# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class GdaxFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], None, None, None, None, data['price'],
                data['volume'], data['time'])

    @staticmethod
    def balance(data, *args, **kwargs):
        return {acct['currency']: acct['available'] for acct in data}

    @staticmethod
    def withdraw(data, *args, **kwargs):
        data.update({'target_address': args[2]})
        return data

    @staticmethod
    def order(data, *args, **kwargs):
        if 'id' not in data:
            return False
        return data['id']
