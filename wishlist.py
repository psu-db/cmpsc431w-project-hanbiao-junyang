from database import connect_db
from mysql.connector import Error

def add_to_wishlist(user_id, product_id):
    """Add a product to the wishlist."""
    connection = connect_db()
    try:
        # Check if the product is already in the wishlist
        query = "SELECT product_id FROM WishList WHERE user_id = %s AND product_id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (user_id, product_id))
        exists = cursor.fetchone()

        if exists:
            print("This product is already in your wishlist.")
        else:
            query = "INSERT INTO WishList (user_id, product_id) VALUES (%s, %s);"
            cursor.execute(query, (user_id, product_id))
            connection.commit()
            print("Item added to wishlist.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def delete_from_wishlist(user_id, product_id):
    """Delete a product from the wishlist."""
    connection = connect_db()
    try:
        query = "DELETE FROM WishList WHERE user_id = %s AND product_id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (user_id, product_id))
        connection.commit()
        print("Item removed from wishlist.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def view_wishlist(user_id):
    """View items in the user's wishlist and add items to the cart."""
    connection = connect_db()
    try:
        print("\n--- Wishlist ---")
        cursor = connection.cursor(dictionary=True)

        # Fetch unique items in the wishlist
        query = """
            SELECT DISTINCT w.product_id, p.product_name, p.price, p.condition
            FROM WishList w
            JOIN Product p ON w.product_id = p.product_id
            WHERE w.user_id = %s;
        """
        cursor.execute(query, (user_id,))
        wishlist_items = cursor.fetchall()

        if wishlist_items:
            for item in wishlist_items:
                print(f"ID: {item['product_id']}, Name: {item['product_name']}, Price: ${item['price']:.2f}, Condition: {item['condition']}")

            while True:
                product_id = int(input("\nEnter the product ID to add to cart (or 0 to return to dashboard): ").strip())
                if product_id == 0:
                    break

                # Check if the product is still in the wishlist
                query = "SELECT product_id FROM WishList WHERE user_id = %s AND product_id = %s;"
                cursor.execute(query, (user_id, product_id))
                exists = cursor.fetchone()

                if exists:
                    try:
                        query = """
                            INSERT INTO History (user_id, product_id, action_type, action_date)
                            VALUES (%s, %s, 'added_to_cart', NOW());
                        """
                        cursor.execute(query, (user_id, product_id))
                        connection.commit()
                        print(f"Product ID {product_id} has been added to your cart.")
                    except Error as e:
                        print(f"Error adding to cart: {e}")
                else:
                    print("This product is not in your wishlist.")
        else:
            print("Your wishlist is empty.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


