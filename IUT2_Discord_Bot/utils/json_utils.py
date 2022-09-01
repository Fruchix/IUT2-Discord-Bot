import json


def append_element_json_array(new_data, array, filename):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside data
        file_data[str(array)].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def remove_element_json_array(index_remove, array, filename):
    # load original json file
    with open(filename, 'r') as file:
        file_data = json.load(file)

        # remove element at index "index_remove" from the json array "array"
        file_data[str(array)].pop(index_remove)

    # rewrite the entire file without the element
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent=4)