from feature import Feature
from feature import Info

featuresDictionary = {}
infoDictionary={}
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
        dictionary_counter += 1
        i += 1
    return dictionary_counter


def saveData(output_address, data):
    """ This function write the data in the output_address file"""
    with open(output_address, "a") as output_handle:
        output_handle.write(data)


def savedict(in_dictionary):
    """This fuction pass elements of dictionary for saving to the saveData function"""
    for elem in in_dictionary:
        saveData(dictionary_address, in_dictionary[elem]._print())


def readDate(fasta_address):
    """ This function reads modified Fasta file
    input:    fastaAddress address of fasta file
    output:   return data on the file line by line """
    # setcontext('salamassdfcsw12')
    dictionary_counter = 0
    with open(fasta_address) as infile:
        for line in infile:
            # TODO Save info for every groups
            if '>' in line:
                i=Info(line)
                infoDictionary[dictionary_counter]=i

                print(i._print())
                #saveData(dictionary_address, line)
                #savedict(infoDictionary)
            else:
                dictionary_counter = setcontext(line, dictionary_counter)

    savedict(featuresDictionary)

readDate('files/test.fasta')
