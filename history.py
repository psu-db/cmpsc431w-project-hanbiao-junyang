from database import connect_db
from mysql.connector import Error

def view_history(user_id):
    """ view user's history details."""
    connection = connect_db()
    if not connection:
        return

    try:
        print("\n--- Your History ---")
        cursor = connection.cursor(dictionary=True)

        # Query to fetch a simplified history list
        query = """
            SELECT 
                h.history_id,
                h.action_type,
                p.product_name,
                u.username AS seller,
                c.category_name AS category
            FROM History h
            JOIN Product p ON h.product_id = p.product_id
            JOIN User u ON p.user_id = u.user_id
            JOIN Category c ON p.category_id = c.category_id
            WHERE h.user_id = %s
            ORDER BY h.action_date DESC;
        """
        cursor.execute(query, (user_id,))
        history = cursor.fetchall()

        if history:
            print("\nYour Actions:")
            for record in history:
                print(f"ID: {record['history_id']}, Action: {record['action_type']}, Item: {record['product_name']}, Category: {record['category']}, Seller: {record['seller']}")

            # Allow the user to select a specific history item for detailed view
            history_id = int(input("\nEnter the history ID to view details (or press 0 to go back): "))
            if history_id != 0:
                query = """
                    SELECT 
                        p.product_name,
                        p.description,
                        p.price,
                        p.condition,
                        p.image_url,
                        u.username AS seller,
                        c.category_name AS category,
                        h.action_date,
                        h.action_type
                    FROM History h
                    JOIN Product p ON h.product_id = p.product_id
                    JOIN User u ON p.user_id = u.user_id
                    JOIN Category c ON p.category_id = c.category_id
                    WHERE h.history_id = %s;
                """
                cursor.execute(query, (history_id,))
                details = cursor.fetchone()

                if details:
                    print("\n--- Action Details ---")
                    print(f"Name: {details['product_name']}")
                    print(f"Description: {details['description']}")
                    print(f"Price: ${details['price']}")
                    print(f"Condition: {details['condition']}")
                    print(f"Category: {details['category']}")
                    print(f"Seller: {details['seller']}")
                    print(f"Action: {details['action_type']}")
                    print(f"Date: {details['action_date']}")
                    if details['image_url']:
                        print(f"Image URL: {details['image_url']}")
                else:
                    print("History record not found.")
        else:
            print("No history found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()