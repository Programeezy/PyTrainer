import psycopg2


conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS task ( 
          id SERIAL PRIMARY KEY,
          status TEXT NOT NULL,
          description TEXT NOT NULL,
          solution TEXT NOT NULL);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          content TEXT NOT NULL);""")

# ---Insert into Task-----------------------------------------------

cur.execute(
    "INSERT INTO task (status, description, solution) VALUES(%s, %s, %s)",
    ('unsolved', 'Извлекиет все слова в text, начинающиеся на гласную букву', r"re.findall(r'\w+', text)"))
conn.commit()

cur.close()
conn.close()
