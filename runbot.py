from datetime import datetime

import telebot
from telebot import types

from database import Student
from database import get_database


with open('bot_auth.txt', 'r') as file:
    bot_token = file.read()
bot = telebot.TeleBot(bot_token)

user_auth = []
with open('user_auth.txt', 'r') as file:
    user_auth.append(file.read())

# Клавиатуры
# Главное меню
main_menu_markup = types.ReplyKeyboardMarkup(row_width=2)
main_menu_button_add = types.KeyboardButton('Как добавить')
main_menu_button_change_name = types.KeyboardButton('Как изменить ФИО')
main_menu_button_change_date = types.KeyboardButton('Как изменить дату')
main_menu_button_show_database = types.KeyboardButton('Список')
main_menu_button_payment = types.KeyboardButton('Как изменить "Оплачен"')
main_menu_markup.add(
    main_menu_button_add,
    main_menu_button_change_name,
    main_menu_button_change_date,
    main_menu_button_payment,
    main_menu_button_show_database,
)

# Меню "Назад"
back_menu_markup = types.ReplyKeyboardMarkup(row_width=1)
back_menu_button = types.KeyboardButton('Назад в меню')
back_menu_markup.add(
    back_menu_button
)

# Меню выбора фильтра БД
filter_menu_markup = types.ReplyKeyboardMarkup(row_width=2)
filter_by_last_name_button = types.KeyboardButton('По фамилии')
filter_by_date_button = types.KeyboardButton('По дате')
filter_by_payment_button = types.KeyboardButton('По оплате')
filter_by_value_button = types.KeyboardButton('По сумме')
filter_by_id_button = types.KeyboardButton('По порядку добавления')
filter_menu_markup.add(
    filter_by_last_name_button,
    filter_by_date_button,
    filter_by_payment_button,
    filter_by_value_button,
    filter_by_id_button,
    back_menu_button
)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
@bot.message_handler(commands=['start'])
def authorization(message):
    bot.send_message(message.chat.id, 'Выбери один из пунктов меню:', reply_markup=main_menu_markup)


@bot.message_handler(func=lambda message: message.text == 'Как добавить')
def add_button(message):
    bot.send_message(message.chat.id, 'Напиши ФИО, сумму и дату через запятую.\n'
                                      'Пример: Иванов Иван Иванович, 100, 22.10.2022')


def change_date_button(message):
    pass


def change_payment_button(message):
    pass


@bot.message_handler(func=lambda message: message.text == 'Список')
def print_database_button(message):
    bot.send_message(message.chat.id, 'Выбери способ фильтрации списка', reply_markup=filter_menu_markup)


@bot.message_handler(func=lambda message: message.text in ['По фамилии', 'По дате', 'По оплате', 'По сумме', 'По порядку добавления'])
def print_database(message):
    bot.send_message(message.chat.id, get_database(message.text))


@bot.message_handler(content_types=['text'])
def add_student(message):
    user_message = message.text.split(',')
    if len(user_message) != 3:
        bot.send_message(message.chat.id, 'В сообщении недостаточно данных для записи в БД')
        return
    else:
        fio = user_message[0].split(' ')
        value = user_message[1].strip(' ')
    if len(fio) != 3:
        bot.send_message(message.chat.id, 'В ФИО недостаточно слов')
        return
    if not value.isdigit():
        bot.send_message(message.chat.id, 'Сумма должна содержать только цифры')
        return
    else:
        value = int(user_message[1])
    try:
        date = datetime.strptime(user_message[2].strip(' '), '%d.%m.%Y')
    except ValueError:
        bot.send_message(message.chat.id, 'Дата должна быть написана в формате dd.mm.yyyy')
        return
    new_student = Student(fio[0], fio[1], fio[2], value, date)
    database_entry = new_student.add_to_database()
    bot.send_message(message.chat.id, database_entry)


bot.infinity_polling()
