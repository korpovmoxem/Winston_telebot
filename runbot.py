from datetime import datetime

import telebot
from telebot import types

from database import Student
from database import get_database
from database import student_payment
from database import delete_student
from database import change_fio
from database import change_data


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
main_menu_button_payment = types.KeyboardButton('Оплатить')
main_menu_button_delete = types.KeyboardButton('Удалить')
main_menu_markup.add(
    main_menu_button_add,
    main_menu_button_change_name,
    main_menu_button_change_date,
    main_menu_button_payment,
    main_menu_button_show_database,
    main_menu_button_delete
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


@bot.message_handler(func=lambda message: message.text == 'Как изменить ФИО')
def change_date_button(message):
    bot.send_message(message.chat.id, 'Напиши текущее ФИО и новое ФИО через запятую.\n'
                                      'Пример: Иванов Иван Иванович, Василенко Василий Васильевич')


@bot.message_handler(func=lambda message: message.text == 'Как изменить дату')
def change_date_button(message):
    bot.send_message(message.chat.id, 'Напиши ФИО и новую дату через запятую.\n'
                                      'Пример: Иванов Иван Иванович, 10.12.2022')


def add_student(user_message,chat_id):
    fio = user_message[0].split(' ')
    value = user_message[1].strip(' ')
    if len(fio) != 3:
        bot.send_message(chat_id, 'В ФИО недостаточно слов')
        return
    if not value.isdigit():
        bot.send_message(chat_id, 'Сумма должна содержать только цифры')
        return
    else:
        value = int(user_message[1])
    try:
        date = datetime.strptime(user_message[2].strip(' '), '%d.%m.%Y')
    except ValueError:
        bot.send_message(chat_id, 'Дата должна быть написана в формате dd.mm.yyyy')
        return
    new_student = Student(fio[0], fio[1], fio[2], value, date)
    database_entry = new_student.add_to_database()
    bot.send_message(chat_id, database_entry)


@bot.message_handler(func=lambda message: message.text == 'Удалить')
def delete_student_button(message):
    database = get_database(type_list='inline')
    student_list_menu = types.InlineKeyboardMarkup(row_width=1)
    for person in database:
        person_string = ' | '.join(map(lambda x: str(x), person))
        person_inline_button = types.InlineKeyboardButton(text=person_string, callback_data=f"delete {person[0]}")
        student_list_menu.add(person_inline_button)
    bot.send_message(message.chat.id, 'Выбери кого удалить', reply_markup=student_list_menu)


@bot.message_handler(func=lambda message: message.text == 'Оплатить')
def student_payment_button(message):
    database = list(filter(lambda x: x[2] != 'Оплачен', get_database(type_list='inline')))
    student_list_menu = types.InlineKeyboardMarkup(row_width=1)
    for person in database:
        del person[2]
        person_string = ' | '.join(map(lambda x: str(x), person))
        person_inline_button = types.InlineKeyboardButton(text=person_string, callback_data=f"payment {person[0]}")
        student_list_menu.add(person_inline_button)
    bot.send_message(message.chat.id, 'Выбери кого оплатить', reply_markup=student_list_menu)


@bot.callback_query_handler(func=lambda callback: 'payment' in callback.data)
def callback_student_payment(callback):
    student_fio = callback.data.split(' ')[1:]
    payment_process = student_payment(student_fio)
    bot.send_message(callback.message.chat.id, payment_process)


@bot.callback_query_handler(func=lambda callback: 'delete' in callback.data)
def callback_delete_student(callback):
    student_fio = callback.data.split(' ')[1:]
    delete_process = delete_student(student_fio)
    bot.send_message(callback.message.chat.id, delete_process)


@bot.message_handler(func=lambda message: message.text == 'Список')
def print_database_button(message):
    bot.send_message(message.chat.id, 'Выбери способ фильтрации списка', reply_markup=filter_menu_markup)


@bot.message_handler(func=lambda message: message.text in ['По фамилии', 'По дате', 'По оплате', 'По сумме', 'По порядку добавления'])
def print_database(message):
    bot.send_message(message.chat.id, get_database(message.text, type_list='table'))


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    user_message = message.text.split(',')
    if len(user_message) == 3:
        add_student(user_message, message.chat.id)
    elif len(user_message) == 2:
        if len(user_message[0].split()) == len(user_message[1].split()):
            old_fio = user_message[0].split()
            new_fio = user_message[1].split()
            change_process = change_fio(old_fio, new_fio)
            bot.send_message(message.chat.id, change_process)
        elif user_message[1].replace('.', '').strip(' ').isdigit():
            try:
                date = datetime.strptime(user_message[1].strip(' '), '%d.%m.%Y')
            except ValueError:
                bot.send_message(message.chat.id, 'Дата должна быть написана в формате dd.mm.yyyy')
                return
            change_data_process = change_data(user_message[0].split(' '), datetime.strftime(date, '%d.%m.%Y'))
            bot.send_message(message.chat.id, change_data_process)
    return bot.send_message(message.chat.id, 'Ошибка: не удалось выполнить команду')


bot.infinity_polling()
