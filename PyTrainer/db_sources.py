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
          description TEXT NOT NULL,
          solution TEXT NOT NULL);""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS article (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL,
          content TEXT ARRAY NOT NULL);""")

# ---Insert into Article--------------------------------------------

cur.execute('SELECT * FROM article')
articles = cur.fetchall()

if not articles:
    page = requests.get('https://qz.com/quartzy/latest/')
    soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')

    web_links = soup.find_all('article')
    page_links = []
    for link in web_links[5:]:
        url = link.contents[0].find_all('a')[0]
        page_links.append('http://qz.com'+url.get('href'))

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

        cur.execute(
            "INSERT INTO article (name, content) VALUES(%s, %s)",
            (the_title, paragraph_text))
    conn.commit()

# ---Insert into Task-----------------------------------------------

cur.execute('SELECT * FROM task')
tasks = cur.fetchall()

if not tasks:
    cur.execute(
        "INSERT INTO task (status, description, solution) VALUES(%s, %s, %s)",
        ('unsolved',
         'Return a string containing all the words from the article starting with a vowel separated by a space',
         r"' '.join(re.findall(r'\b[aeiouAEIOU]\w+', article))"))
    conn.commit()

cur.close()
conn.close()
