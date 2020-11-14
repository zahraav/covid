from feature import Feature

featuresDictionary = {}
dictionary_address = 'files/featuresDict'


def setcontext(seq, dictionary_counter):
    """ This function set Feature in a dictionary and set context and group for the given sequence
    input: fasta sequence
    output: -
    """
    i = 2
    while i < len(seq) - 2:
        f = Feature(seq[i], 0, seq[i - 2:i + 3:1], i + 1, "info")
        featuresDictionary[dictionary_counter] = f
        dictionary_counter+=1
        i += 1
    return dictionary_counter


def saveData(output_address, data):
    """ This function write the data in the output_address file"""
    with open(output_address, "a") as output_handle:
        print(data)
        output_handle.write(data)


def savedict():
    """This fuction pass elements of dictionary for saving to the saveData function"""
    for elem in featuresDictionary:
        saveData(dictionary_address, featuresDictionary[elem].print_features())


def readDate(fasta_address):
    featuresDictionary.clear()
    """ This function reads modified Fasta file
    input:    fastaAddress address of fasta file
    output:   return data on the file line by line """
    # setcontext('salamassdfcsw12')
    dictionary_counter = 0
    with open(fasta_address) as infile:
        for line in infile:
            # TODO Save info for every groups
            if '>' in line:
                saveData(dictionary_address, line)
            else:
                dictionary_counter = setcontext(line, dictionary_counter)

    savedict()


readDate('files/test.fasta')
