import telebot
from telebot import types
from config import currency, TOKEN, chat, option, welcome_ru, welcome_eng
from utils import ConvertionException, CryptoConverter, CryptoRating
import random


def key_markup(quote = True):
    but_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True)
    buttons = []
    for val in currency.keys():
        if val != quote:
            buttons.append(types.KeyboardButton(val.capitalize()))

    but_markup.add(*buttons)
    return but_markup


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start'])
def start(message: telebot.types.Message):
    text = '@PandaCryptoConverter_bot поможет сконвертировать несколько популярных валют  \
           \n\nСконвертировать валюту: /convert\nПосмотреть список доступных валют: /values\nУзнать стоимость выбранной валюты: /rate \
           \n\nЕсли есть вопросы, задавай, попытаюсь помочь'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands = ['help'])
def start(message: telebot.types.Message):
    text = '@PandaCryptoConverter_bot поможет сконвертировать несколько популярных валют.  \
           \n\nСконвертировать валюту: /convert\nПосмотреть список доступных валют: /values\nУзнать стоимость выбранной валюты: /rate \
           \n\nДля ввода с клавиатуры валюты используй названия из списка доступных валют: /values \
           \n\nЕсли есть вопросы, задавай, попытаюсь помочь'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands = ['values'])
def values_list(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i, val in currency.items():
        text = '\n- '.join((text, f'{i.capitalize()} - ({val})'))
    bot.send_message(message.chat.id, text)

    text = 'Сконвертировать валюту: /convert\nУзнать стоимость выбранной валюты: /rate'
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands = ['rate'])
def valute_choice(message: telebot.types.Message):
    text = 'Выбери валюту, чтобы узнать её стоимость: '
    bot.send_message(message.chat.id, text, reply_markup = key_markup())
    bot.register_next_step_handler(message, valute_rating)


def valute_rating(message: telebot.types.Message):
    try:
        quote = message.text.strip().lower()
        total = CryptoRating.rating(quote)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода\n{e}')
    else:
        text = f'Цена за 1: {quote.upper()}'
        for key, val in currency.items():
            if key not in quote:
                if key == 'bitcoin' or key == 'etherium' or key == 'binance coin':
                    text = '\n- '.join((text, f'{key.capitalize()} ------ {total[val]:.8f}'))
                else:
                    text = '\n- '.join((text, f'{key.capitalize()} ------ {round(total[val], 2)}'))
        bot.send_message(message.chat.id, text)

        text = 'Сконвертировать сумму выбранной валюты: /convert'
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
    base = message.text.strip().lower()
    text = 'Количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)


@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if 'приве' in message.text.lower() or 'здрав' in message.text.lower() or 'здоров' in message.text.lower():
        bot.send_message(message.from_user.id, f'{random.choice(welcome_ru)} \nЕсли хочешь посмотреть список доступных валют - /values')
    elif 'hello' in message.text.lower() or 'hi' in message.text.lower():
        bot.send_message(message.from_user.id, f'{random.choice(welcome_eng)} \nЕсли хочешь сконвертировать валюту - /convert')
    elif 'смотр' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь посмотреть список доступных валют - /values')
    elif 'конверт' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь сконвертировать валюту - /convert')
    elif 'вид' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь увидеть список доступных валют - /values')
    elif 'сколь' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь узнать сколько в списке доступных валют - /values')
    elif 'стои' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь узнать сколько стоит выбранная валюта - /rate')
    elif 'счит' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь посчитать стоимость сконвертированной валюты - /convert')
    elif 'помо' in message.text.lower() or 'help' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что тебе нужна помощь - /help')
    elif 'меня' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь узнать где можно поменять валюту. Хммм...')
    elif 'куда' in message.text.lower() or 'сайт' in message.text.lower() or 'данн' in message.text.lower():
        bot.send_message(message.from_user.id, f'Похоже, что ты хочешь узнать откуда беруться данные - www.cryptocompare.com')
    elif 'ты' in message.text.lower() or 'кто' in message.text.lower():
        bot.send_message(message.from_user.id, f'Я @PandaCryptoConverter_bot. Рад знакомству! {random.choice(option)}')
    else:
        bot.send_message(message.from_user.id, f'{random.choice(chat)} \n{random.choice(option)}')


def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
    else:
        if base == 'bitcoin' or base == 'etherium' or base == 'binance coin':
            text = f'Результат конвертации\nКол-во единиц: {amount} \n{quote.upper()} в {base.upper()} \n{total_base:.8f}'
        else:
            text = f'Результат конвертации\nКол-во единиц: {amount} \n{quote.upper()} в {base.upper()} \n{round(total_base, 2)}'
        bot.send_message(message.chat.id, text)

        text = 'Сконвертировать валюту: /convert\nПосмотреть список доступных валют: /values\nУзнать стоимость выбранной валюты: /rate'
        bot.send_message(message.chat.id, text)




bot.polling(non_stop = True)




