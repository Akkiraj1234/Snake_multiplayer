original_dict = {"name": "Alice", "details": {"age": 25, "city": "New York", "something":{"name":"ayushi"}}}
shallow_copy = dict(original_dict)

# Modifying the nested dictionary in the deep copy
shallow_copy["details"]["age"] = 26
shallow_copy["name"] = "marco"
shallow_copy["details"]["something"]["name"] = "shivani"


print(original_dict)  # Output: {'name': 'Alice', 'details': {'age': 26, 'city': 'New York'}}
print(shallow_copy)   # Output: {'name': 'Alice', 'details': {'age': 26, 'city': 'New York'}}



def deep_copy(original:dict|list|tuple|set):
    # Create an empty dictionary to hold the copy
    copied_dict = {}
    
    # Iterate through each key-value pair in the original dictionary
    for key, value in original.items():
        # If the value is a dictionary, recursively copy it
        if isinstance(value, dict):
            copied_dict[key] = deep_copy(value)
        # If the value is a list, make a copy of the list and check for nested dictionaries
        elif isinstance(value, list):
            copied_list = []
            for item in value:
                if isinstance(item, dict):
                    copied_list.append(deep_copy(item))
                else:
                    copied_list.append(item)
            copied_dict[key] = copied_list
        # If the value is a set, make a copy of the set and check for nested dictionaries
        elif isinstance(value, set):
            copied_set = set()
            for item in value:
                if isinstance(item, dict):
                    copied_set.add(frozenset(deep_copy(item).items()))
                else:
                    copied_set.add(item)
            copied_dict[key] = copied_set
        # For all other data types, simply copy the value
        else:
            copied_dict[key] = value
    
    return copied_dict

original_dict = {"name": "Alice", "details": {"age": 25, "city": "New York", "something":{"name":"ayushi"}}}
shallow_copy = deep_copy(original_dict)

# Modifying the nested dictionary in the deep copy
shallow_copy["details"]["age"] = 26
shallow_copy["name"] = "marco"
shallow_copy["details"]["something"]["name"] = "shivani"

print(original_dict)  # Output: {'name': 'Alice', 'details': {'age': 25, 'city': 'New York'}}
print(shallow_copy)      # Output: {'name': 'Alice', 'details': {'age': 26, 'city': 'New York'}}

