import json
import requests
import telebot
from telebot import types


def key_markup(quote = True):
    but_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    buttons = []
    for val in keys.keys():
        if val != quote:
            buttons.append(types.KeyboardButton(val.capitalize()))

    but_markup.add(*buttons)
    return but_markup


TOKEN = '5487683906:AAED5AuLe4wU14cR2THvtQpXCvh5T2y5e9I'

bot = telebot.TeleBot(TOKEN)

keys = {
        'биткоин': 'BTC',
        'эфириум': 'ETH',
        'фунт': 'GBP',
        'доллар': 'USD',
        'рубль': 'RUB',
        'евро': 'EUR',
        'юань': 'CNY',
        'франк': 'CHF',
        'крона': 'DKK'
        }



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



@bot.message_handler(commands = ['rate'])
def valute_choice(message: telebot.types.Message):
    text = 'Выбери валюту, чтобы узнать курс: '
    bot.send_message(message.chat.id, text, reply_markup = key_markup())
    bot.register_next_step_handler(message, valute_rating)

def valute_rating(message: telebot.types.Message):
    quote = message.text.strip().lower()
    base = message.text.strip().lower()
    amount = message.text.strip()
    total_base = CryptoConverter.convert(quote, base, amount)

    text = f'Курс {quote.upper()}'

    for i in keys.keys():
        if i not in quote:
            text = '\n- '.join((text, i + i[total_base]))

    bot.send_message(message.chat.id, text)



bot.polling(non_stop = True)






