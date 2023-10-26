import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6097744579:AAE00iDqR7gJAosCunrKZ9HEOLZF9X6rMTE')

# Подключение к базе данных
connLogPas = sqlite3.connect('dbLogPas.db')
cursorLogPas = connLogPas.cursor()


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Логин')
    btn2 = types.KeyboardButton('Расписания')
    btn3 = types.KeyboardButton('Домашние Задания')
    btn4 = types.KeyboardButton('Учебные материалы')
    btn5 = types.KeyboardButton('Выбора группы')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}!', reply_markup=markup)



@bot.message_handler(func=lambda message: True)
def check_login_pass(message):
    if message.text == 'Логин':
        # Ожидаем логин
        bot.send_message(message.chat.id, 'Введите ваш логин:')
        bot.register_next_step_handler(message, check_login)


def check_login(message):
    login = message.text

    # Проверяем наличие логина в базе данных
    cursorLogPas.execute("SELECT * FROM users WHERE login=?", (login,))
    user = cursorLogPas.fetchone()
    if user:
        # Сохраняем логин в контексте для дальнейшей проверки пароля
        bot_data = bot.get_chat(message.chat.id)
        bot_data.login = login

        # Ожидаем пароль
        bot.send_message(message.chat.id, 'Введите ваш пароль:')
        bot.register_next_step_handler(message, check_password)
    else:
        bot.send_message(message.chat.id, 'Неверный логин. Попробуйте еще раз.')


def check_password(message):
    password = message.text

    # Получаем логин из контекста
    bot_data = bot.get_chat(message.chat.id)
    login = bot_data.login

    # Проверяем пароль
    cursorLogPas.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    user = cursorLogPas.fetchone()
    if user:
        bot.send_message(message.chat.id, 'Вход выполнен!')
    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Попробуйте еще раз.')
        bot.register_next_step_handler(message, check_login)


bot.polling(none_stop=True)

cursorLogPas.close()
connLogPas.close()