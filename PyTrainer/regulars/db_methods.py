import psycopg2


def get_tasks():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM task')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


def get_articles():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM article')
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return articles


def get_attempts():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM attempt')
    attempts = cur.fetchall()
    cur.close()
    conn.close()
    return attempts


def add_attempt(task_id, task_name, solution, passed_tests):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attempt (task_id, task_name, solution, passed_tests, date) VALUES(%s, %s, %s, %s, now())",
        (task_id, task_name, solution, passed_tests)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_article_logs():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM article_log')
    article_logs = cur.fetchall()
    cur.close()
    conn.close()
    return article_logs


def get_task_logs():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM task_log')
    task_logs = cur.fetchall()
    cur.close()
    conn.close()
    return task_logs


def get_users():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM db_user')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


def add_user(user_name, user_password, role='user'):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO db_user (name, password, role, is_active) VALUES(%s, %s, %s, %s)",
        (user_name, user_password, role, False)
    )
    conn.commit()
    cur.close()
    conn.close()


def find_active():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM db_user')
    users = cur.fetchall()
    for user in users:
        if user[4]:
            return user[1]
    cur.close()
    conn.close()


def set_user_activity(user_name, value):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('UPDATE db_user SET is_active = %s WHERE name = %s;', (value, user_name))
    conn.commit()
    cur.close()
    conn.close()
