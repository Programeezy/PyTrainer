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
