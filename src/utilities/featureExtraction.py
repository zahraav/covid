from feature import Feature
from feature import Info
import StatisticalTest


class NucleotideCount:
    def __init__(self):
        # for Nanopore
        self.ACount_N = 0
        self.CCount_N = 0
        self.TCount_N = 0
        self.GCount_N = 0
        self.NCount_N = 0
        self.GapCount_N = 0

        # for Illumina
        self.ACount_I = 0
        self.CCount_I = 0
        self.TCount_I = 0
        self.GCount_I = 0
        self.NCount_I = 0
        self.GapCount_I = 0

        self.Apvalue = 0
        self.Cpvalue = 0
        self.Tpvalue = 0
        self.Gpvalue = 0

    def addNucleotidwith_tech(self, nucleotide, technology):
        if technology == 'Nanopore':
            if nucleotide == 'A' or nucleotide == 'W':
                self.ACount_N += 1
            elif nucleotide == 'C' or nucleotide == 'Y':
                self.CCount_N += 1
            elif nucleotide == 'T':
                self.TCount_N += 1
            elif nucleotide == 'G' or nucleotide == 'S':
                self.GCount_N += 1
            elif nucleotide == 'N':
                self.NCount_N += 1
            elif nucleotide == '-':
                self.GapCount_N += 1
        elif technology == 'Illumina':
            if nucleotide == 'A' or nucleotide == 'W':
                self.ACount_I += 1
            elif nucleotide == 'C' or nucleotide == 'Y':
                self.CCount_I += 1
            elif nucleotide == 'T':
                self.TCount_I += 1
            elif nucleotide == 'G' or nucleotide == 'S':
                self.GCount_I += 1
            elif nucleotide == 'N':
                self.NCount_I += 1
            elif nucleotide == '-':
                self.GapCount_I += 1
        else:
            print('unkown character: ' + nucleotide)

    def fisher(self):
        not_A_illumina = self.CCount_I + self.TCount_I + self.GCount_I + self.NCount_I + self.GapCount_I
        not_A_nanopore = self.CCount_N + self.TCount_N + self.GCount_N + self.NCount_N + self.GapCount_N

        not_C_illumina = self.ACount_I + self.TCount_I + self.GCount_I + self.NCount_I + self.GapCount_I
        not_C_nanopore = self.ACount_N + self.TCount_N + self.GCount_N + self.NCount_N + self.GapCount_N

        not_T_illumina = self.ACount_I + self.CCount_I + self.GCount_I + self.NCount_I + self.GapCount_I
        not_T_nanopore = self.ACount_N + self.CCount_N + self.GCount_N + self.NCount_N + self.GapCount_N

        not_G_illumina = self.ACount_I + self.CCount_I + self.TCount_I + self.NCount_I + self.GapCount_I
        not_G_nanopore = self.ACount_N + self.CCount_N + self.TCount_N + self.NCount_N + self.GapCount_N

        self.Apvalue = StatisticalTest.FisherExactTest(self.ACount_N, self.ACount_I, not_A_nanopore, not_A_illumina)
        self.Cpvalue = StatisticalTest.FisherExactTest(self.CCount_N, self.CCount_I, not_C_nanopore, not_C_illumina)
        self.Gpvalue = StatisticalTest.FisherExactTest(self.GCount_N, self.GCount_I, not_G_nanopore, not_G_illumina)
        self.Tpvalue = StatisticalTest.FisherExactTest(self.TCount_N, self.TCount_I, not_T_nanopore, not_T_illumina)

    def toprint(self):
        self.fisher()
        return 'Nanopore count: A: ' + str(self.ACount_N) + ' C: ' + str(self.CCount_N) + ' T: ' + str(
            self.TCount_N) + ' G: ' + str(
            self.GCount_N) + ' N: ' + str(self.NCount_N) + ' Gap: ' + str(self.GapCount_N) + '  ' + \
               ' |illumina count A: ' + str(self.ACount_I) + ' C: ' + str(self.CCount_I) + ' T: ' + str(
            self.TCount_I) + ' G: ' + str(
            self.GCount_I) + ' N: ' + str(self.NCount_I) + ' Gap: ' + str(self.GapCount_I) + ' |pvalue  ' \
               + str(self.Apvalue) + '  ' + str(self.Cpvalue) + '  ' + str(self.Gpvalue) + '  ' + str(self.Tpvalue)+ '\n'


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


def countNucleotides(line, tech):
    for i in range(2, len(line) - 2):
        #        print(i,line[i])
        #        nucleotidesDictionary[i] =NucleotideCount()
        nucleotidesDictionary[i].addNucleotidwith_tech(line[i], tech)


def readDate(fasta_address):
    """ This function reads modified Fasta file
    input:    fastaAddress address of fasta file
    output:   return data on the file line by line """
    dictionary_counter = 0
    is_first_time_to_make_nucleotides_dictionary = True
    fastafile_line_counter = 0
    nucleotide_within_every_line_counter = 0

    with open(fasta_address) as infile:
        for rline in infile:
            line = rline.strip()
            if '>' in line:
                infoDictionary[fastafile_line_counter] = Info(line)
            else:
                """ the first time  we see a line of sequence, we make a dictionary of [index of nucleotide, NucleotideCount()]
                with length len(line) -4 ( start from 2 , end at line -2 )  
                """
                if is_first_time_to_make_nucleotides_dictionary:
                    for i in range(2, len(line) - 2):
                        nucleotidesDictionary[i] = NucleotideCount()
                    is_first_time_to_make_nucleotides_dictionary = False

                countNucleotides(line, infoDictionary[fastafile_line_counter].technology)
                nucleotide_within_every_line_counter = setcontext(line, nucleotide_within_every_line_counter,
                                                                  fastafile_line_counter)
                fastafile_line_counter += 1

    save_dict(infoDictionary, nucleotide_dict_address)
    save_dict(featuresDictionary, feature_dict_address)
    save_dict(nucleotidesDictionary, nucleotid_count_dict_address)

    save_pvalue_address = 'files/Canada_Pvalues.txt'

    signifcant_p_valuesA = [nucleotidesDictionary[v].Apvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Apvalue < 0.01]
    saveData(save_pvalue_address,
             '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesA) / len(nucleotidesDictionary))),
                                    str(len(signifcant_p_valuesA)), str(len(nucleotidesDictionary)) ))

    signifcant_p_valuesC = [nucleotidesDictionary[v].Cpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Cpvalue < 0.01]
    saveData(save_pvalue_address,
             '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesC) / len(nucleotidesDictionary))),
                                    str(len(signifcant_p_valuesC)), str(len(nucleotidesDictionary))))

    signifcant_p_valuesG = [nucleotidesDictionary[v].Gpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Gpvalue < 0.01]
    saveData(save_pvalue_address,
             '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesG) / len(nucleotidesDictionary))),
                                    str(len(signifcant_p_valuesG)), str(len(nucleotidesDictionary))))

    signifcant_p_valuesT = [nucleotidesDictionary[v].Tpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Tpvalue < 0.01]
    saveData(save_pvalue_address,
             '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesT) / len(nucleotidesDictionary))),
                                    str(len(signifcant_p_valuesT)), str(len(nucleotidesDictionary))))

readDate('files/aligned_canada_gisaid_hcov-19_2020_09_24_21.fasta')
