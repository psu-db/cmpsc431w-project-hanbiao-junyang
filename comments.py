from database import connect_db
from mysql.connector import Error

def add_comment(user_id, product_id):
    """Add a comment to a product."""
    connection = connect_db()
    try:
        comment_text = input("Enter your comment: ")
        query = "INSERT INTO Comment (user_id, product_id, comment_text) VALUES (%s, %s, %s);"
        cursor = connection.cursor()
        cursor.execute(query, (user_id, product_id, comment_text))
        connection.commit()
        print("Comment added successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def view_comments(product_id):
    """View comments on a product."""
    connection = connect_db()
    try:
        query = "SELECT u.username, c.comment_text FROM Comment c JOIN User u ON c.user_id = u.user_id WHERE c.product_id = %s;"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (product_id,))
        comments = cursor.fetchall()

        if comments:
            for comment in comments:
                print(f"{comment['username']}: {comment['comment_text']}")
        else:
            print("No comments yet.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()
