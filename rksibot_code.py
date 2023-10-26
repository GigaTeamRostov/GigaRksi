import telebot
import sqlite3
from telebot import types
import atexit
import re

bot = telebot.TeleBot('6097744579:AAE00iDqR7gJAosCunrKZ9HEOLZF9X6rMTE')

# Подключение к базе данных
connLogPas = sqlite3.connect('dbLogPas.db')
cursorLogPas = connLogPas.cursor()
admin_id = []
for item in list(map(str, list(cursorLogPas.execute('SELECT chat_id FROM admins')))):
    admin_id.append(str(re.findall(r'\d+', item)[0]))
    

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Логин')
    btn2 = types.KeyboardButton('Расписания')
    btn3 = types.KeyboardButton('Домашние Задания')
    btn4 = types.KeyboardButton('Учебные материалы')
    btn5 = types.KeyboardButton('Выбор группы')
    btn6 = types.KeyboardButton('Админ панель')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    if message.chat.id in admin_id:
        markup.row(btn5, btn6)
    else:
        markup.row(btn5)
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}!', reply_markup=markup)


#Программное
@bot.message_handler(commands=['main'])
def main(message):
    if message.chat.id in admin_id:
        bot.send_message(message.chat.id, message)

#Программное
@bot.message_handler(commands=['id'])
def info_message(message):
    if message.chat.id in admin_id:
        bot.send_message(message.chat.id, message.chat.id)



@bot.message_handler(func=lambda message: True)
def check_login_pass(message):
    if message.text == 'Логин':
        # Ожидаем логин
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Я случайно нажал на логин')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Введите ваш логин и пароль через пробел:', reply_markup = markup)
        bot.register_next_step_handler(message, log_pas)
    elif message.text == 'Выбор группы':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('ИС-11')
        btn2 = types.KeyboardButton('ИС-12')
        btn3 = types.KeyboardButton('ИС-13')
        btn4 = types.KeyboardButton('ИС-14')
        btn5 = types.KeyboardButton('ИС-15')
        btn6 = types.KeyboardButton('ИС-16')
        btn7 = types.KeyboardButton('На главное меню')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7)
        bot.send_message(message.chat.id, f'Выбери свою группу', reply_markup=markup)
    elif message.text == 'На главное меню':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Логин')
        btn2 = types.KeyboardButton('Расписания')
        btn3 = types.KeyboardButton('Домашние Задания')
        btn4 = types.KeyboardButton('Учебные материалы')
        btn5 = types.KeyboardButton('Выбор группы')
        btn6 = types.KeyboardButton('Админ панель')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        if message.chat.id in admin_id:
            markup.row(btn5, btn6)
        else:
            markup.row(btn5)
        bot.send_message(message.chat.id, f'Вы вернулись в главное меню', reply_markup=markup)

def log_pas(message):
    if message.text == 'Я случайно нажал на логин':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('На главное меню')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Вернитесь в главное меню', reply_markup=markup)
        return
    else:
        loginUser = message.text.split()[0]
        passwordUser = message.text.split()[1]
        tf=False
        index = 0

        # Logins
        logins = []
        loginsInDB = list(map(str, list(cursorLogPas.execute('SELECT login FROM teachers'))))
        for item in loginsInDB:
            logins.append(str(re.findall(r'(?i)([a-z]+_+\d+)', item)[list(map(str, list(cursorLogPas.execute('SELECT login FROM teachers')))).index(item)]))
        
        for item in logins:
            it=str(re.findall(r'\d+', item)[0])
            tf=it==loginUser.replace(' ', '')
            index = logins.index(it)
            if tf: break
        passwordInDB = str(re.findall(r'(?i)([a-z]+\d+)', list(map(str, list(cursorLogPas.execute('SELECT password FROM teachers'))))[index])[index])
        if tf:
            if passwordInDB == passwordUser:
                cursorLogPas.execute(f'UPDATE teachers SET chat_id = {message.chat.id}')
                connLogPas.commit()
        else:
            bot.send_message(message.chat.id, 'Такого логина или пароля не существует. Попробуйте еще раз.')

@atexit.register
def goodbye():
    # отправляем сообщение о том, что бот выключен в чат с указанным идентификатором
    for item in admin_id:
        bot.send_message(item, "Bot offline")

bot.polling(none_stop=True)


cursorLogPas.close()
connLogPas.close()

# Сработай во имя святой машины, АМИНЬ!