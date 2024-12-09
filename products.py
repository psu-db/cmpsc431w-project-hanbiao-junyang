from database import connect_db
from mysql.connector import Error

def post_item(user_id):
    """Allows a user to post a new product with a category name."""
    connection = connect_db()
    try:
        print("\n--- Post a New Item ---")
        product_name = input("Enter product name: ")
        description = input("Enter description: ")
        price = float(input("Enter price: "))
        condition = input("Enter condition (new, like new, used): ").lower()
        category_name = input("Enter category name: ")
        image_url = input("Enter image URL (optional, press Enter to skip): ")

        cursor = connection.cursor(dictionary=True)

        # Check if the category already exists, if not, create one
        query = "SELECT category_id FROM Category WHERE category_name = %s;"
        cursor.execute(query, (category_name,))
        category = cursor.fetchone()

        if category:
            category_id = category['category_id']
        else:
            query = "INSERT INTO Category (category_name) VALUES (%s);"
            cursor.execute(query, (category_name,))
            connection.commit()
            category_id = cursor.lastrowid
            print(f"Category '{category_name}' created with ID {category_id}.")

        query = """
            INSERT INTO Product (user_id, category_id, product_name, description, price, `condition`, image_url, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW());
        """
        cursor.execute(query, (user_id, category_id, product_name, description, price, condition, image_url or None))
        connection.commit()
        print("Product posted successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def browse_products(user_id):
    """Displays all available products with the option to view details or apply filters."""
    connection = connect_db()
    try:
        print("\n--- Browse Products ---")
        cursor = connection.cursor(dictionary=True)

        while True:
            print("\nOptions:")
            print("1. View All Products")
            print("2. Apply Filters")
            print("3. Go Back")
            option = input("Choose an option (1/2/3): ").strip()

            if option == '1':
                # Fetch and display all products
                query = "SELECT product_id, product_name, price FROM Product;"
                cursor.execute(query)
                products = cursor.fetchall()

                if products:
                    print("\nAvailable Products:")
                    for product in products:
                        print(f"ID: {product['product_id']}, Name: {product['product_name']}, Price: ${product['price']:.2f}")
                else:
                    print("No products available.")
            elif option == '2':
                # Apply filters
                min_price = float(input("Enter minimum price (or 0 to skip): ") or 0)
                max_price = float(input("Enter maximum price (or 0 to skip): ") or 0)
                condition = input("Enter condition (new, like new, used, or leave blank to skip): ").lower()

                query = """
                    SELECT product_id, product_name, price
                    FROM Product
                    WHERE (price >= %s OR %s = 0)
                      AND (price <= %s OR %s = 0)
                      AND (`condition` = %s OR %s = '');
                """
                cursor.execute(query, (min_price, min_price, max_price, max_price, condition, condition))
                products = cursor.fetchall()

                if products:
                    print("\nFiltered Products:")
                    for product in products:
                        print(f"ID: {product['product_id']}, Name: {product['product_name']}, Price: ${product['price']:.2f}")
                else:
                    print("No products match your filters.")
            elif option == '3':
                break
            else:
                print("Invalid option. Please try again.")

            # Allow the user to view product details or add to cart
            product_id = int(input("\nEnter the product ID to view details or add to cart (or 0 to return to options): ").strip())
            if product_id == 0:
                continue

            action = input("Would you like to (v)iew details or (a)dd to cart? (v/a): ").strip().lower()
            if action == 'v':
                # Fetch details for the selected product
                query = """
                    SELECT 
                        p.product_name,
                        p.description,
                        p.price,
                        p.condition,
                        p.image_url,
                        u.username AS seller,
                        c.category_name AS category,
                        p.created_at
                    FROM Product p
                    JOIN User u ON p.user_id = u.user_id
                    LEFT JOIN Category c ON p.category_id = c.category_id
                    WHERE p.product_id = %s;
                """
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()

                if product:
                    print("\n--- Product Details ---")
                    print(f"Name: {product['product_name']}")
                    print(f"Description: {product['description']}")
                    print(f"Price: ${product['price']:.2f}")
                    print(f"Condition: {product['condition']}")
                    print(f"Category: {product['category'] or 'Uncategorized'}")
                    print(f"Seller: {product['seller']}")
                    print(f"Posted on: {product['created_at']}")
                    if product['image_url']:
                        print(f"Image URL: {product['image_url']}")

                    # Record the view action in the history table
                    try:
                        query = """
                            INSERT INTO History (user_id, product_id, action_type, action_date)
                            VALUES (%s, %s, 'viewed', NOW());
                        """
                        cursor.execute(query, (user_id, product_id))
                        connection.commit()
                        print("This product has been added to your viewing history.")
                    except Error as e:
                        print(f"Error updating history: {e}")
                else:
                    print("Product not found.")
            elif action == 'a':
                # Add to cart
                try:
                    query = """
                        INSERT INTO History (user_id, product_id, action_type, action_date)
                        VALUES (%s, %s, 'added_to_cart', NOW());
                    """
                    cursor.execute(query, (user_id, product_id))
                    connection.commit()
                    print("Item added to cart.")
                except Error as e:
                    print(f"Error adding to cart: {e}")
            else:
                print("Invalid action. Please choose 'v' to view details or 'a' to add to cart.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()



def delete_item(user_id):
    """Delete an item posted by the user."""
    connection = connect_db()
    try:
        print("\n--- Delete an Item ---")
        product_id = int(input("Enter the product ID to delete: "))
        
        # Check if the product belongs to the user
        query = "SELECT product_id FROM Product WHERE product_id = %s AND user_id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (product_id, user_id))
        result = cursor.fetchone()
        
        if result:
            query = "DELETE FROM Product WHERE product_id = %s;"
            cursor.execute(query, (product_id,))
            connection.commit()
            print("Item deleted successfully.")
        else:
            print("You do not have permission to delete this item.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def update_item(user_id):
    """Update an existing item."""
    connection = connect_db()
    try:
        print("\n--- Update an Item ---")
        product_id = int(input("Enter the product ID to update: "))
        
        # Check if the product belongs to the user
        query = "SELECT product_id FROM Product WHERE product_id = %s AND user_id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (product_id, user_id))
        result = cursor.fetchone()
        
        if result:
            product_name = input("Enter new product name: ")
            description = input("Enter new description: ")
            price = float(input("Enter new price: "))
            condition = input("Enter new condition (new, like new, used): ").lower()

            query = """
                UPDATE Product
                SET product_name = %s, description = %s, price = %s, `condition` = %s, updated_at = NOW()
                WHERE product_id = %s;
            """
            cursor.execute(query, (product_name, description, price, condition, product_id))
            connection.commit()
            print("Item updated successfully.")
        else:
            print("You do not have permission to update this item.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()
