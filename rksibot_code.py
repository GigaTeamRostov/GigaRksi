import telebot

bot = telebot.TeleBot('6097744579:AAE00iDqR7gJAosCunrKZ9HEOLZF9X6rMTE')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')



bot.polling(none_stop=True)