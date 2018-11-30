import psycopg2


conn = psycopg2.connect("dbname=django_db user=anton password=3ie8 host=127.0.0.1")
cur = conn.cursor()

cur.execute("""
  CREATE TABLE IF NOT EXISTS task ( 
    id SERIAL PRIMARY KEY,
    status CHAR(32) NOT NULL,
    description CHAR(256) NOT NULL,
    solution CHAR(64) NOT NULL);
""")

conn.commit()

cur.close()
conn.close()
