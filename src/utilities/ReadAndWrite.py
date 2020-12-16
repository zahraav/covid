import csv


def saveData(saving_address, data):
    """
    This function write the data in the output_address file
    :param saving_address: Address of file which we want to save data
    :param data: data for saving in the file , String
    :return: none
    """
    with open(saving_address, "a") as output_handle:
        output_handle.write(data)


def saveDictionary(input_dictionary, saving_address):
    """
    This function pass elements of dictionary for saving to the saveData function
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    for elem in input_dictionary.keys:
        for i in input_dictionary[elem]:
            saveData(saving_address, input_dictionary[elem] + '\n')


def saveDictionaryWith_toPrint(input_dictionary, saving_address):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    for elem in input_dictionary:
        saveData(saving_address, input_dictionary[elem].toPrint())


def saveDictionaryWith_toprintAndCSV(input_dictionary, saving_address,csv_adress):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    is_header = True
    for elem in input_dictionary:
        temp, csvlist = input_dictionary[elem].toPrint()
        saveData(saving_address, temp)
        saveToCsv(csv_adress, csvlist,
                  ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2'], is_header)

        is_header = False


def saveToCsv(file_name, csvlist, fieldnames, is_header):
    x = {}
    for name, elem in zip(fieldnames, csvlist):
        x[name] = str(elem)

    with open(file_name, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if is_header:
            writer.writeheader()
        writer.writerow(x)
