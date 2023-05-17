# ссылка на бота - https://t.me/Convert12345Bot

# библиотеки для работы бота
import telebot
from telebot import types
# библиотека для конвертации валюты
from currency_converter import CurrencyConverter


# ключ для управления ботом
bot = telebot.TeleBot('5994619998:AAEpyE8O3g_TMPYXVrbLc1Xku4HSnZitIWo')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start']) # Message handlers - обработчики сообщений
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, введите сумму') # Вывод сообщения при вводе команды start
    bot.register_next_step_handler(message, summ) # Регистрируем следующее действие


def summ(message):
    global amount

    try:
        amount = int(message.text.strip()) # Получаем от пользователя данные и помещаем в переменную amount
    except ValueError: # Ошибка при вводе данных не в виде int
        bot.send_message(message.chat.id, 'Введён неверный формат. Нужно вписать сумму.') # Вывод сообщения
        bot.register_next_step_handler(message, summ) # Регистрируем следующее действие (следующее, что вводит пользователь будет обработано этой же функцией)
        return # Чтобы не выполнялся последующий код

    if amount > 0: # Если введённое пользователем число больше 0
        markup = types.InlineKeyboardMarkup(row_width=2) # Создаём инлайн кнопку и указываем что в одном ряду будет 2 кнопки
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur') # создаём кнопку USD/EUR
        button2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd') # создаём кнопку EUR/USD
        button3 = types.InlineKeyboardButton('Другое значение', callback_data='else') # создаём кнопку "Другое значение"
        markup.add(button1, button2, button3) # Добавляем ранее созданные кнопки в markup
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup) # Вывод сообщения
    else: # Ошибка если пользователь вводит 0 или отрицательное число
        bot.send_message(message.chat.id, 'Число должно быть больше 0') # Вывод сообщения
        bot.register_next_step_handler(message, summ) # Регистрируем следующее действие


@bot.callback_query_handler(func=lambda call: True) # обработка запроса обратного вызова (создание метода, который будет обрабатывать callback_data)
def callback(call):
    if call.data != 'else': # Обработка кнопок USD/EUR и EUR/USD
        value = call.data.upper().split('/') # помещение usd/eur или eur/usd в value
        res = currency.convert(amount, value[0], value[1]) # конвертация полученного значения
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.') # Вывод сообщения и округления res до двуз цифр после запятой
        bot.register_next_step_handler(call.message, summ) # Регистрируем следующее действие (чтобы можно было заново ввести сумму и провести конвертацию)
    else: # Обработка кнопки "Другое значение"
        bot.send_message(call.message.chat.id, 'Введите пару валют через слеш') # Вывод сообщения
        bot.register_next_step_handler(call.message, user_currency) # Регистрируем следующее действие

def user_currency(message): # Обработка данных введёных пользователем
    try:
        value = message.text.upper().split('/') # помещение введённых пользователем пары валют в value
        res = currency.convert(amount, value[0], value[1]) # конвертация полученного значения
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.') # Вывод сообщения
        bot.register_next_step_handler(message, summ) # Регистрируем следующее действие (чтобы можно было заново ввести сумму и провести конвертацию)
    except Exception: # при возникновении любой ошибки - вывод сообщения и регистрация следующего действия
        bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте заново ввести сумму.')
        bot.register_next_step_handler(message, summ)


bot.polling(none_stop=True) # запуск бота