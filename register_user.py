"""
Simple script to register users via console
"""
import sys
sys.path.insert(0, 'client')

from database import UserDatabase

def main():
    db = UserDatabase()

    print("=== Telegraf User Registration ===")
    print()

    username = input("Enter username (min 3 chars): ").strip()
    password = input("Enter password (min 4 chars): ").strip()

    print()
    print("Registering...")

    success, result = db.register_user(username, password)

    if success:
        print(f"SUCCESS! User '{username}' registered with ID: {result}")
        print()
        print("Now you can login in the app with:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
    else:
        print(f"ERROR: {result}")

if __name__ == "__main__":
    main()
