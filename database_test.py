# db_test
from user_management import find_user, register_user, deactivate_user as deactivate_user_db, update_user_info, get_admin_users, get_active_users
from init import init_db as init_users
from init import connect as con

def main_menu():
    print("\n=== User Authentication System ===")
    print("1. Register a new user")
    print("2. Login")
    print("3. Update user information")
    print("4. Deactivate user")
    print("5. List admin users")
    print("6. List active users")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice

def register_new_user(conn):
    print("\n=== Register New User ===")
    username = input("Enter username: ")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    password = input("Enter password: ") 
    email = input("Enter email: ")
    role = input("Enter role: ")
    
    user_id = register_user(conn, username, fname, lname, password, email, role)
    if user_id:
        print(f"User registered successfully with ID: {user_id}")
    else:
        print("Failed to register user.")

def login_user(conn):
    print("\n=== User Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = find_user(conn, username, password)
    if user:
        print(f"Welcome, {user[2]} {user[3]} ({user[1]})")
    else:
        print("Invalid username or password.")

def update_user(conn):
    print("\n=== Update User Information ===")
    username = input("Enter username of the user to update: ")
    field_map = {
        'first name': 'fname',
        'last name': 'lname',
        'password': 'password',
        'email': 'email',
        'role': 'role'
    }
    
    print("Enter field to update (First Name, Last Name, Password, Email, Role): ")
    field_input = input().strip().lower()
    field = field_map.get(field_input)
    if field is None:
        print("Invalid field. Please enter one of: First Name, Last Name, Password, Email, Role.")
        return
    
    new_value = input(f"Enter new value for {field_input.capitalize()}: ")
    if field == 'password':
        new_password = input("Enter new password: ")
        update_user_info(conn, username, 'password', new_password)
    else:
        update_user_info(conn, username, field, new_value)

def deactivate_user_menu(conn):
    print("\n=== Deactivate User ===")
    username = input("Enter user name of the user to deactivate: ")
    active_status = 0
    deactivate_user_db(conn, username, active_status)

def display_admin_users(conn):
    print("\n=== Admin Users ===")
    admin_users = get_admin_users(conn)
    if admin_users:
        for user in admin_users:
            print(f"Username: {user[0]}, First Name: {user[1]}, Last Name: {user[2]}, Email: {user[3]}")
    else:
        print("No admin users found.")

def display_active_users(conn):
    print("\n=== Active Users ===")
    active_users = get_active_users(conn)
    if active_users:
        for user in active_users:
            print(f"Username: {user[0]}, First Name: {user[1]}, Last Name: {user[2]}, Email: {user[3]}")
    else:
        print("No active users found.")

def user_menu():
    init_users()
    db_file = 'database.db'
    conn = con(db_file)
    if conn:
        while True:
            choice = main_menu()
            
            if choice == '1':
                register_new_user(conn)
            elif choice == '2':
                login_user(conn)
            elif choice == '3':
                update_user(conn)
            elif choice == '4':
                deactivate_user_menu(conn)  
            elif choice == '5':
                display_admin_users(conn)  
            elif choice == '6':
                display_active_users(conn)  
            elif choice == '0':
                print("Exiting program.")
                break
            else:
                print("Invalid choice, please enter another choice.")
        
        conn.close()
    else:
        print(f"Error: Unable to establish connection to {db_file}")

if __name__ == '__main__':
    user_menu()


