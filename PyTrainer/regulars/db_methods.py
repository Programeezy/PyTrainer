from bs4 import BeautifulSoup
import psycopg2
import requests
import pytz
from datetime import datetime, timedelta


def get_tasks(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM task WHERE creator = %s', (get_active_user_id(cookies_dict), ))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks


def get_articles(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM article WHERE creator = %s', (get_active_user_id(cookies_dict), ))
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return articles


def get_attempts(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM attempt WHERE user_id = %s', (get_active_user_id(cookies_dict), ))
    attempts = cur.fetchall()
    cur.close()
    conn.close()
    return attempts


def add_attempt(cookies_dict, task_id, task_name, solution, passed_tests):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO attempt (user_id, task_id, task_name, solution, passed_tests, date)
        VALUES(%s, %s, %s, %s, %s, now())""",
        (get_active_user_id(cookies_dict), task_id, task_name, solution, passed_tests)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_article_logs(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM article_log WHERE user_id = %s', (get_active_user_id(cookies_dict), ))
    article_logs = cur.fetchall()
    cur.close()
    conn.close()
    return article_logs


def get_task_logs(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM task_log WHERE user_id = %s', (get_active_user_id(cookies_dict), ))
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
        "INSERT INTO db_user (name, password, role) VALUES(%s, %s, %s)", (user_name, user_password, role)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_active_user_id(cookies_dict):
    update_sessions()
    sessions = get_sessions()
    for session in sessions:
        if str(session[0]).lower() in cookies_dict:
            return session[2]
    return None


def update_task_status(cookies_dict, task_id, value='solved'):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('UPDATE task SET status = %s WHERE ((id = %s) AND (creator = %s));',
                (value, task_id, get_active_user_id(cookies_dict)))
    conn.commit()
    cur.close()
    conn.close()


def find_active(cookies_dict):
    active_user_id = get_active_user_id(cookies_dict)
    if active_user_id:
        users = get_users()
        for user in users:
            if user[0] == active_user_id:
                return user[1]
    return None


def fill_tasks(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    active_user_id = get_active_user_id(cookies_dict)

    cur.execute(
        "INSERT INTO task (status, name, description, solution, creator) VALUES(%s, %s, %s, %s, %s)",
        ('unsolved', 'A string of vowels',
         'Return a string containing all the words from the article starting with a vowel separated by a space',
         r"' '.join(re.findall(r'\b[aeiouAEIOU]\w+', article))", active_user_id))

    cur.execute(
        "INSERT INTO task (status, name, description, solution, creator) VALUES(%s, %s, %s, %s, %s)",
        ('unsolved', 'Simplified string',
         "Return a string where in place of the following characters: ',', ':', '^' and '?' there will be spaces.",
         r"' '.join(re.split(r'[;,\s]', article))", active_user_id))

    cur.execute(
        "INSERT INTO task (status, name, description, solution, creator) VALUES(%s, %s, %s, %s, %s)",
        ('unsolved', 'Letter number letter',
         "Return the number of digits in the string, surrounded by not number on both sides.",
         r"len(re.findall(r'(?<!\d)\d(?!\d)', article))", active_user_id))

    cur.execute('SELECT * FROM task')
    tasks = cur.fetchall()
    cur.execute('SELECT * FROM task_log WHERE user_id = %s', (get_active_user_id(cookies_dict), ))
    task_log_ids = [lst[0] for lst in cur.fetchall()]
    for task in tasks:
        if task[0] not in task_log_ids:
            cur.execute(
                """INSERT INTO task_log (task_id, user_id, name, description, solution, operation, date)
                VALUES(%s, %s, %s, %s, %s, %s, now())""",
                (task[0], active_user_id, task[2], task[3], task[4], 'creation')
            )

    conn.commit()

    cur.close()
    conn.close()


def fill_articles(cookies_dict):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()

    cur.execute('SELECT name FROM article WHERE creator = %s', (get_active_user_id(cookies_dict), ))
    articles_names = [lst[0] for lst in cur.fetchall()]

    page = requests.get('https://qz.com/quartzy/latest/')
    soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')

    web_links = soup.find_all('article')
    page_links = []
    for link in web_links[5:]:
        url = link.contents[0].find_all('a')[0]
        page_links.append('http://qz.com' + url.get('href'))

    active_user_id = get_active_user_id(cookies_dict)
    the_articles = []
    for link in page_links:
        paragraph_text = []
        url = link
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        the_title = soup.find(class_="_21349 _9a905 none _4ca8e").text
        article_body = soup.find(class_='_61c55 _6923f')
        article_text = soup.find_all('p')[8:]
        for paragraph in article_text[:-1]:
            text = paragraph.text
            paragraph_text.append(text)
        paragraph_text = [s.replace('\xa0', ' ') for s in paragraph_text]

        if the_title not in articles_names:
            cur.execute(
                "INSERT INTO article (name, content, creator) VALUES(%s, %s, %s)",
                (the_title, paragraph_text, active_user_id)
            )

    conn.commit()
    cur.execute('SELECT * FROM article')
    articles = cur.fetchall()
    cur.execute('SELECT * FROM article_log WHERE user_id = %s', (get_active_user_id(cookies_dict), ))
    article_log_ids = [lst[0] for lst in cur.fetchall()]
    for article in articles:
        if article[0] not in article_log_ids:
            cur.execute(
                """INSERT INTO article_log (article_id, user_id, name, content, operation, date)
                VALUES(%s, %s, %s, %s, %s, now())""",
                (article[0], active_user_id, article[1], article[2], 'creation')
            )

    conn.commit()


def attempt_admin():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM db_user WHERE role = %s', ('admin', ))
    admin_users = cur.fetchall()
    if not admin_users:
        cur.execute(
            "INSERT INTO db_user (name, password, role, invitation_key) VALUES(%s, %s, %s, %s)",
            ('admin', 'admin', 'admin', '2kf94ye4o8')
        )
    conn.commit()
    cur.close()
    conn.close()


def delete_user(user_name):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('DELETE FROM db_user WHERE name = %s', (user_name, ))
    conn.commit()
    cur.close()
    conn.close()


def get_sessions():
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM db_session')
    sessions = cur.fetchall()
    cur.close()
    conn.close()
    return sessions


def add_session(userId):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO db_session (user_id) VALUES(%s)", (userId, ))
    conn.commit()
    cur.close()
    conn.close()


def get_session(userId):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('SELECT * FROM db_session WHERE user_id = %s', (userId, ))
    sessions = cur.fetchall()
    cur.close()
    conn.close()
    return sessions[0][0]


def delete_session(userId):
    conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute('DELETE FROM db_session WHERE user_id = %s', (userId,))
    conn.commit()
    cur.close()
    conn.close()


def update_sessions():
    sessions = get_sessions()
    for session in sessions:
        if session[1] + timedelta(hours=1) < datetime.utcnow().replace(tzinfo=pytz.utc):
            delete_session(session[2])
