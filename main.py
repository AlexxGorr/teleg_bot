import telebot
from telebot import types
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


def key_markup(quote = True):
    but_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    buttons = []
    for val in keys.keys():
        if val != quote:
            buttons.append(types.KeyboardButton(val))

    but_markup.add(*buttons)
    return but_markup


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты: /convert\nСписок доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in keys.keys():
        text = '\n- '.join((text, i))
    bot.send_message(message.chat.id, text)

    text = 'Операция конверсии: /convert'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['convert'])
def values(message: telebot.types.Message):
    text = 'Выбери валюту из которой конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup = key_markup())
    bot.register_next_step_handler(message, quote_handler)

def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().lower()
    text = 'Выбери валюту в которую конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup = key_markup(quote))
    bot.register_next_step_handler(message, base_handler, quote)

def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip()
    text = 'Количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации\n{e} \nПовторить: /convert')
    else:
        text = f'Результат конвертации\nКол-во единиц: {amount} \n{quote.upper()} в {base.upper()} \n{total_base}'
        bot.send_message(message.chat.id, text)

        text = 'Доступные валюты: /convert\nСписок доступных валют: /values'
        bot.send_message(message.chat.id, text)



bot.polling(non_stop = True)





