import os
from datetime import datetime

LOG_FILE = 'LongBeachLogs2023.txt'

def login():
    username = input("Enter your name for login: ")
    timestamp = datetime.now().strftime("%b %d %Y %H:%M")
    log_entry = f'{timestamp} : \"{username}\" logged in\n'
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)
    print(f"Welcome {username}!")

def upload_manifest():
    print("Please choose the file path for the manifest:")
    filepath = input("Enter the full path to your manifest file: ")
    if os.path.exists(filepath):
        print(f"Manifest '{filepath}' has been successfully uploaded.")
    else:
        print("The file path specified does not exist. Please try again.")

def menu():
    print("Menu functionality will be implemented soon.")

def main():
    while True:
        print("\nWavefront Solutions\n")
        print("1. Login")
        print("2. Upload Manifest")
        print("3. Menu")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            login()
        elif choice == '2':
            upload_manifest()
        elif choice == '3':
            menu()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
