import telebot
from telebot import types

from database import Student


with open('auth.txt', 'r') as file:
    bot_token = file.read()
bot = telebot.TeleBot(bot_token)

# Keyboards
main_menu_markup = types.ReplyKeyboardMarkup(row_width=2)
main_menu_button_add = types.KeyboardButton('Добавить')
main_menu_button_change_name = types.KeyboardButton('Изменить ФИО')
main_menu_button_change_date = types.KeyboardButton('Изменить дату')
main_menu_button_show_database = types.KeyboardButton('Список')
main_menu_button_pay = types.KeyboardButton('Оплатить')
main_menu_markup.add(
    main_menu_button_add,
    main_menu_button_change_name,
    main_menu_button_change_date,
    main_menu_button_show_database,
    main_menu_button_pay
)

back_menu_markup = types.ReplyKeyboardMarkup(row_width=1)
back_menu_button = types.KeyboardButton('Назад в меню')
back_menu_markup.add(
    back_menu_button
)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
@bot.message_handler(commands=['start'])
def authorization(message):
    bot.send_message(message.chat.id, 'Выбери пункт меню:', reply_markup=main_menu_markup)


@bot.message_handler(func=lambda message: message.text == 'Добавить')
def add_student(message):
    student_info_message = bot.send_message(message.chat.id, 'Напиши ФИО, сумму и дату экзамена через запятую.'
                                                   '\n Пример: Иванов Иван Иванович, 100, 22.10.2022',
                                  reply_markup=back_menu_markup)
    bot.register_next_step_handler(student_info_message, get_person)


def get_person(message):
    student_info = message.text.split(',')
    student_fio = student_info[0].split(' ')
    print(student_fio)
    if len(student_fio != 3):
        student_info_message = bot.send_message(message.chat.id, 'ФИО должно состоять из трех слов! Напиши всю информацию заново')
        bot.register_next_step_handler(student_info_message, get_person)

    for i in student_info:
        bot.send_message(message.chat.id, i)




bot.infinity_polling()