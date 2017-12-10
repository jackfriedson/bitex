# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class PlnxFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        data = data[args[1]]
        return (data['highestBid'], data['lowestAsk'], None, None, None, None,
                data['last'], None, None)

    @staticmethod
    def order(data, *args, **kwargs):
        return data.get('orderNumber')

    @staticmethod
    def cancel(data, *args, **kwargs):
        return True if data.get('success') else False

    @staticmethod
    def withdraw(data, *args, **kwargs):
        if not data:
            return False

        return {
            'currency': kwargs.get('currency'),
            'amount': args[1],
            'target_address': args[2],
        }
