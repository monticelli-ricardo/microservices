# Type hinting in Python 3.10+
# if your python is < 3.10 then uncomment the following
# from typing import str

from typing import List, Union


def get_full_name(firstname: str, lastname: str):
    return firstname.title() + " " + lastname.upper()

# Hinting lists
a_list_of_names = ["nizar", "slah", "ayed"]

def process(a_list: List[str]):
    for name in a_list:
        print(name.title())

# Hinting Dicts
an_inventory = {
    "product 1": 10.2,
    "product 2": 12.5,
    "product 3": 11.4,
    "product 4": 15.2,
}

def process_dict(an_inventory: dict[str, float]):
    for product, price in an_inventory.items():
        print("the", product.title(),
              "is offered at", price,"euro(s)")


# Union
a_mixed_list = [1, 2, "name1", "name2", [1, 2]]
#process(a_mixed_list)

def process_mixed(a_list: list[str | int]):
    for item in a_list:
        print(item, "is of type",
              "int" if type(item) is int
                    else "str" if type(item) is str
                    else "other")
        

def optimal_process(a_list: list[str | int | list]):
    for item in a_list:
        print(item.title() if type(item) is str
              else "a list of length " + str(len(item)) if type(item) is list
              else item)


# Optional
# For example, to create an item in a database, we need an id.
# Should we compute the Id ? No, of course
# But, to describe the item, we need to tell the system that the item
# needs an id

def max_id(a_list):
    if len(a_list) == 0:
        return 0
    return sorted([i.id for i in a_list])[-1]

class Item():
    id: int | None = 0
    name: str
    price: float

    def __init__(self, name: str, price: float):
        self.id = max_id(items) + 1
        self.name = name
        self.price = price
        
    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Price: {self.price}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
        
    def from_dict(item_dict: dict[str, Union[str, float, int]]):
        item = Item(item_dict["name"], item_dict["price"])
        item.id = item_dict["id"]
        return item

items = []

def process_list(items):
    for item in items:
        print(item)

def add_item(item: Item):
    items.append(item)
    
# print(get_full_name("nizar", "ayed"))
# process(a_list_of_names)    
# process_dict(an_inventory)
# process_mixed(a_mixed_list)
# optimal_process(a_mixed_list)
add_item(Item("Product 1", 11.2))
add_item(Item("Product 2", 13.2))
add_item(Item("Product 3", 15.2))
add_item(Item("Product 4", 10.2))

new_item = Item.from_dict({
    "name": "Product 3",
    "price": 15.2
})

print(new_item)
process_list(items)
