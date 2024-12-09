from products import post_item, browse_products, delete_item, update_item
from history import view_history
from checkout import checkout
from wishlist import add_to_wishlist, delete_from_wishlist, view_wishlist
from comments import add_comment, view_comments

def user_dashboard(user_id):
    """Main dashboard for user."""
    while True:
        print("\n--- User Dashboard ---")
        print("1. Post Item")
        print("2. Browse Products")
        print("3. View History")
        print("4. Delete Item")
        print("5. Update Item")
        print("6. Add to Wishlist")
        print("7. Remove from Wishlist")
        print("8. View Wishlist") 
        print("9. Add Comment")
        print("10. View Comments")
        print("11. Checkout")
        print("12. Logout")

        choice = input("Choose an option (1/2/3/4/5/6/7/8/9/10/11/12): ").strip()
        if choice == '1':
            post_item(user_id)
        elif choice == '2':
            browse_products(user_id)
        elif choice == '3':
            view_history(user_id)
        elif choice == '4':
            delete_item(user_id)
        elif choice == '5':
            update_item(user_id)
        elif choice == '6':
            product_id = int(input("Enter the product ID to add to your wishlist: "))
            add_to_wishlist(user_id, product_id)
        elif choice == '7':
            product_id = int(input("Enter the product ID to remove from your wishlist: "))
            delete_from_wishlist(user_id, product_id)
        elif choice == '8':
            view_wishlist(user_id)
        elif choice == '9':
            product_id = int(input("Enter the product ID to comment on: "))
            add_comment(user_id, product_id)
        elif choice == '10':
            product_id = int(input("Enter the product ID to view comments: "))
            view_comments(product_id)
        elif choice == '11':
            checkout(user_id)
        elif choice == '12':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")