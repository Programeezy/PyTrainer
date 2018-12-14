import psycopg2


conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS db_user (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          password TEXT NOT NULL,
          role TEXT NOT NULL,
          is_active BOOL NOT NULL,
          invitation_key TEXT);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS task ( 
          id SERIAL PRIMARY KEY,
          status TEXT NOT NULL,
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          solution TEXT NOT NULL,
          creator INTEGER REFERENCES db_user(id));""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          content TEXT ARRAY NOT NULL,
          creator INTEGER REFERENCES db_user(id));""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS task_log (
          task_id INTEGER REFERENCES task(id),
          user_id INTEGER REFERENCES db_user(id),
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          solution TEXT NOT NULL,
          operation TEXT NOT NULL,
          date TIMESTAMP NOT NULL,
          PRIMARY KEY (user_id, task_id));""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article_log (
          article_id INTEGER REFERENCES article(id),
          user_id INTEGER REFERENCES db_user(id),
          name TEXT NOT NULL,
          content TEXT NOT NULL,
          operation TEXT NOT NULL,
          date TIMESTAMP NOT NULL,
          PRIMARY KEY (user_id, article_id));""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS attempt (
          id SERIAL PRIMARY KEY,
          user_id INTEGER REFERENCES db_user(id),
          task_id INTEGER REFERENCES task(id),
          task_name TEXT NOT NULL,
          solution TEXT NOT NULL,
          passed_tests TEXT NOT NULL,
          date TIMESTAMP NOT NULL);""")

conn.commit()

cur.close()
conn.close()
