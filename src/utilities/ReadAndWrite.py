def save_data(saving_address, data):
    """
    This function write the data in the output_address file
    :param saving_address: Address of file which we want to save data
    :param data: data for saving in the file , String
    :return: none
    """
    with open(saving_address, "a") as output_handle:
        output_handle.write(data)


def save_dict(input_dictionary, saving_address):
    """
    This function pass elements of dictionary for saving to the saveData function
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    print(len(input_dictionary))
    for elem in input_dictionary.keys:
        #print('-->', input_dictionary[elem])
        for i in input_dictionary[elem]:
            print('i: ', i )
            save_data(saving_address, input_dictionary[elem]+'\n')


def save_dict_with_toprint(input_dictionary, saving_address):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    for elem in input_dictionary:
        save_data(saving_address, input_dictionary[elem].to_print())
