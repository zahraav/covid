def save_data(output_address, data):
    """ This function write the data in the output_address file"""
    with open(output_address, "a") as output_handle:
        output_handle.write(data)


def save_dict(input_dictionary, input_address):
    """This function pass elements of dictionary for saving to the saveData function"""
    for elem in input_dictionary:
        save_data(input_address, input_dictionary[elem])


def save_dict_with_toprint(input_dictionary, in_address):
    """This function pass elements of dictionary for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string"""
    for elem in input_dictionary:
        save_data(in_address, input_dictionary[elem].to_print())
