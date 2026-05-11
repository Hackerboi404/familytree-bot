import sqlite3
import os

from config import Config


# Create connection
def get_db_connection():

    # Create database folder if missing
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect(Config.DATABASE_PATH)

    # Access columns like dictionary
    conn.row_factory = sqlite3.Row

    return conn


# Initialize database
def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS family_tree (

            user_id INTEGER,
            relation_type TEXT,
            target_id INTEGER,
            first_name TEXT,
            username TEXT,

            PRIMARY KEY (user_id, relation_type)
        )
    """)

    conn.commit()
    conn.close()


# Add or replace relation
def add_relation(
    user_id,
    relation_type,
    target_id,
    first_name,
    username
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO family_tree
        (
            user_id,
            relation_type,
            target_id,
            first_name,
            username
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        relation_type,
        target_id,
        first_name,
        username
    ))

    conn.commit()
    conn.close()


# Get full family tree
def get_family_tree(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            relation_type,
            target_id,
            first_name,
            username
        FROM family_tree
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    # Convert into dictionary
    family_data = {}

    for row in rows:

        family_data[row["relation_type"]] = {
            "target_id": row["target_id"],
            "first_name": row["first_name"],
            "username": row["username"]
        }

    return family_data


# Delete specific relation
def delete_relation(user_id, relation_type):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM family_tree
        WHERE user_id = ?
        AND relation_type = ?
    """, (
        user_id,
        relation_type
    ))

    conn.commit()
    conn.close()


# Clear full family tree
def clear_family_tree(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM family_tree
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
