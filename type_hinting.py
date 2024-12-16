# Type hinting in Python 3.10+
# if your python is < 3.10 then uncomment the following
# from typing import str

from typing import List


def get_full_name(firstname: str, lastname: str):
    return firstname.title() + " " + lastname.upper()

print(get_full_name("nizar", "ayed"))

# Hinting lists
a_list_of_names = ["nizar", "slah", "ayed"]

def process(a_list: List[str]):
    for name in a_list:
        print(name.title())
        
process(a_list_of_names)