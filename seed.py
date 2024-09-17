from datetime import datetime
import faker
from random import randint, choice
import sqlite3

# Константи для генерації даних
NUMBER_USERS = 10
NUMBER_TASKS = 15

# Функція для генерації випадкової інформації
def generate_fake_data(number_users, number_tasks) -> tuple:
    fake_names = []
    fake_emails = []
    fake_titles = []
    fake_descriptions = []

    fake_data = faker.Faker()

# Дадаємо випадкові імена та імейли для користувачів
    for _ in range(number_users):
        fake_names.append(fake_data.name())
        fake_emails.append(fake_data.email())

# Додаємо випадкові назви завдань та їх описи
    for _ in range(number_tasks):
        fake_titles.append(fake_data.bs().title())
        fake_descriptions.append(fake_data.sentence())
    
# Генерація кількох порожніх описів
    for _ in range(3):
        del fake_descriptions[-1]
    for _ in range(3):
        rand_ind = randint(0, len(fake_descriptions))
        fake_descriptions.insert(rand_ind, '')

    return fake_names, fake_emails, fake_titles, fake_descriptions


# Функція для підготовки даних для скрипту створення таблиць
def prepare_data(names, emails, titles, descriptions) -> tuple:
    for_users = []

# Куреючись формою таблиць, організовуємо дані в потрібну форму
    for name, email in zip(names, emails):
        for_users.append((name, email))

# Статуси задані заздалегідь
    for_status = [('new',), ('in progress',), ('completed',)]
    for_tasks = []
    
    for title, description in zip(titles, descriptions):
        for_tasks.append((title, description, randint(1, 3), randint(1, NUMBER_USERS)))

    return for_users, for_status, for_tasks


# Функція для виконання скрипту створення таблиць
def insert_data_to_db(users, status, tasks) -> None:

    with sqlite3.connect('task_management.db') as con:

        cur = con.cursor()

# Вставлення даних у таблицю користувачів
        sql_to_users = """INSERT INTO users(fullname, email)
                               VALUES (?, ?)"""

        cur.executemany(sql_to_users, users)

# Вставлення даних у таблицю статусів
        sql_to_status = """INSERT INTO status(name)
                               VALUES (?)"""

        cur.executemany(sql_to_status, status)

# Вставлення даних у таблицю завдань
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                              VALUES (?, ?, ?, ?)"""

        cur.executemany(sql_to_tasks, tasks)

# Фіксуємо наші зміни в БД
        con.commit()

if __name__ == "__main__":
    users, status, tasks = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS))
    insert_data_to_db(users, status, tasks)

