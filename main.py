import sys
import time

rooms = {
    'Foyer': {
        'description': 'A dimly lit entrance hall with a grand staircase.',
        'connections': ['Library', 'Dining Room'],
        'items': []
    },
    'Library': {
        'description': 'Walls lined with ancient books. A cold draft chills you.',
        'connections': ['Foyer', 'Study'],
        'items': ['Silver Key']
    },
    'Dining Room': {
        'description': 'An elegant dining room with an old chandelier.',
        'connections': ['Foyer', 'Kitchen'],
        'items': []
    },
    'Kitchen': {
        'description': 'A dark kitchen filled with strange smells.',
        'connections': ['Dining Room', 'Basement'],
        'items': ['Flashlight']
    },
    'Study': {
        'description': 'A room with large piano.',
        'connections': ['Library'],
        'items': []
    },
    'Basement': {
        'description': 'A creepy dark basement.',
        'connections': ['Kitchen'],
        'items': []
    },
}

class Player:
    def __init__(self):
        self.inventory = []

# Initialize the player with an empty inventory
player = Player()

class Furniture:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.opens_with = None

# Initialize the player with an empty inventory
player = Player()

# Initialize a piece of furniture with an empty inventory
furniture = Furniture("Oak Drawer", "A beautifully carved wooden drawer.")
furniture = Furniture("Oak Drawer", "A beautifully carved wooden drawer.")

def check_items(items, room):
    keep_item = None
    if len(items) > 1:
        print(f"You found a {', '.join(items[:-1])}, and a {items[-1]}.")
        print("-" * 40)
        keep_item = input("Do you want to keep any of these items? (yes/no): ").strip().lower()
        if keep_item == 'yes':
            item_to_keep = input(f"Which item do you want to keep? {', '.join(items)}: ").strip()
            # Check if the item is in the room's items and add it to the player's inventory while removing it from the room
            item_to_keep = item_to_keep.title()  # Normalize input to match item names
            if item_to_keep in items:
                player.inventory.append(item_to_keep)
                rooms[room]['items'].remove(item_to_keep)
                print(f"You have kept the {item_to_keep}.")
                print("-" * 40)
        else:
            print("You chose not to keep any items.")
            print("-" * 40)
    elif len(items) == 1:
        print(f"You found a {items[0]}.")
        print("-" * 40)
        keep_item = input(f"Do you want to keep the {items[0]}? (yes/no): ").strip().lower()
        if keep_item == 'yes':
            # Check if the item is in the room's items and add it to the player's inventory while removing it from the room
            item_to_keep = items[0]
            if item_to_keep in items:
                player.inventory.append(item_to_keep)
                rooms[room]['items'].remove(item_to_keep)
                print(f"You have kept the {item_to_keep}.")
                print("-" * 40)

        else:
            print("That item is not available.")
            print("-" * 40)
    return

def move_to_room(new_room):
    return new_room

def describe_room(room):
    print(f"You are in the {room}.")
    print("-" * 40)
    print(rooms[room]['description'])
    print(f"From here you can access the {' and the '.join(rooms[room]['connections'])}.")
    print("What would you like to do next?")
    print("-" * 40)
    return

# This function prints text slowly, simulating a typewriter effect
def print_slow(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after printing

def main():
    # current_room sets the starting point of the game
    current_room = 'Foyer'
    # is_game_running controls the game loop
    is_game_running = True
    # printing the welcome message
    #print_slow("""
#Welcome to the Escape the Haunted Mansion game!
#You wake up on a couch and find yourself in a strange house with no windows. 
#You don’t remember how you got here, but a chilling sense of danger fills the air. 
#You must escape the house, and quickly!
#Navigate through rooms, collect items, and find your way out.
#You can type 'inventory' to check your items at any time.
#Good luck!""")
    # while loop to keep the game running or until the player decides to quit
    while is_game_running:
        # describe_room 
        describe_room(current_room)
        user_input = input("""
Would you like to check for items in this room?
Please type 'items' OR 
type a room name to move to the next room.
Type 'Quit' to exit the game.
        """).strip().lower()
        print("-" * 40)
        # If the user input is 'quit', the game ends.
        if user_input == 'quit':
            print("Game over")
            is_game_running = False
            
        elif user_input == 'inventory':
            # If the user input is 'inventory', it shows the player's inventory.
            if player.inventory:
                print(f"Your inventory: {', '.join(player.inventory)}")
                print("-" * 40)
            else:
                print("Your inventory is empty.")
                print("-" * 40)

        # If the user input is 'items', it checks for items in the current room.
        elif user_input == 'items':
            items = rooms[current_room]['items']
            if items != []: # check if list is not empty
                check_items(items, current_room)
            else:
                print("There are no items in this room.")
                print("-" * 40)
            
        # If the user input is a valid room name, it moves to that room.        
        elif user_input.title() in rooms[current_room]['connections']:
            new_room = user_input.title()
            current_room = move_to_room(new_room)
        else:
            print("Invalid command. You can't go that way. Please try again.")

main()