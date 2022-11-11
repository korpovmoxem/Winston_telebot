import sqlite3 as sl


def connect_database():
    connect = sl.connect('DataBase.db')
    data = connect.execute("select count(*) from sqlite_master where type='table' and name='goods'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для товаров
            with connect:
                connect.execute("""
                CREATE TABLE main_table (
                id INTEGER PRIMARY KEY,
                last_name VARCHAR(50),
                first_name VARCHAR(50),
                second_name VARCHAR(50),
                value INTEGER,
                paid INTEGER,
                exam_date VARCHAR(10)
                );
                """)


class Student:

    def _init__(self, last_name, first_name, second_name, value, exam_date):
        self.last_name = last_name
        self.first_name = first_name
        self.second_name = second_name
        self.value = value
        self.exam_date = exam_date

