import sqlite3
from config import Config
import os

def get_db_connection():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS family_tree (
            user_id INTEGER,
            relation_type TEXT,
            target_id INTEGER,
            first_name TEXT,
            username TEXT,
            PRIMARY KEY (user_id, relation_type)
        )
    ''')
    conn.commit()
    conn.close()

def add_relation(user_id, relation_type, target_id, first_name, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO family_tree (user_id, relation_type, target_id, first_name, username)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, relation_type, target_id, first_name, username))
    conn.commit()
    conn.close()

def get_family_tree(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT relation_type, first_name, username FROM family_tree WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
