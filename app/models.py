import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data/analytics.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, content TEXT, timestamp DATETIME)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS analytics
                 (id INTEGER PRIMARY KEY, post_id INTEGER, type TEXT, value TEXT, timestamp DATETIME,
                 FOREIGN KEY (post_id) REFERENCES posts (id))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('data/analytics.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_post(content):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO posts (content, timestamp) VALUES (?, ?)",
              (content, datetime.now().isoformat()))
    conn.commit()
    conn.close()