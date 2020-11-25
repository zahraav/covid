from feature import Feature
from feature import Info
import scipy.stats as stats

class NucleotideCount:
    def __init__(self):
        self.ACount = 0
        self.CCount = 0
        self.TCount = 0
        self.GCount = 0
        self.NCount = 0
        self.GapCount = 0

        self.Apvalue = 0
        self.Cpvalue = 0
        self.Tpvalue = 0
        self.Gpvalue = 0

    def addNucleotide(self, nucleotide):
        """ Increase the count of the Nucleotide if that nucleotide """
        if nucleotide == 'A' or nucleotide == 'W':
            self.ACount += 1
        elif nucleotide == 'C' or nucleotide == 'Y':
            self.CCount += 1
        elif nucleotide == 'T':
            self.TCount += 1
        elif nucleotide == 'G' or nucleotide == 'S':
            self.GCount += 1
        elif nucleotide == 'N':
            self.NCount += 1
        elif nucleotide == '-':
            self.GapCount += 1
        else:
            print('unkown character: ' + nucleotide)

    def do_fisher_test(self):
        """ [nucleotide count,others count],[Illumina_nucleotid, Nanopore_nucleotid]"""
        oddsratio, pvalue = stats.fisher_exact([[8, 2], [1, 5]])
        print(pvalue)
        return pvalue


    def toprint(self):
        return ' A: ' + str(self.ACount) + ' C: ' + str(self.CCount) + ' T: ' + str(self.TCount) + ' G: ' + str(
            self.GCount) + ' N: ' + str(self.NCount) + ' Gap: ' + str(self.GapCount) + '  ' +\
               str(self.ACount + self.CCount + self.TCount + self.GCount + self.NCount + self.GapCount) + '  '+ str(self.do_fisher_test())+'\n'


featuresDictionary = {}
infoDictionary = {}
nucleotidesDictionary = {}

nucleotide_dict_address = 'files/Canada_NucleotideDictionary.txt'
nucleotid_count_dict_address = 'files/Canada_NucleotidcountDictionary.txt'
feature_dict_address = 'files/Canada_FeatureDictionary.txt'


def setcontext(seq, dictionary_counter, line_counter):
    """ This function set Feature in a dictionary and set context and group for the given sequence
    input: fasta sequence
    output: -
    """
    i = 2
    while i < len(seq) - 3:
        f = Feature(seq[i], 0, seq[i - 2:i + 3: 1], i + 1, "info", line_counter)
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
    for i in range(2, len(line) - 2):
        #        print(i,line[i])
        #        nucleotidesDictionary[i] =NucleotideCount()
        nucleotidesDictionary[i].addNucleotide(line[i])


def readDate(fasta_address):
    """ This function reads modified Fasta file
    input:    fastaAddress address of fasta file
    output:   return data on the file line by line """
    dictionary_counter = 0
    is_first_time_to_make_nucleotides_dictionary = True
    line_counter = 0
    with open(fasta_address) as infile:
        for rline in infile:
            line = rline.strip()
            if '>' in line:
                i = Info(line)
                infoDictionary[dictionary_counter] = i
            else:
                """ the first time  we see a line of sequence, we make a dictionary of [index of nucleotide, NucleotideCount()]
                with length len(line) -4 ( start from 2 , end at line -2 )  
                """
                if is_first_time_to_make_nucleotides_dictionary:
                    for i in range(2, len(line) - 2):
                        nucleotidesDictionary[i] = NucleotideCount()
                    is_first_time_to_make_nucleotides_dictionary = False

                countNucleotides(line)
                dictionary_counter = setcontext(line, dictionary_counter, line_counter)
                line_counter += 1
                if (line_counter == 1880):
                    break

    save_dict(infoDictionary, nucleotide_dict_address)
    save_dict(featuresDictionary, feature_dict_address)
    save_dict(nucleotidesDictionary, nucleotid_count_dict_address)


readDate('files/aligned_canada_gisaid_hcov-19_2020_09_24_21.fasta')
