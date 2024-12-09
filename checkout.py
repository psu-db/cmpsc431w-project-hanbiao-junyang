from database import connect_db
from mysql.connector import Error

def checkout(user_id):
    """Checkout process with the ability to decrease item quantity or remove items."""
    connection = connect_db()
    try:
        print("\n--- Checkout ---")
        cursor = connection.cursor(dictionary=True)

        while True:
            # Fetch items in the cart
            query = """
                SELECT h.product_id, p.product_name, p.price, h.quantity
                FROM History h
                JOIN Product p ON h.product_id = p.product_id
                WHERE h.user_id = %s AND h.action_type = 'added_to_cart';
            """
            cursor.execute(query, (user_id,))
            cart_items = cursor.fetchall()

            if cart_items:
                print("\nYour Cart:")
                total = 0
                for item in cart_items:
                    item_total = item['price'] * item['quantity']
                    total += item_total
                    print(f"ID: {item['product_id']}, Name: {item['product_name']}, "
                          f"Price: ${item['price']:.2f}, Quantity: {item['quantity']}, Total: ${item_total:.2f}")

                print(f"\nTotal: ${total:.2f}")
                print("\nOptions:")
                print("1. Proceed to checkout")
                print("2. Remove or decrease quantity of an item")
                print("3. Go back to dashboard")
                action = input("Choose an option (1/2/3): ").strip()

                if action == '1':
                    # Finalize checkout
                    confirm = input("Proceed to checkout? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        query = """
                            INSERT INTO `Order` (user_id, order_date, total_amount, payment_method, payment_status)
                            VALUES (%s, NOW(), %s, 'credit card', 'PAID');
                        """
                        cursor.execute(query, (user_id, total))
                        connection.commit()
                        print("Order placed successfully!")

                        # Clear the cart after checkout
                        query = "DELETE FROM History WHERE user_id = %s AND action_type = 'added_to_cart';"
                        cursor.execute(query, (user_id,))
                        connection.commit()
                    break
                elif action == '2':
                    # Remove or decrease quantity
                    product_id = int(input("Enter the product ID to modify: ").strip())
                    decrease = input("Decrease quantity by 1 or remove completely? (d/r): ").strip().lower()

                    if decrease == 'd':
                        # Decrease quantity by 1
                        query = """
                            UPDATE History
                            SET quantity = quantity - 1
                            WHERE user_id = %s AND product_id = %s AND action_type = 'added_to_cart' AND quantity > 1;
                        """
                        cursor.execute(query, (user_id, product_id))
                        if cursor.rowcount > 0:
                            print(f"Decreased quantity of Product ID {product_id} by 1.")
                        else:
                            print(f"Product ID {product_id} is already at the minimum quantity.")
                    elif decrease == 'r':
                        # Remove the item completely
                        query = """
                            DELETE FROM History
                            WHERE user_id = %s AND product_id = %s AND action_type = 'added_to_cart';
                        """
                        cursor.execute(query, (user_id, product_id))
                        print(f"Removed Product ID {product_id} from the cart.")
                    connection.commit()
                elif action == '3':
                    break
                else:
                    print("Invalid option. Please try again.")
            else:
                print("Your cart is empty.")
                break
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()





def add_to_cart(user_id, product_id):
    """Add a product to the cart, increasing quantity if it already exists."""
    connection = connect_db()
    try:
        # Check if the product is already in the cart
        query = """
            SELECT quantity FROM History
            WHERE user_id = %s AND product_id = %s AND action_type = 'added_to_cart';
        """
        cursor = connection.cursor()
        cursor.execute(query, (user_id, product_id))
        record = cursor.fetchone()

        if record:
            # If the product exists, increase its quantity
            query = """
                UPDATE History
                SET quantity = quantity + 1
                WHERE user_id = %s AND product_id = %s AND action_type = 'added_to_cart';
            """
            cursor.execute(query, (user_id, product_id))
        else:
            # If the product does not exist, insert a new record
            query = """
                INSERT INTO History (user_id, product_id, action_type, action_date, quantity)
                VALUES (%s, %s, 'added_to_cart', NOW(), 1);
            """
            cursor.execute(query, (user_id, product_id))
        connection.commit()
        print("Item added to cart.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()
