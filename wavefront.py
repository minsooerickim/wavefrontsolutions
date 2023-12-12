import os
from datetime import datetime

LOG_FILE = 'LongBeachLogs2023.txt'

def login():
    username = input("Enter your name for login: ")
    timestamp = datetime.now().strftime("%b %d %Y %H:%M")
    log_entry = f"{timestamp} : \"{username}\" logged in\n"
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)
    print(f"Welcome {username}!")

def upload_manifest():
    print("Please choose the file path for the manifest:")
    filepath = input("Enter the full path to your manifest file: ")
    if os.path.exists(filepath):
        print(f"Manifest '{filepath}' has been successfully uploaded.")
        display_manifest(filepath)
        after_upload_menu(filepath)
        return filepath
    else:
        print("The file path specified does not exist. Please try again.")
        return None

def display_manifest(filepath):
    print("\nManifest Contents:\n")
    with open(filepath, 'r') as file:
        for line in file:
            slot, _, content = line.strip().partition(', ')
            if 'UNUSED' not in content and 'NAN' not in content:
                # Only print out slots that are not UNUSED or NAN for clarity
                print(f"Slot: {slot} - Content: {content}")

def load_offload(manifest_path):
    if manifest_path:
        timestamp = datetime.now().strftime("%b %d %Y %H:%M")
        log_entry_start = f"{timestamp} load offload sequence for \"{os.path.basename(manifest_path)}\" started\n"
        log_entry_end = f"{timestamp} load offload sequence for \"{os.path.basename(manifest_path)}\" finished\n"
        with open(LOG_FILE, 'a') as file:
            file.write(log_entry_start)
        
        print("You've selected Load/Offload.")
        offload_containers(manifest_path)
        onload_containers(manifest_path)

        with open(LOG_FILE, 'a') as file:
            file.write(log_entry_end)
    else:
        print("Please upload a manifest before attempting to load or offload containers.")


def offload_containers(manifest_path):
    offload = input("Enter the x,y coordinates of the container to offload (e.g., 01,02) or 'done' to finish: ")
    while offload.lower() != 'done':
        # Here you would have the logic to offload the container
        print(f"Container at {offload} scheduled for offloading.")
        offload = input("Enter the x,y coordinates of the next container to offload or 'done' to finish: ")

def onload_containers(manifest_path):
    onload = input("Enter the x,y coordinates of the container to onload (e.g., 02,03) or 'done' to finish: ")
    while onload.lower() != 'done':
        # Here you would have the logic to onload the container
        print(f"Container at {onload} scheduled for onloading.")
        onload = input("Enter the x,y coordinates of the next container to onload or 'done' to finish: ")

def after_upload_menu(filepath):
    while True:
        print("\nWhat would you like to do next?")
        print("1. Balance")
        print("2. Load/Offload")
        print("3. Return to Main Menu")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            print("Balance function is not implemented yet.")
            break
        elif choice == '2':
            load_offload(filepath)
            break
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

def menu():
    print("Menu functionality will be implemented soon.")

def main():
    manifest_path = None
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
            manifest_path = upload_manifest()
        elif choice == '3':
            menu()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
