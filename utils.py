import requests
import json
from config import keys



class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base.upper()} \nПовторить попытку: /convert')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote.upper()} \nПовторить попытку: /convert')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base.upper()} \nПовторить попытку: /convert')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount.upper()} \nПовторить попытку: /convert')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base












