import sys
import time

# Create a Player class to manage the player's inventory
class Player:
    def __init__(self):
        self.inventory = []
        
# Initialize the player with an empty inventory
player = Player()

# Create a base class for objects in the game
class Object:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        
# Create a subclass for furniture that can be moved
class MovableObject(Object):
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self.is_portable = True
        
    # This method allows the player to pick up the object and add it to their inventory
    def pick_up(self, player):
        player.inventory.append(self)

# Create a subclass for furniture that cannot be moved
class ImmovableObject(Object):
    def __init__(self, name, description="", opens_with=None, plays_with=None, has_item=False, is_hidden=False):
        super().__init__(name, description)
        self.is_portable = False
        self.opens_with = opens_with
        self.plays_with = plays_with
        self.has_item = has_item
        self.is_hidden = is_hidden
    
    # This method allows the object to be shown if it is hidden
    def show(self):
        self.is_hidden = False

    # This method allows the object to be updated with a new description
    def update_description(self, new_description):
        self.description = new_description
    
    # This method allows the object to be updated with a new description
    def update_piano(self):
        self.plays_with = False
        
# Initialize movable objects that can be picked up
book = MovableObject("Book", "A draft on the book reads 'A Key Behind a Portrait.' and 'Do La Si 📃 🎶'.")
silver_key = MovableObject("Silver Key", "A shiny silver key that looks like it could open something important.")
flashlight = MovableObject("Flashlight", "A dusty flashlight that might come in handy in the dark basement.")
screwdriver = MovableObject("Screwdriver", "A rusty screwdriver that looks like it has seen better days.")

# Initialize movable objects that cannot be picked up
main_gate = ImmovableObject("Main Gate", "A large iron gate that is locked. It seems it is the only way out, but it is locked!", opens_with=silver_key)
bookshelf = ImmovableObject("Bookshelf", "A beautifully carved wooden bookshelf with many books. But wait, there is a book that seems to be out of place on the shelf. 📖", has_item=True)
piano = ImmovableObject("Piano", "A grand piano with a dusty cover. It looks like it hasn't been played in years.", plays_with='do la si')
chandelier = ImmovableObject("Chandelier", "An old chandelier that hangs precariously from the ceiling. It looks like it could fall at any moment.", has_item=True, is_hidden=True)
cupboard = ImmovableObject("Cupboard", "A wooden cupboard with a brass handle. There seems to be something in one of its drawers.", has_item=True)
house_portrait = ImmovableObject("Portrait of a House", "A large portrait of a house. It looks like it could be of this mansion I am in just now! It looks like it can be moved.", opens_with=screwdriver, is_hidden=True)
dracula_portrait = ImmovableObject("Portrait of Dracula", "A large portrait of Dracula. He looks frightening. It looks like it can be moved.", opens_with=screwdriver)

# Initialize the rooms with their descriptions, connections, and items
rooms = {
    'Foyer': {
        'description': 'A dimly lit entrance hall with a grand staircase.',
        'connections': ['Library', 'Dining Room'],
        'items': [main_gate]
    },
    'Library': {
        'description': 'Walls lined with ancient books. A cold draft chills you.',
        'connections': ['Foyer', 'Study'],
        'items': [bookshelf, book]
    },
    'Dining Room': {
        'description': 'An elegant dining room with an old chandelier.',
        'connections': ['Foyer', 'Kitchen'],
        'items': [chandelier, screwdriver]
    },
    'Kitchen': {
        'description': 'A dark kitchen filled with strange smells.',
        'connections': ['Dining Room', 'Basement'],
        'items': [cupboard, flashlight]
    },
    'Study': {
        'description': 'A room with a large piano.',
        'connections': ['Library'],
        'items': [piano]
    },
    'Basement': {
        'description': 'A creepy dark basement.',
        'connections': ['Kitchen'],
        'items': [house_portrait, dracula_portrait, silver_key]
    },
}

# is_game_running controls the game loop
is_game_running = True

# This function prints a welcome message to the player
def welcome_message():
    print_slow("""
Welcome to the Escape the Haunted Mansion game! 👻
You wake up on a couch and find yourself in a strange house with no windows.
You don’t remember how you got here, but a chilling sense of danger fills the air.
You must escape the house, and quickly!
Navigate through rooms, collect items, and find your way out.
You can type 'inventory' to check your items at any time.
Good luck! 🎃
""")

# This function checks for movable items in the room
def check_movable_items(non_portable_item, portable_item, room, player):
    # Checks if list is empty
    if portable_item == []:
        print(f"There are no items left to be picked up from the {non_portable_item[0].name}.")
        print("-" * 40)
        return
    else:
        item = portable_item[0] if portable_item else None
        print(f"You found a {item.name}!")
        print("-" * 40)
        keep_item = input(f"Would you like to keep the {item.name}? (yes/no): ").strip().lower()
        print("-" * 40)
        if keep_item == 'yes':
            # Check if the item is in the room's items and add it to the player's inventory while removing it from the room
            if item in rooms[room]['items']:
                item.pick_up(player)
                rooms[room]['items'].remove(item)
                print(f"You have added the {item.name} to your inventory.")
                print("-" * 40)
                if item.name == 'Book':
                    bookshelf.update_description("The bookshelf now has an empty spot where the mysterious book once was.")
                if item.name == 'Flashlight':
                    print("You can now see in the dark basement!")
                    print("-" * 40)
                    house_portrait.show()
                    cupboard.update_description("The cupboard now has an empty spot where the flashlight once was.")
            else:
                print("That item is not available.")
                print("-" * 40)
        else:
            print(f"You chose not to keep the {item.name}.")
            print("-" * 40)
                
        return
    
# This function checks the main gate in the Foyer
def check_main_gate(item):
    global is_game_running
    user_input = input(f"You see the {item.name}. Would you like to examine it? (yes/no): ").strip().lower()
    print("-" * 40)
    if user_input == 'yes':
        if getattr(item, 'opens_with', None):
            print(f"The {item.name} can only be opened with the {item.opens_with.name}. 🗝️")
            if player.inventory and any(inv_item.name == item.opens_with.name for inv_item in player.inventory):
                print(f"You have the {item.opens_with.name}! You can open the {item.name}. 😄")
                print("-" * 40)
                user_input = input(f"Would you like to open the {item.name}? (yes/no): ").strip().lower()
                print("-" * 40)
                if user_input == 'yes':
                        print(f"You opened the {item.name}! ✨")
                        # Check if the item is the Main Gate and if the player has the Silver Key player wins
                        if item.name == 'Main Gate':
                            print("""
You managed to escape from the haunted mansion! 
You won! 
🥳 🎉
""")
                            # Set the game running flag to False to end the game
                            is_game_running = False
                            return
                else:
                    print(f"You chose not to open the {item.name}. 🤯")
                    print("-" * 40)
            else:
                print(f"""
It seems to be the only way out, but it is locked! 😥
I wonder where I can find the key to open it!
""")
                print("-" * 40)
    else:
        print(f"You chose not to examine the {item.name}.")
        print("-" * 40)
        return

# This function checks the piano in the Study
def check_piano(piano):
    if not piano.plays_with == False:
        user_input = input("Alright, that is an old piano! Should I try to play it? (yes/no): ").strip().lower()
        print("-" * 40)
        if user_input == 'yes':
            played_notes = input(f"""
I should play some random notes on the piano 🎹 (e.g., do, re, mi). 
Perhaps I can find some music sheets in the Library? 
Or should I check the inventory for some clue? Anyway, I'll play on! 🎵
{'-' * 40}
""").strip().lower()
            print("-" * 40)
            # Check if the played notes match the piano's plays_with attribute
            if played_notes == piano.plays_with:
                print(f"You played the notes '{piano.plays_with}' on the piano and it echoes loudly throughout the house 🎶 !")
                print("💥 Bang! It sounds like the chandelier just fell down in the Dining Room! Go check it out!")
                print("-" * 40)
                # Show the chandelier
                chandelier.show()
                # Update the piano's plays_with attribute to False
                piano.update_piano()
            else:
                print("You play the piano, but it doesn't produce any sound.")
                print("-" * 40)
        else:
            print("You chose not to play the piano.")
            print("-" * 40)
    else:
        print("The piano is silent now. It seems like it has been played enough for today.")
        print("-" * 40)

# This function checks the chandelier in the Dining Room
def check_chandelier(item):
    if item.is_hidden == True:
        print(f"""
I see a chandelier hanging from the ceiling. 
It looks like it can fall at any moment. 
Strange, but I can see a screwdriver suspended from the chandelier, but I can't reach it.
""")
        print("-" * 40)
        return None
    elif item.is_hidden == False:
        user_input = input(f"The chandelier lies shattered on the floor. Would you like to examine it? (yes/no): ").strip().lower()
        print("-" * 40)
    return user_input

# This function checks for items in the basement
def check_basement_items(non_portable_items, portable_items, room, player):
    global is_game_running
    # Check if the house portrait is hidden
    if house_portrait.is_hidden:
        print("""
The basement is dark and eerie.
I can barely see anything. 
Maybe I should look for a flashlight?
""")
        print("-" * 40)
    elif house_portrait.is_hidden == False:
        print("""
Now that I have the flashlight, I can see two portraits in the basement! 💡
It seems that they can be removed from the wall:
""")
        print("-" * 40)
        for item in non_portable_items:
            print(f"- {item.name}")
            print("-" * 40)
        user_input = input("Would you like to inspect one of these portraits? (yes/no): ").strip().lower()
        print("-" * 40)
        if user_input == 'yes':
            user_input = input("Which portrait would you like to inspect? (Portrait of a House or Portrait of Dracula): ").strip()
            print("-" * 40)
            # Normalize both user input and item names to lower case for comparison
            portrait_input = next((j for j in non_portable_items if j.name.lower() == user_input.lower()), None)
            if not portrait_input:
                print("Invalid choice. Please try again.")
                print("-" * 40)
                return
            if portrait_input.name == 'Portrait of a House' and silver_key not in rooms[room]['items']:
                print("The Silver Key has already been taken. Rush to the Main Gate!")
                print("-" * 40)
            elif portrait_input.name == 'Portrait of a House' and any(item.name == house_portrait.opens_with.name for item in player.inventory):
                print("Now that I have the screwdriver, I can remove the portrait from the wall. 🙏")
                print("I found a Silver Key behind the portrait 🗝️! I can use it to open the Main Gate. ✨")
                print("-" * 40)
                user_choice = input("Would you like to take the Silver Key? (yes/no): ").strip().lower()
                print("-" * 40)
                if user_choice == 'yes':
                    new_item = portable_items[0] if portable_items else None
                    # Add the Silver Key to the player's inventory and remove it from the room
                    new_item.pick_up(player)
                    print("Now I have the Silver Key. Better rush to the Main Gate! 😁")
                    print("-" * 40)
                    print("You have added the Silver Key to your inventory.")
                    rooms[room]['items'].remove(new_item)
                    print("-" * 40)
                else:
                    print("You chose not to take the Silver Key. 🤯")
                    print("-" * 40)
            elif portrait_input.name == 'Portrait of Dracula' and house_portrait.opens_with in player.inventory:
                print("Now that I have the screwdriver, I can remove the portrait from the wall.")
                print('-' * 40)
                print("""
Oh no! 😱 
Dracula appears behind the portrait and attacks you!
Game over
🧛🦇
""")
                print("-" * 40)
                # Set the game running flag to False to end the game
                is_game_running = False
                return
            elif portrait_input.name == 'Portrait of a House' or portrait_input.name == 'Portrait of Dracula':
                print("What a spooky portrait! It looks like it can be moved, but I need a screwdriver in order to do that.")
                print("-" * 40)
        else:
            print("You chose not to examine any of the portraits.")
            print("-" * 40)

# This function checks for immovable items in the room
def check_immovable_items(non_portable_items, portable_items, room, player):
    # Checks if there is a single non-portable object in the room
    if len(non_portable_items) == 1:
        item = non_portable_items[0]
        if room == 'Foyer' and item.name == 'Main Gate':
            check_main_gate(item)

        # Checks if the item is the piano
        elif room == 'Study' and item.name == 'Piano':
            check_piano(item)

        elif item.name == 'Chandelier':
            user_input = check_chandelier(item)
            if user_input == 'yes':
            # If the immovable object stores an item, check if the player wants to take it
                if item.has_item and not item.is_hidden:
                    check_movable_items(non_portable_items, portable_items, room, player)
                    
            elif chandelier.is_hidden == False:
                print(f"You chose not to examine the {item.name}.")
                print("-" * 40)
                
        # Checks if the item is the bookshelf or cupboard
        elif item.name == 'Bookshelf' or item.name == 'Cupboard':
            user_input = input(f"You see a {item.name}. Would you like to examine it? (yes/no): ").strip().lower()
            print('-' * 40)
            if user_input == 'yes':
                print(item.description)
                print("-" * 40)
                # If the immovable object stores an item, check if the player wants to take it
                if item.has_item and not item.is_hidden:
                    check_movable_items(non_portable_items, portable_items, room, player)
            else:
                print(f"You chose not to examine the {item.name}.")
                print("-" * 40)
            
    # Checks if there are at least two non-portable objects in the room and if the room is the Basement
    elif len(non_portable_items) >= 2 and room == 'Basement':
        check_basement_items(non_portable_items, portable_items, room, player)

# This function moves the player to a new room
def move_to_room(new_room):
    return new_room

# This function describes the current room and its connections
def describe_room(room):
    print(f"You are in the {room}.")
    print("-" * 40)
    print(rooms[room]['description'])
    print(f"From here you can access the {' and the '.join(rooms[room]['connections'])}.")
    print("-" * 40)
    return

# This function checks the player's inventory and prints the items they have collected
def inventory():
    if player.inventory:
        print("Your inventory:")
        for item in player.inventory:
            print(f"- {item.name}: {item.description}")
    else:
        print("Your inventory is empty.")
    print("-" * 40)

# This function prints text slowly, simulating a typewriter effect
def print_slow(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after printing
    
def main(player):
    global is_game_running
    # current_room sets the starting point of the game
    current_room = 'Foyer'
    
    # printing the welcome message
    welcome_message()
    print("-" * 40)

    # while loop to keep the game running or until the player decides to quit
    while is_game_running:
        # describe_room
        describe_room(current_room)
        user_input = input(f"""
Type 'explore' to check for items in this room.
Type {' or '.join(rooms[current_room]['connections'])} to move to the next room.
Type 'inventory' to check your inventory.
Type 'quit' to exit the game.
{'-' * 40}
        """).strip().lower()
        print("-" * 40)
        
        # If the user input is 'quit', the game ends.
        if user_input == 'quit':
            print("Game over")
            is_game_running = False
            
        # Displays the player's inventory if the user input is 'inventory'.
        elif user_input == 'inventory':
            inventory()
                
        # If the user input is 'explore', it checks for items in the current room.
        elif user_input == 'explore':
            non_portable_items = [item for item in rooms[current_room]['items'] if not item.is_portable]
            portable_items = [item for item in rooms[current_room]['items'] if item.is_portable]
            item_names = ' and '.join([item.name for item in non_portable_items])

            # check if room has items
            if non_portable_items:
                check_immovable_items(non_portable_items, portable_items, current_room, player)
            else:
                print(f"There are no items in this room.")
                print("-" * 40)
                
        # If the user input is a valid room name, it moves to that room.
        elif user_input.title() in rooms[current_room]['connections']:
            destination = user_input.title()
            current_room = move_to_room(destination)
        else:
            print("Oops, invalid input. Please try again.")
            print('-' * 40)

# Start the game
main(player)