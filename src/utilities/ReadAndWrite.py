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


def saveDictionary(inputDictionary, savingAddress):
    """
    This function pass elements of dictionary for saving to the saveData function
    :param inputDictionary: Dictionary for saving in the file
    :param savingAddress: Address of file which we want to save data
    :return: none
    """
    for elem in inputDictionary.keys():
        for i in inputDictionary[elem]:
            saveData(savingAddress, inputDictionary[elem] + '\n')


def saveSimpleDictionary(inputDictionary, savingAddress):
    for elem in inputDictionary.keys():
        saveData(savingAddress, elem + ':' + str(inputDictionary[elem]) + '\n')


def saveDictionaryWith_toPrint(inputDictionary, savingAddress):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param inputDictionary: Dictionary for saving in the file
    :param savingAddress: Address of file which we want to save data
    :return: none
    """
    for elem in inputDictionary:
        saveData(savingAddress, inputDictionary[elem].toPrint())


def saveDictionaryWith_toprintAndCSV(inputDictionary, savingAddress, csvAddress):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param inputDictionary: Dictionary for saving in the file
    :param savingAddress: Address of file which we want to save data
    :return: none
    """
    is_header = True
    for elem in inputDictionary:
        temp, csvList = inputDictionary[elem].toPrint()
        # saveData(savingAddress, temp)
        saveToCsv(csvAddress, csvList,
                  ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2',
                   'N2', 'GAP2'],
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


def saveSeqAlignmentToCSV(inputDictionary, savingAddress, csvAddress):
    """
    This function pass elements of dictionary of specific classes for saving to the saveData function
    every elem in dictionary must have toprint() function, which gives a string
    :param inputDictionary: Dictionary for saving in the file
    :param savingAddress: Address of file which we want to save data
    :return: none
    """
    is_header = True
    for elem in inputDictionary:
        temp, csvList = inputDictionary[elem].toPrint()
        saveData(savingAddress, temp)
        saveToCsv(csvAddress, csvList,
                  ['Accession_id', 'seq_alignment'], is_header)

        is_header = False
