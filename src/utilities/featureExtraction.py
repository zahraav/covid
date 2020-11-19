from feature import Feature
from feature import Info


class NucleotideCount:
    def __init__(self):
        self.ACount = 0
        self.CCount = 0
        self.TCount = 0
        self.GCount = 0
        self.NCount = 0
        self.GapCount = 0

    def addNucleotide(self, nucleotide):
        """ Increase the count of the Nucleotide if that nucleotide """
        if nucleotide == 'A':
            self.ACount += 1
        if nucleotide == 'C':
            self.CCount += 1
        if nucleotide == 'T':
            self.TCount += 1
        if nucleotide == 'G':
            self.GCount += 1
        if nucleotide == 'N':
            self.NCount += 1
        if nucleotide == '-':
            self.GapCount += 1

    def toprint(self):
        return ' A: ' + str(self.ACount) + ' C: ' + str(self.CCount) + ' T: ' + str(self.TCount) + ' G: ' + str(
            self.GCount) + \
               ' N: ' + str(self.NCount) + ' Gap: ' + str(self.GapCount) + '\n'


featuresDictionary = {}
infoDictionary = {}
nucleotidesDictionary = {}

nucleotide_dict_address = 'files/NucleotideDictionary1.txt'
nucleotid_count_dict_address = 'files/NucleotidcountDictionary1.txt'
feature_dict_address = 'files/FeatureDictionary1.txt'


def setcontext(seq, dictionary_counter,line_counter):
    """ This function set Feature in a dictionary and set context and group for the given sequence
    input: fasta sequence
    output: -
    """
    i = 2
    while i < len(seq) - 3:
        f = Feature(seq[i], 0, seq[i - 2:i + 3: 1], i + 1, "info",line_counter)
        featuresDictionary[dictionary_counter] = f
        dictionary_counter += 1
        i += 1
    return dictionary_counter


def saveData(output_address, data):
    """ This function write the data in the output_address file"""
    with open(output_address, "a") as output_handle:
        output_handle.write(data)


def save_dict(input_dictionary, in_address):
    """This function pass elements of dictionary for saving to the saveData function"""
    for elem in input_dictionary:
        saveData(in_address, input_dictionary[elem].toprint())


def countNucleotides(line):
    #   print(len(line))
    for i in range(2, len(line) - 2):
        #        print(i,line[i])
        #        nucleotidesDictionary[i] =NucleotideCount()
        nucleotidesDictionary[i].addNucleotide(line[i])


def readDate(fasta_address):
    """ This function reads modified Fasta file
    input:    fastaAddress address of fasta file
    output:   return data on the file line by line """
    dictionary_counter = 0
    is_array = True
    line_counter=0
    with open(fasta_address) as infile:
        for line in infile:
            if '>' in line:
                i = Info(line)
                infoDictionary[dictionary_counter] = i
                #saveData(feature_dict_address, line)
            else:
                if is_array:
                    for i in range(2, len(line) - 2):
                        nucleotidesDictionary[i] = NucleotideCount()
                    is_array = False

                countNucleotides(line)
                dictionary_counter = setcontext(line, dictionary_counter,line_counter)
                line_counter+=1

    save_dict(infoDictionary, nucleotide_dict_address)
    save_dict(featuresDictionary, feature_dict_address)
    save_dict(nucleotidesDictionary, nucleotid_count_dict_address)

readDate('files/test.fasta')
