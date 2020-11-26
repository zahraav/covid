from feature import Feature
from feature import Info
import StatisticalTest
import ReadAndWrite


class ncount:
    def __init__(self):
        self.count_of_nucleotid_in_illumina = 0
        self.count_of_nucleotid_in_nanopore = 0
        self.p_value = 0

    def count_sum(self):
        return self.count_of_nucleotid_in_illumina + self.count_of_nucleotid_in_nanopore

    def add_counter(self, tech):
        if tech == 'Nanopore':
            self.count_of_nucleotid_in_nanopore += 1
        else:
            self.count_of_nucleotid_in_illumina += 1


class NucleotideCount:
    def __init__(self):
        self.A = ncount()
        self.C = ncount()
        self.G = ncount()
        self.T = ncount()
        self.N = ncount()
        self.Gap = ncount()

    def add_nucleotid(self, nucleotide, technology):
        if nucleotide == 'A' or nucleotide == 'W':
            self.A.add_counter(technology)
        elif nucleotide == 'C' or nucleotide == 'Y':
            self.C.add_counter(technology)
        elif nucleotide == 'T':
            self.T.add_counter(technology)
        elif nucleotide == 'G' or nucleotide == 'S':
            self.G.add_counter(technology)
        elif nucleotide == 'N':
            self.N.add_counter(technology)
        elif nucleotide == '-':
            self.Gap.add_counter(technology)
        else:
            print('unkown character: ' + nucleotide)

    def not_nucleotide(self, nucleotide_count_nanopore, nucleotide_count_illumina):
        illumina_sum = self.A.count_of_nucleotid_in_illumina + self.C.count_of_nucleotid_in_illumina + self.T.count_of_nucleotid_in_illumina + \
                       self.G.count_of_nucleotid_in_illumina + self.N.count_of_nucleotid_in_illumina + \
                       self.Gap.count_of_nucleotid_in_illumina - nucleotide_count_illumina
        nanopore_sum = self.A.count_of_nucleotid_in_nanopore + self.C.count_of_nucleotid_in_nanopore + self.T.count_of_nucleotid_in_nanopore + \
                       self.G.count_of_nucleotid_in_nanopore + self.N.count_of_nucleotid_in_nanopore + \
                       self.Gap.count_of_nucleotid_in_nanopore - nucleotide_count_nanopore
        return nanopore_sum, illumina_sum

    def fisher(self):
        not_A_nanopore, not_A_illumina = self.not_nucleotide(self.A.count_of_nucleotid_in_nanopore,
                                                             self.A.count_of_nucleotid_in_illumina)
        not_C_nanopore, not_C_illumina = self.not_nucleotide(self.C.count_of_nucleotid_in_nanopore,
                                                             self.C.count_of_nucleotid_in_illumina)
        not_G_nanopore, not_G_illumina = self.not_nucleotide(self.G.count_of_nucleotid_in_nanopore,
                                                             self.G.count_of_nucleotid_in_illumina)
        not_T_nanopore, not_T_illumina = self.not_nucleotide(self.T.count_of_nucleotid_in_nanopore,
                                                             self.T.count_of_nucleotid_in_illumina)

        self.A.p_value = StatisticalTest.FisherExactTest(self.A.count_of_nucleotid_in_nanopore,
                                                         self.A.count_of_nucleotid_in_illumina, not_A_nanopore,
                                                         not_A_illumina)
        self.C.p_value = StatisticalTest.FisherExactTest(self.C.count_of_nucleotid_in_nanopore,
                                                         self.C.count_of_nucleotid_in_illumina, not_C_nanopore,
                                                         not_C_illumina)
        self.G.p_value = StatisticalTest.FisherExactTest(self.G.count_of_nucleotid_in_nanopore,
                                                         self.G.count_of_nucleotid_in_illumina, not_G_nanopore,
                                                         not_G_illumina)
        self.T.p_value = StatisticalTest.FisherExactTest(self.T.count_of_nucleotid_in_nanopore,
                                                         self.T.count_of_nucleotid_in_illumina, not_T_nanopore,
                                                         not_T_illumina)

    def to_print(self):
        self.fisher()
        return 'N- A:' + str(self.A.count_of_nucleotid_in_nanopore) + '|C:' + str(
            self.C.count_of_nucleotid_in_nanopore) + '|G:' + str(self.G.count_of_nucleotid_in_nanopore) + '|T:' + str(
            self.T.count_of_nucleotid_in_nanopore) + '|N:' + str(self.N.count_of_nucleotid_in_nanopore) + '|Gap:' + str(
            self.Gap.count_of_nucleotid_in_nanopore) + '--' + ' |illumina- A:' + str(
            self.A.count_of_nucleotid_in_illumina) + '|C:' + str(self.C.count_of_nucleotid_in_illumina) + '|G:' + str(
            self.G.count_of_nucleotid_in_illumina) + '|T:' + str(self.T.count_of_nucleotid_in_illumina) + '|N:' + str(
            self.N.count_of_nucleotid_in_illumina) + '|Gap:' + str(
            self.Gap.count_of_nucleotid_in_illumina) + '|pvalue: ' + str(self.A.pvalue) + '  ' + str(
            self.C.pvalue) + '  ' + str(self.G.pvalue) + '  ' + str(self.T.pvalue) + '\n'

def setcontext(featuresDictionary,seq, dictionary_counter, line_counter, ):
    """
    This function set Feature in a dictionary and set context and group for the given sequence
    :param featuresDictionary:
    :param seq:
    :param dictionary_counter:
    :param line_counter:
    :return:
    """
    i = 2
    while i < len(seq) - 3:
        featuresDictionary[dictionary_counter] = Feature(seq[i], 0, seq[i - 2:i + 3: 1], i + 1, "info", line_counter)
        dictionary_counter += 1
        i += 1
    return dictionary_counter


def countNucleotides(nucleotidesDictionary, line, tech):
    """
    :param nucleotidesDictionary: Dictionary that contains all the nucleotides and their count for every vertical index there is a NucleotideCount Class
            Which countains the count of every nucleotide in a vertical cut of sequences in fasta file
    :param line: lastest line that is read
    :param tech:technology of reading the current sequence
    :return: none
    """
    for i in range(2, len(line) - 2):
        nucleotidesDictionary[i].add_nucleotid(line[i], tech)


def process_fasta_file(fasta_address):
    """This function reads modified Fasta file and count number of nucleotides for every vertical cuts and also calculate p-value
    :param fasta_address: address of fasta file that we want to be read and processed
    :return: none
    """
    featuresDictionary = {}
    infoDictionary = {}
    nucleotidesDictionary = {}

    nucleotide_dict_address = 'files/Canada_NucleotideDictionary.txt'
    nucleotid_count_dict_address = 'files/Canada_NucleotidcountDictionary.txt'
    feature_dict_address = 'files/Canada_FeatureDictionary.txt'

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

                countNucleotides(nucleotidesDictionary, line, infoDictionary[fastafile_line_counter].technology)

                nucleotide_within_every_line_counter = setcontext(featuresDictionary, line, nucleotide_within_every_line_counter,
                                                                  fastafile_line_counter)
                fastafile_line_counter += 1

    ReadAndWrite.save_dict_with_toprint(infoDictionary, nucleotide_dict_address)
    ReadAndWrite.save_dict_with_toprint(featuresDictionary, feature_dict_address)
    ReadAndWrite.save_dict_with_toprint(nucleotidesDictionary, nucleotid_count_dict_address)

    save_pvalue_address = 'files/Canada_Pvalues.txt'

    signifcant_p_valuesA = [nucleotidesDictionary[v].Apvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Apvalue < 0.01]
    ReadAndWrite.save_data(save_pvalue_address,
                           '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesA) / len(nucleotidesDictionary))),
                                                     str(len(signifcant_p_valuesA)), str(len(nucleotidesDictionary))))

    signifcant_p_valuesC = [nucleotidesDictionary[v].Cpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Cpvalue < 0.01]
    ReadAndWrite.save_data(save_pvalue_address,
                           '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesC) / len(nucleotidesDictionary))),
                                                     str(len(signifcant_p_valuesC)), str(len(nucleotidesDictionary))))

    signifcant_p_valuesG = [nucleotidesDictionary[v].Gpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Gpvalue < 0.01]
    ReadAndWrite.save_data(save_pvalue_address,
                           '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesG) / len(nucleotidesDictionary))),
                                                     str(len(signifcant_p_valuesG)), str(len(nucleotidesDictionary))))

    signifcant_p_valuesT = [nucleotidesDictionary[v].Tpvalue for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].Tpvalue < 0.01]
    ReadAndWrite.save_data(save_pvalue_address,
                           '{0}  {1}  {2} \n'.format(str(str(len(signifcant_p_valuesT) / len(nucleotidesDictionary))),
                                                     str(len(signifcant_p_valuesT)), str(len(nucleotidesDictionary))))


process_fasta_file('files/aligned_canada_gisaid_hcov-19_2020_09_24_21.fasta')
