# init.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, active INT, username TEXT, fname TEXT, lname TEXT, password TEXT, email TEXT, role TEXT)')
    print("Table created successfully")
    conn.close()

def connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return conn

