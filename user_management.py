# user_management.py
import sqlite3
import bcrypt
from init import connect as con

def find_user(conn, username, password):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cur.fetchone()
    
    if user:
        hashed_password = user[5] 
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return user
    return None

def register_user(conn, username, fname, lname, password, email, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (active, username, fname, lname, password, email, role) VALUES (1, ?, ?, ?, ?, ?, ?)',
                    (username, fname, lname, hashed_password, email, role))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
        return None

def update_user_info(conn, username, field, new_value):
    cur = conn.cursor()
    try:
        if field == 'password':
            hashed_password = bcrypt.hashpw(new_value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute('UPDATE users SET password=? WHERE username=?', (hashed_password, username))
        else:
            cur.execute(f'UPDATE users SET {field}=? WHERE username=?', (new_value, username))
        
        conn.commit()
        print(f"Updated {field} for user '{username}' to '{new_value}'.")
    except sqlite3.Error as e:
        print(f"Error updating user info: {e}")

def deactivate_user(conn, username, active_status):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE users SET active=? WHERE username=?', (active_status, username))
        conn.commit()
        print(f"Deactivated user with user name '{username}'.")
    except sqlite3.Error as e:
        print(f"Error deactivating user: {e}")

def get_admin_users(conn):
    cur = conn.cursor()
    role = 'admin'
    try:
        cur.execute(f"SELECT username, fname, lname, email FROM users WHERE role='{role}'")
        admin_users = cur.fetchall()
        return admin_users
    except sqlite3.Error as e:
        print(f"Error fetching admin users: {e}")
        return None
    
def get_active_users(conn):
    cur = conn.cursor()
    active = 1
    try:
        cur.execute(f"SELECT username, fname, lname, email FROM users WHERE active={active}")
        active_users = cur.fetchall()
        return active_users
    except sqlite3.Error as e:
        print(f"Error fetching active users: {e}")
        return None


