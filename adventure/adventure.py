from room import Room
import sys
from item import Item
from inventory import Inventory


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """

        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.items = self.load_items(f"data/{game}Items.txt")
        self.synonyms = self.load_synonyms(f"data/SmallSynonyms.txt")

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a collection of Room objects.
        """
        self.room_number = 0

        with open(filename, "r") as file:
            # create list for saving the read data
            self.room_list = []
            # read 3 lines of data for id, name and description and save it
            for text_line in file:
                # strip end of line
                text_line = text_line.strip()
                if text_line.isdigit():
                    id = text_line
                    text_line = file.readline().strip()
                    name = text_line
                    text_line = file.readline().strip()
                    description = text_line
                    self.room = Room(id, name, description)
                    self.room_list.append(self.room)

                elif text_line.isupper():
                    split_line = text_line.rsplit()
                    # direction is the user input
                    direction = split_line[0]
                    # movement is the room to move to after giving direction
                    movement = split_line[1]

                    # if key in dictionary already exists, add option to list
                    if direction in self.room_list[-1].connections:
                        self.room_list[-1].connections[direction].append(movement)
                    else:
                        self.room_list[-1].connections[direction] = [movement]

        # initialization of current_location at postion 0 (self.room_number = 0)
        self.current_room = self.room_list[self.room_number]

    def load_items(self, filename):
        """
        Loads items from item file.
        Places items into the inventory of the correct room.
        """
        # Creating player inventory
        self.inventory_player = Inventory()

        with open(filename, "r") as file:
            self.location_items = []
            counter = 0
            for text_line in file:
                text_line = text_line.strip()

                # getting name
                if text_line.isupper():
                    name = text_line

                # getting description
                elif text_line.islower():
                    description = text_line

                # getting original_room_id
                elif text_line.isdigit:
                    initial_room_id = text_line
                    # assigning the item to the proper room
                    for room in self.room_list:
                        if initial_room_id == room.id:
                            room.inventory.add(Item(name, description,
                                                    initial_room_id))

    def load_synonyms(self, filename):
        """
        Load abbreviations of commands into a dictionary
        """
        self.synonyms_dict = {}

        with open(filename, "r") as file:
            self.location_items = []
            counter = 0
            for text_line in file:
                text_line = text_line.strip()

                split_line = text_line.split("=")
                self.synonyms_dict[split_line[0]] = split_line[1]

    def take(self, item):
        """
        Places items into the inventory of the player.
        """
        # Checks if the item in current room
        if self.current_room.inventory.return_inventory(item):
            item = self.current_room.inventory.return_inventory(item)
            self.current_room.inventory.remove(item)
            self.inventory_player.add(item)
            print(f"{item.name} taken")
        else:
            print("No such item")

    def drop(self, item):
        """
        Function for dropping items into the current room.
        """
        if self.inventory_player.return_inventory(item):
            item = self.inventory_player.return_inventory(item)
            self.inventory_player.remove(item)
            self.current_room.inventory.add(item)
            print(f"{item.name} dropped")
        else:
            print("No such item")

    def help_command(self):
        """
        Returns help text
        """
        print(f"""
You can move by typing directions such as EAST/WEST/IN/OUT
QUIT quits the game.
HELP prints instructions for the game.
INVENTORY lists the item in your inventory.
LOOK lists the complete description of the room and its contents.
TAKE <item> take item from the room.
DROP <item> drop item from your inventory.
        """)

    def quit_command(self):
        """
        Exits game.
        """
        print("Thanks for playing!")
        sys.exit()

    def look_command(self):
        """
        prints description of room and items in inventory.
        """
        print(self.current_room)
        if self.current_room.inventory.check_inventory():
            print(self.current_room.inventory)

    def won(self):
        """
        Check if the game is won.
        Returns a boolean.
        """
        if int(self.room_number) < 0:
            return True
        else:
            False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """

        # TODO: Update the current room to a connected direction.
        # room number is returned by the .valid function of Room. However, this number
        # represents the id, not the actual location in the room_list. To get the location in
        # the room_list, simply subtract 1 to get to the proper location.
        inventory = self.inventory_player.item_list
        if (self.current_room.valid(direction, inventory)) is False:
            print("Invalid command")
        else:
            self.room_number = self.current_room.valid(direction, inventory)
            self.current_room = self.room_list[self.room_number]
        while "FORCED" in (self.current_room.connections):
            if self.current_room.description == "-----":
                pass
            else:
                print(self.current_room)
            direction = "FORCED"
            self.room_number = self.current_room.valid(direction, inventory)
            self.current_room = self.room_list[self.room_number]
            if self.won():
                break

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")

        # print description of first room
        print(self.current_room)

        # create array for controlling if someones been in a room before
        room_visited = []
        # add the first room to this list
        room_visited.append(0)

        # Prompt the user for commands until they've won the game.
        while not self.won():
            command = input("> ").upper()
            # if one letter commands, check with synonyms_dictionary
            if command in ["Q", "L", "I", "N", "S", "E", "W", "U", "D"]:
                command = self.synonyms_dict[command]
            # check if command is legal movement
            if command in self.current_room.connections:
                self.move(command)
                #  if room_number is in array
                if self.room_number in room_visited:
                    # short description
                    print(self.current_room.name)
                    # items in room
                    if self.current_room.inventory.check_inventory():
                        print(self.current_room.inventory)
                else:
                    # add room_number to visited rooms if it has a description
                    if self.current_room == "-----" or self.won():
                        pass
                    # else print the description, add room_number and print
                    # items in list
                    else:
                        room_visited.append(self.room_number)
                        print(self.current_room)
                        if self.current_room.inventory.check_inventory():
                            print(self.current_room.inventory)

            elif command == "LOOK":
                self.look_command()

            elif command == "HELP":
                self.help_command()

            elif command == "QUIT":
                self.quit_command()

            elif command == "INVENTORY":
                if self.inventory_player.check_inventory():
                    print(self.inventory_player)
                else:
                    print("Your inventory is empty")

            elif " " in command:
                split_command = command.rsplit()
                if len(split_command) == 2:
                    if split_command[0] == "TAKE":
                        self.take(split_command[1])

                    elif split_command[0] == "DROP":
                        self.drop(split_command[1])
                    else:
                        print("Invalid command")
                # if command is longer than 2 words, it is a invalid command
                else:
                    print("Invalid command")
            else:
                print("Invalid command")


if __name__ == "__main__":
    adventure = Adventure("Crowther")
    adventure.play()
