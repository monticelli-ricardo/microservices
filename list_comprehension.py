# List comprehension

a_list = [1, 2, 3]

def double_it(a_list):
    return [operation_on(item) for item in a_list]

def operation_on(item) :
    return item * 2

print("this is the list:", a_list)
print("this is the double of the list:", double_it(a_list))

# Dict comprehension

def double_it_with_keys(a_list):
    """Create a dict where keys are
    items from a_list and values
    are the double of those items

    Args:
        a_list (list[int]): a list of items (numbers)
    """
    return { item: operation_on(item) for item in a_list}

print("the double in form of dict:", double_it_with_keys(a_list))
    
def double_range(lowest, highest):
    #return double_it_with_keys(range(lowest, highest))
    a_list = range(lowest, highest)
    return { key: value for (key, value) in zip(
        a_list,
        double_it(a_list)
        )}

print("the double of the range between 5 and 15 is",
      double_range(5, 15))
# {
#   5:10,
#   6:12,
#   7:14,
#   ...
#   14:28       
# }
