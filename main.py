from login import create_account, login
from dashboard import user_dashboard

def main_menu():
    """Main menu for the CLI Second-hand trading platform application."""
    while True:
        print("\n--- Main Menu ---")
        print("1. Create Account")
        print("2. Log In")
        print("3. Exit")
        
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            user_id = login()  # Retrieve user_id upon successful login
            if user_id:  # Proceed to the dashboard if login is successful
                user_dashboard(user_id)
        elif choice == '3':
            print("Exiting the application. See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Welcome to the CLI Second-hand trading platform application!")
    main_menu()