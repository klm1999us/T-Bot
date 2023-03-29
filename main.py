import telebot
from config import TOKEN, currency
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# Справка по работе с ботом-конвертором валют.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите запрос в формате: <имя валюты> <в какую валюту перевести> \
<количество покупаемой валюты>. Например: доллар рубль 100\n     \
Или: USD RUB 100\n Чтобы увидеть список валют, введите - /values'
    bot.reply_to(message, text)


# Отображение списка валют, с которыми бот работает.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for c in currency.keys():
        text = '\n'.join((text, c))
    bot.reply_to(message, text)


# Обработка ввода пользователя, отлов ошибок пользователя.
# Получение ответа от API через метод get_price(), и вывод результата коевертации в бот.
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        user_input = message.text.split()

        if len(user_input) != 3:
            raise APIException('Введите три параметра!\n Для справки наберите /help')

        base, quote, amount = user_input

        if base in currency.values():
            base = list(currency.keys())[list(currency.values()).index(base)]
        if quote in currency.values():
            quote = list(currency.keys())[list(currency.values()).index(quote)]

        final_price = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать параметр {e}!')
    else:
        text = f'{amount} {currency[base]} = {final_price} {currency[quote]}'
        bot.send_message(message.chat.id, text)


bot.polling()
