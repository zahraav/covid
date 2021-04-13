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


def saveDictionaryWith_toprintAndCSV(input_dictionary, saving_address,csvAddress):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param input_dictionary: Dictionary for saving in the file
    :param saving_address: Address of file which we want to save data
    :return: none
    """
    is_header = True
    for elem in input_dictionary:
        temp, csvList = input_dictionary[elem].toPrint()
        #saveData(saving_address, temp)
        saveToCsv(csvAddress, csvList,
                  ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2'],
                  is_header)

        is_header = False


def saveToCsv(fileName, csvList, fieldNames, isHeader):
    # is_header should set to true for the first time then it should set to false for rest of calls
    # this print the header in CSV file.
    # if it doesn't set to false it will print the header for every line.
    x = {}
    for name, elem in zip(fieldNames, csvList):
        x[name] = str(elem)
    with open(fileName, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isHeader:
            writer.writeheader()
        writer.writerow(x)


def saveSeqAlignmentToCSV(input_dictionary, saving_address,csvAddress):
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
        saveToCsv(csvAddress, csvlist,
                  ['Accession_id', 'seq_alignment'],is_header)

        is_header = False
