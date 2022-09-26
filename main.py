import telebot
from telebot import types
from config import keys, TOKEN, chat, option, welcome_ru, welcome_eng
from utils import ConvertionException, CryptoConverter
import random


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
    text = '@PundaBear_bot поможет сконвертировать несколько популярных валют  \
           \n\nСконвертировать валюту: /convert\nПосмотреть список доступных валют: /values \
           \n\nЕсли есть вопросы, задавай, попытаюсь помочь'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in keys.keys():
        text = '\n- '.join((text, i))
    bot.send_message(message.chat.id, text)

    text = 'Сконвертировать валюту: /convert'
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


@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if 'ривет' in message.text or 'дравств' in message.text:
        bot.send_message(message.from_user.id, f'{random.choice(welcome_ru)} \nЕсли хочешь посмотреть список доступных валют - /values')
    elif 'ello' in message.text or 'hi' in message.text or 'Hi' in message.text:
        bot.send_message(message.from_user.id, f'{random.choice(welcome_eng)} \nЕсли хочешь сконвертировать валюту - /convert')
    elif 'смотр' in message.text or 'вид' in message.text or 'валю' in message.text:
        bot.send_message(message.from_user.id, f'Похоже что ты хочешь посмотреть список доступных валют - /values')
    elif 'конверт' in message.text or 'счет' in message.text or 'мен' in message.text \
            or 'сколь' in message.text or 'коли' in message.text:
        bot.send_message(message.from_user.id, f'Похоже что ты хочешь сконвертировать валюту - /convert')
    else:
        bot.send_message(message.from_user.id, f'{random.choice(chat)} \n{random.choice(option)}')


def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
    else:
        text = f'Результат конвертации\nКол-во единиц: {amount} \n{quote.upper()} в {base.upper()} \n{total_base}'
        bot.send_message(message.chat.id, text)

        text = 'Сконвертировать валюту: /convert\nПосмотреть список доступных валют: /values'
        bot.send_message(message.chat.id, text)



bot.polling(non_stop = True)










