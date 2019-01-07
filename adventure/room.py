from inventory import Inventory


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initialize a Room
        give it an id, name and description
        """
        self.id = id
        self.name = name
        self.description = description
        self.inventory = Inventory()
        # saving the connections between rooms in the dictionary "connections"
        self.connections = {}

    def valid(self, direction, inventory):
        """
        Returns integer with room_list position of the room if movement is allowed.
        Checks inventory if conditional movements are possible.
        If direction is not valid, returns False.
        """
        # if direction is valid, return True
        if direction in self.connections:
            location_list = self.connections[direction]
            for location in location_list:
                # checking for conditional movements
                if "/" in location:
                    split_location = location.split("/")
                    location = split_location[0]
                    condition = split_location[1]
                    for item in inventory:
                        if item.name == condition:
                            return(int(location) - 1)
                elif location.isdigit:
                    return(int(location) - 1)
        else:
            return False

    def __str__(self):
        return f"{self.description}"

