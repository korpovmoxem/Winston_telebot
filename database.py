import sqlite3
import sqlite3 as sl
from datetime import datetime
from tabulate import tabulate


def connect_database() -> sqlite3.Connection:
    connect = sl.connect('DataBase.db')
    data = connect.execute("select count(*) from sqlite_master where type='table' and name='students'")
    for row in data:
        if row[0] == 0:
            with connect:
                connect.execute("""
                CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                last_name VARCHAR(50),
                first_name VARCHAR(50),
                second_name VARCHAR(50),
                value INTEGER,
                paid INTEGER,
                exam_date VARCHAR(10)
                );
                """)
    return connect


def change_fio(old_fio, new_fio):
    connect = connect_database()
    with connect:
        sql = 'SELECT * FROM students WHERE last_name=? and first_name=? and second_name=?'
        data = (
            old_fio[0].capitalize(),
            old_fio[1].capitalize(),
            old_fio[2].capitalize()
        )
        find_person = connect.execute(sql, data).fetchall()
        if not find_person:
            return f"Ошибка: {' '.join(map(lambda x: x.capitalize(), old_fio))} не найден!"
        sql = 'UPDATE students SET last_name=?, first_name=?, second_name=? WHERE last_name=? and first_name=? and second_name=?'
        data = (
            new_fio[0].capitalize(),
            new_fio[1].capitalize(),
            new_fio[2].capitalize(),
            old_fio[0].capitalize(),
            old_fio[1].capitalize(),
            old_fio[2].capitalize(),
        )
        connect.execute(sql, data)
        return f'Успех: {" ".join(map(lambda x: x.capitalize(), old_fio))} изменен на {" ".join(map(lambda x: x.capitalize(), new_fio))}'


def delete_student(fio):
    connect = connect_database()
    with connect:
        sql = 'DELETE FROM students WHERE last_name=? and first_name=? and second_name=?'
        data = (
            fio[0],
            fio[1],
            fio[2],
        )
        connect.execute(sql, data)
        return f'Успех: {" ".join(fio)} удален'


def student_payment(fio):
    connect = connect_database()
    with connect:
        sql = 'UPDATE students SET paid=1 WHERE last_name=? and first_name=? and second_name=?'
        data = (
            fio[0],
            fio[1],
            fio[2],
        )
        connect.execute(sql, data)
        return f'Успех: {" ".join(fio)} оплачен'

def change_data(fio, date):
    connect = connect_database()
    with connect:
        sql = 'SELECT * FROM students WHERE last_name=? and first_name=? and second_name=?'
        data = (
            fio[0].capitalize(),
            fio[1].capitalize(),
            fio[2].capitalize()
        )
        find_person = connect.execute(sql, data).fetchall()
        if not find_person:
            return f"Ошибка: {' '.join(map(lambda x: x.capitalize(), fio))} не найден!"
        sql = 'UPDATE students SET exam_date=? WHERE last_name=? and first_name=? and second_name=?'
        data = (
            date,
            fio[0].capitalize(),
            fio[1].capitalize(),
            fio[2].capitalize(),
        )
        connect.execute(sql, data)
    return f"Успех: Дата {' '.join(map(lambda x: x.capitalize(), fio))} изменена на {date}"


def change_value(fio, value):
    connect = connect_database()
    with connect:
        sql = 'SELECT * FROM students WHERE last_name=? and first_name=? and second_name=?'
        data = (
            fio[0].capitalize(),
            fio[1].capitalize(),
            fio[2].capitalize()
        )
        find_person = connect.execute(sql, data).fetchall()
        if not find_person:
            return f"Ошибка: {' '.join(map(lambda x: x.capitalize(), fio))} не найден!"
        sql = 'UPDATE students SET value=? WHERE last_name=? and first_name=? and second_name=?'
        data = (
            int(value),
            fio[0].capitalize(),
            fio[1].capitalize(),
            fio[2].capitalize(),
        )
        connect.execute(sql, data)
    return f"Успех: Сумма {' '.join(map(lambda x: x.capitalize(), fio))} изменена на {value}"


class Student:

    def __init__(self, last_name: str, first_name: str, second_name: str, value: int, exam_date: datetime):
        self.last_name = last_name.capitalize().strip(' ')
        self.first_name = first_name.capitalize().strip(' ')
        self.second_name = second_name.capitalize().strip(' ')
        self.value = value
        self.exam_date = datetime.strftime(exam_date, '%d.%m.%Y')

    def is_student_in_database(self) -> list:
        connect = connect_database()
        sql = 'SELECT * FROM students WHERE last_name=? and first_name=? and  second_name=?'
        data = (
             self.last_name,
             self.first_name,
             self.second_name
             )
        with connect:
            return connect.execute(sql, data).fetchall()

    def add_to_database(self) -> str:
        connect = connect_database()
        if self.is_student_in_database():
            return 'Ошибка: Данные уже записаны в БД'
        sql = 'INSERT INTO students (last_name, first_name, second_name, value, paid, exam_date) values (?, ?, ?, ?, ?, ?)'
        data = (
             self.last_name,
             self.first_name,
             self.second_name,
             self.value,
             0,
             self.exam_date)
        with connect:
            connect.execute(sql, data)
        return 'Успех: Данные записаны в БД'


def get_database(key='По порядку добавления', type_list=None):
    sorting_keys = {
        'По фамилии': 0,
        'По дате': 5,
        'По сумме': 3,
        'По оплате': 4,
        'По порядку добавления': 1,
    }
    connect = connect_database()
    sql = 'SELECT * FROM students'
    database_entries = connect.execute(sql).fetchall()
    database_list = []
    for entry in sorted(database_entries, key=lambda x: x[sorting_keys[key]]):
        entry = list(entry)
        entry[5] = 'Оплачен' if entry[5] == 1 else 'Не оплачен'
        data_for_table = [
            f"{entry[1]} {entry[2]} {entry[3]}",
            entry[4],
            entry[5],
            entry[6]
        ]
        database_list.append(data_for_table)
    database_table = tabulate(database_list, headers=['ФИО', 'Сумма', 'Оплачен', 'Дата'])
    if type_list == 'table':
        return database_table
    elif type_list == 'inline' or not key:
        return database_list


