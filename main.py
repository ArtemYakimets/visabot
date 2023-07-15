import telebot
import sqlite3

from telebot import types

TOKEN = '6335375630:AAHgQHYKe1aSnTWYrVUV8o5_SNiJ-2Gr1QE'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Авторизация")
    item2 = types.KeyboardButton("Мои данные")
    item3 = types.KeyboardButton("О боте")
    menu_text = "Меню:\n\n"\
            "*Авторизация*\n"\
            "*Мои данные*\n"\
            "*О боте*"
    menu_keyboard.add(item1, item2, item3)
    bot.send_message(message.chat.id, menu_text, parse_mode="Markdown", reply_markup=menu_keyboard)


# Handler for menu options
@bot.message_handler(content_types=['text'])
def menu_option(message):
    option = message.text

    # Handle option 1
    if option == "Авторизация":
        msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
        bot.register_next_step_handler(msg, authorization)

    # Handle option 2
    elif option == "О боте":
        bot.reply_to(message, "Здесь пока ничего нет")

    elif option == "Мои данные":
        bot.reply_to(message, "Здесь будут хранится ваши данные")

    else:
        bot.reply_to(message, "Я вас не понимаю...")


def authorization(message):
    name = message.text.split(' ')
    first_name = name[0]
    last_name = name[1] if len(name) > 1 else ""

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        fisrt_name TEXT,
        last_name TEXT
        )""")

    connect.commit()

    current_user_id = message.chat.id
    cursor.execute(f"SELECT id FROM users WHERE id = {current_user_id}")
    data = cursor.fetchone()
    if data is None:
        user = (message.chat.id, first_name, last_name)
        cursor.execute("INSERT INTO users VALUES(?, ?, ?);", user)
        connect.commit()
        bot.send_message(message.chat.id, "Успешно!")
    else:
        bot.send_message(message.chat.id, "Вы уже авторизованы")

bot.polling()
