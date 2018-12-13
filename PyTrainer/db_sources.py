from bs4 import BeautifulSoup
import psycopg2
import pprint
import requests

conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS task ( 
          id SERIAL PRIMARY KEY,
          status TEXT NOT NULL,
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          solution TEXT NOT NULL);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          content TEXT ARRAY NOT NULL);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS task_log (
          id SERIAL PRIMARY KEY,
          task_id INTEGER REFERENCES task(id),
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          solution TEXT NOT NULL,
          date TIMESTAMP NOT NULL);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article_log (
          id SERIAL PRIMARY KEY,
          article_id integer REFERENCES article(id),
          name TEXT NOT NULL,
          content TEXT NOT NULL,
          date TIMESTAMP NOT NULL);""")

# ---Insert into Article--------------------------------------------

cur.execute('SELECT name FROM article')
articles_names = cur.fetchall()

page = requests.get('https://qz.com/quartzy/latest/')
soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')

web_links = soup.find_all('article')
page_links = []
for link in web_links[5:]:
    url = link.contents[0].find_all('a')[0]
    page_links.append('http://qz.com' + url.get('href'))

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
            "INSERT INTO article (name, content) VALUES(%s, %s)",
            (the_title, paragraph_text)
        )
conn.commit()

cur.execute('SELECT * FROM article')
articles = cur.fetchall()
cur.execute('SELECT id FROM article_log')
article_log_ids = cur.fetchall()
for article in articles:
    if article[0] not in article_log_ids:
        cur.execute(
            "INSERT INTO article_log (article_id, name, content, date) VALUES(%s, %s, %s, now())",
            (article[0], article[1], article[2])
        )
conn.commit()

# ---Insert into Task-----------------------------------------------

cur.execute('SELECT * FROM task')
tasks = cur.fetchall()

if not tasks:
    cur.execute(
        "INSERT INTO task (status, name, description, solution) VALUES(%s, %s, %s, %s)",
        ('unsolved', 'A string of vowels',
         'Return a string containing all the words from the article starting with a vowel separated by a space',
         r"' '.join(re.findall(r'\b[aeiouAEIOU]\w+', article))"))
    conn.commit()

    cur.execute('SELECT * FROM task')
    tasks = cur.fetchall()
    cur.execute('SELECT id FROM task_log')
    task_log_ids = cur.fetchall()
    for task in tasks:
        if task[0] not in task_log_ids:
            cur.execute(
                "INSERT INTO task_log (task_id, name, description, solution, date) VALUES(%s, %s, %s, %s, now())",
                (task[0], task[2], task[3], task[4])
            )
    conn.commit()

cur.close()
conn.close()
