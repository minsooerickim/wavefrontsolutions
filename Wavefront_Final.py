import os
from datetime import datetime
from Search8 import Node, Search

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
        with open(filepath, 'r') as file:
            # Check if the file is empty
            if file.read().strip() == '':
                print("The manifest file is empty.")
                return None
            file.seek(0)

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



def parse_manifest_to_array_for_balance(manifest_path):
    """
    Parses manifest and puts weight as value in the correct x, y position in 2D array
    """
    # Initialize an empty 12x8 grid filled with zeros
    grid = [[0 for _ in range(8)] for _ in range(8)]

    with open(manifest_path, 'r') as file:
        for line in file:
            # Split the line and extract the necessary parts
            parts = line.strip().split(', ')
            position = parts[0].strip("[]")
            row, col = map(int, position.split(','))
            weight = int(parts[1].strip("{}"))
            grid[row - 1][col - 1] = weight


    return grid

def balance_containers(manifest_path):
    if manifest_path:
        print("Balancing the containers...")

        # Load the manifest into an array
        grid = parse_manifest_to_array_for_balance(manifest_path)

        # Perform the balancing search
        search_obj = Search(len(grid))
        result_node = search_obj.process(grid, 0.9)

        if result_node:
            print("Found a balanced configuration:")
            result_node.print_grid()
            print("Balance score:", search_obj.balance_score(result_node.grid))
        else:
            print("No balanced configuration found.")

def after_upload_menu(filepath):
    while True:
        print("\nWhat would you like to do next?")
        print("1. Balance")
        print("2. Load/Offload")
        print("3. Return to Main Menu")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            balance_containers(filepath)
            break
        elif choice == '2':
            # Call the load_unload_containers method from the Node class
            unload_input = input("Enter the unload positions as pairs separated by commas (e.g., 2-5,4-6,5-6): ")
            unload_positions = [tuple(map(int, pair.split('-'))) for pair in unload_input.split(',')]
            dock_input = input("Enter the dock positions separated by commas (e.g., 1,2,2,3,3,4,3,2,1): ")
            dock = list(map(int, dock_input.split(',')))
            grid = parse_manifest_to_array_for_balance(filepath)
            initial_node = Node(grid, 0, 0, None)
            initial_node.unload_containers(unload_positions)
            initial_node.branch_loadoffload(dock)
            
            break
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

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
            manifest_path = upload_manifest()
        elif choice == '3':
            menu()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

arr_ship = [
    [0, 0, 0, 0, 3, 2, 1, 1],
    [0, 0, 0, 0, 0, 0, 5, 4],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 4, 1, 1, 2, 2, 3, 2],
    [0, 0, 0, 0, 0, 0, 9, 8],
    [0, 0, 0, 0, 3, 2, 3, 8]
]

arr_dock = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3],
    [0, 1, 6, 4]
]
    
if __name__ == "__main__":
    main()