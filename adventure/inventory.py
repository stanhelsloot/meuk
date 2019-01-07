class Inventory(object):
    """
    Representation of inventory object in adventure
    """

    def __init__(self):
        # a list for the items in the inventory
        self.item_list = []

    def add(self, item):
        self.item_list.append(item)

    def remove(self, item):
        self.item_list.remove(item)

    def check_inventory(self):
        """
        Returns True if item(s) in inventory.
        Returns False otherwise
        """
        if len(self.item_list) > 0:
            return True
        else:
            return

    def return_inventory(self, item):
        """
        Returns item from inventory if input matches with it.
        Returns False if no matches present.
        """
        for objects in self.item_list:
            if objects.name == item:
                return objects
        return False

    def __str__(self):
        """
        Returns a string of joined items.
        """
        if len(self.item_list) is not 0:
            item_return_list = []
            for item in self.item_list:
                item_return_list.append(f"{item}")
            return '\n'.join(item_return_list)
        else:
            return("Inventory is currently empty")