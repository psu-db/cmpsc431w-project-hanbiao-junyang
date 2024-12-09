import bcrypt
import getpass
from database import connect_db
from mysql.connector import Error

def create_account():
    """Create a new user account."""
    connection = connect_db()
    cursor = connection.cursor()
    
    try:
        print("\nCreate a New Account")
        username = input("Enter the username: ")
        email = input("Enter your email: ")
        password = getpass.getpass("Enter a password: ")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = "INSERT INTO User (username, password_hash, email) VALUES (%s, %s, %s);"
        cursor.execute(query, (username, hashed_password, email))
        connection.commit()
        print("Account created successfully!")
    except Error as e:
        if e.errno == 1062:  # Duplicate entry
            print("Error: Username or email already exists.")
        else:
            print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

def login():
    """Log in a user and return their user_id."""
    connection = connect_db()
    try:
        print("\n--- Log In ---")
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        cursor = connection.cursor(dictionary=True)
        query = "SELECT user_id, password_hash FROM User WHERE username = %s;"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            print(f"Welcome, {username}! You are now logged in.")
            return user['user_id']# for later query use
        else:
            print("Invalid username or password.")
            return None
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        connection.close()