import sqlite3


def select_tasks_by_user(con: sqlite3.Connection, user_id):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id = ?;", (user_id,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def select_tasks_by_status(con: sqlite3.Connection, status_name):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);", (status_name,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def update_status(con: sqlite3.Connection, task_id, status_name):
    cur = con.cursor()
    try:
        cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?;", (status_name, task_id))
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return 'Task successfully updated.'


def select_users_no_tasks(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def insert_task_for_user(con: sqlite3.Connection, task_title, task_description, status_id, user_id):
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?,?,?,?);", 
                    (task_title, task_description, status_id, user_id))
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return 'Task successfully added.'


def select_incomplete_tasks(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def delete_task(con: sqlite3.Connection, task_id):
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return 'Task successfully deleted.'


def select_user_by_email(con: sqlite3.Connection, filter):
    rows = None
    cur = con.cursor()
    try:
        filtering_text = f'%{filter}%'
        cur.execute("SELECT * FROM users WHERE email LIKE ?;", (filtering_text,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def update_user_name(con: sqlite3.Connection, user_id, new_name):
    cur = con.cursor()
    try:
        cur.execute("UPDATE users SET fullname = ? WHERE id = ?;", (new_name, user_id))
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return "User's name successfully updated."


def count_tasks_by_status(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT s.name, COUNT(*) as task_count FROM tasks AS t JOIN status AS s ON s.id = t.status_id GROUP BY status_id;")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def select_tasks_by_useremail(con: sqlite3.Connection, domain):
    rows = None
    cur = con.cursor()
    try:
        domain_text = f'%@{domain}'
        cur.execute('''SELECT t.id, t.title, t.description, t.status_id, u.email FROM tasks AS t 
                    JOIN users AS u ON t.user_id = u.id WHERE u.email LIKE ?;''', (domain_text,))
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def select_tasks_no_description(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE description = '';")
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def select_users_tasks_in_progress(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute('''SELECT u.id, u.fullname, t.id, t.title, t.description, t.status_id FROM users AS u 
                    INNER JOIN tasks AS t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');''')
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


def select_users_task_count(con: sqlite3.Connection):
    rows = None
    cur = con.cursor()
    try:
        cur.execute('''SELECT u.id, u.fullname, COUNT(*) AS task_count FROM users AS u 
                    LEFT JOIN tasks AS t ON u.id = t.user_id GROUP BY u.id;''')
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()

    return rows


if __name__ == "__main__":
    with sqlite3.connect('task_management.db') as con:
        print('Select user tasks:\n',select_tasks_by_user(con, 10), '\n')
        print('Select tasks by status:\n', select_tasks_by_status(con, 'in progress'), '\n')
        print('Update task status:\n', update_status(con, 10, 'completed'), '\n')
        print('Select users with no tasks:\n',select_users_no_tasks(con), '\n')
        print('Insert new task for a user:\n', insert_task_for_user(con, 'Start The App Development', 'Also some random text...', 1, 4), '\n')
        print('Select incomplete tasks:\n', select_incomplete_tasks(con), '\n')
        print('Delete task:\n', delete_task(con, 12), '\n')
        print('Select user by email:\n', select_user_by_email(con, 'ia'), '\n')
        print("Update user's fullname:\n", update_user_name(con, 3, 'Emma Stones'), '\n')
        print('Count tasks for each status:\n', count_tasks_by_status(con), '\n')
        print('Select tasks by user email:\n', select_tasks_by_useremail(con, 'example.org'), '\n')
        print('Select tasks with no description:\n', select_tasks_no_description(con), '\n')
        print('Select user and their tasks in progress:\n', select_users_tasks_in_progress(con), '\n')
        print('Select user and their task numbers:\n', select_users_task_count(con), '\n')


