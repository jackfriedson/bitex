# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter

log = logging.getLogger(__name__)


def format_currency(currency):
    currency_map = {'BCC': 'BCH'}
    return currency_map.get(currency, currency)


class BtrxFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        data = data['result'][0]
        return (data['Bid'], data['Ask'], data['High'], data['Low'], None, None,
                data['Last'], data['Volume'], None)

    @staticmethod
    def order(data, *args, **kwargs):
        if data['success']:
            return data['result']['uuid']
        else:
            return False

    @staticmethod
    def order_book(data, *args, **kwargs):
        if data['success']:
            return data['result']

    @staticmethod
    def cancel(data, *args, **kwargs):
        return True if data['success'] else False

    @staticmethod
    def balance(data, *args, **kwargs):
        if data['success']:
            return {
                format_currency(x['Currency']): x['Available']
                for x in data['result']
            }

    @staticmethod
    def deposit(data, *args, **kwargs):
        if data['success']:
            return data['result']['Address']

    @staticmethod
    def withdraw(data, *args, **kwargs):
        result = {
            'currency': kwargs.get('currency'),
            'amount': args[1],
            'target_address': args[2],
        }

        if data['success']:
            result.update({'id': data['result']['uuid']})
            return result
