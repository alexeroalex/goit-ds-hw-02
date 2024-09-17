import sqlite3

def create_db():
# Прочитати скрипт для створення таблиць
    with open('task_management.sql', 'r') as f:
        sql = f.read()

# Створити з'єднання з БД
    with sqlite3.connect('task_management.db') as con:
        cur = con.cursor()
        cur.executescript(sql)

if __name__ == "__main__":
    create_db()
