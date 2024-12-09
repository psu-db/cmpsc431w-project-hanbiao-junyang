import mysql.connector
from mysql.connector import Error
from database import connect_db


create_tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone_number VARCHAR(15),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        user_rating INT CHECK (user_rating BETWEEN 1 AND 5)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Category (
        category_id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Product (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        category_id INT,
        product_name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        `condition` ENUM('new', 'like new', 'used') NOT NULL,
        image_url VARCHAR(255),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Address (
        address_id INT AUTO_INCREMENT PRIMARY KEY,
        street VARCHAR(150),
        city VARCHAR(30),
        postal_code CHAR(5)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Comment (
        comment_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        comment_text TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS `Order` (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL,
        payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('credit card', 'PayPal')),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        address_id INT,
        payment_status ENUM('PAID', 'UNPAID') NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (address_id) REFERENCES Address(address_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS WishList (
        wish_list_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS History (
        history_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        action_type ENUM('viewed', 'added_to_cart', 'purchased') NOT NULL,
        action_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
    );
    """
]

# Connect to the database 
try:
    connection = mysql.connector.connect(
        host='localhost',  
        user='project_user', 
        password='1234', 
        database='431project'  
    )

    if connection.is_connected():
        print("Connected to the database")

        cursor = connection.cursor()
        for sql in create_tables_sql:
            cursor.execute(sql)
            print("Table processed successfully.")
        
        connection.commit()

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")

def add_quantity_column():
    """Add quantity column to the History table."""
    connection = connect_db()
    try:
        cursor = connection.cursor()
        query = "ALTER TABLE History ADD COLUMN quantity INT DEFAULT 1;"
        cursor.execute(query)
        connection.commit()
        print("Quantity column added successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

add_quantity_column()
