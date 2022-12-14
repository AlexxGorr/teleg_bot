import requests
import json
from config import currency



class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base.upper()} \nПовторить попытку: /convert')
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote.upper()} \nПовторить попытку: /convert')
        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base.upper()} \nПовторить попытку: /convert')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount.upper()} \nПовторить попытку: /convert')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]] * amount

        return total_base


class CryptoRating:
    @staticmethod
    def rating(quote: str):
        lst_base = ''
        for i in currency.values():
            lst_base = lst_base + i + ','
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote.upper()} \nПовторить попытку: /rate')

        base_ticker = lst_base

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total = json.loads(r.content)

        return total

















