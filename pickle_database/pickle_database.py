import pickle
import os

some_data = ["a list", "containing", 5,
             "values including another list",
             ["inner", "list"]]

with open("pickled_list", 'wb') as file:
    # picle.dump writes some_data in bytes format to file
    pickle.dump(some_data, file)
with open("pickled_list", 'rb') as file:
    # pickle.load load the data stored in file
    loaded_data = pickle.load(file)
    
print('Loaded data type: {}'.format(type(loaded_data)))
print('Loaded data: {}'.format(loaded_data))

# Raise an exception if the content of the two objects is not the same
assert loaded_data == some_data