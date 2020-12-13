import math

from feature import Feature
from feature import Info
import StatisticalTest
import ReadAndWrite


class nucleotide:
    def __init__(self):
        self.count_of_nucleotid_in_illumina = 0
        self.count_of_nucleotid_in_nanopore = 0
        self.p_value = 0

    def count_sum(self):
        return self.count_of_nucleotid_in_illumina + self.count_of_nucleotid_in_nanopore

    def add_counter(self, tech):
        """
        Every time this function is called the counter of the nucleotide is increase by 1
        :param tech:
        :return:
        """
        if tech == 'Nanopore':
            self.count_of_nucleotid_in_nanopore += 1
        else:
            self.count_of_nucleotid_in_illumina += 1


class NucleotidesCount:
    def __init__(self):
        self.A = nucleotide()
        self.C = nucleotide()
        self.G = nucleotide()
        self.T = nucleotide()
        self.N = nucleotide()
        self.Gap = nucleotide()

    def sumIllumina(self):
        return self.A.count_of_nucleotid_in_illumina + self.C.count_of_nucleotid_in_illumina + \
               self.G.count_of_nucleotid_in_illumina + self.T.count_of_nucleotid_in_illumina + \
               self.N.count_of_nucleotid_in_illumina + self.Gap.count_of_nucleotid_in_illumina

    def sumNanopore(self):
        return self.A.count_of_nucleotid_in_nanopore + self.C.count_of_nucleotid_in_nanopore + \
               self.G.count_of_nucleotid_in_nanopore + self.T.count_of_nucleotid_in_nanopore + \
               self.N.count_of_nucleotid_in_nanopore + self.Gap.count_of_nucleotid_in_nanopore

    def sum(self):
        return self.sumIllumina() + self.sumNanopore()

    def add_nucleotide(self, nucleotide, technology):
        """
        Every time this function is called the counter of the nucleotide is increase by 1
        :param nucleotide:
        :param technology:
        :return:
        """
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
        """
        This function calculate sum of nucleotides other than the nucleotide that recieved as input, and return the sum for using in
        Fisher exact test
        :param nucleotide_count_nanopore: nucleotide in sequences that the technology was Nanopore
        :param nucleotide_count_illumina:  nucleotide in sequences that the technology was Illumina
        :return: 2 output, sum of Nucleotides that technology were nanopore and Illumina
        """
        illumina_sum = self.A.count_of_nucleotid_in_illumina + self.C.count_of_nucleotid_in_illumina + self.T.count_of_nucleotid_in_illumina + \
                       self.G.count_of_nucleotid_in_illumina + self.N.count_of_nucleotid_in_illumina + \
                       self.Gap.count_of_nucleotid_in_illumina - nucleotide_count_illumina
        nanopore_sum = self.A.count_of_nucleotid_in_nanopore + self.C.count_of_nucleotid_in_nanopore + self.T.count_of_nucleotid_in_nanopore + \
                       self.G.count_of_nucleotid_in_nanopore + self.N.count_of_nucleotid_in_nanopore + \
                       self.Gap.count_of_nucleotid_in_nanopore - nucleotide_count_nanopore
        return nanopore_sum, illumina_sum

    def calculate_list_elements(self, ni, nSum):
        # if (ni<10 or nSum < 10):
        print('ni:  ', ni, ' nsum:  ', nSum , ' return: ')
        if ni == 0:
            print('ni:  ', ni, ' nsum:  ', nSum, ' return: ', 0 )
            return 0
        result=(ni / nSum) * math.log10(ni / nSum)
        print('ni:  ', ni, ' nsum:  ', nSum, ' return: ',result)
        return result

    def likelihoodRatioTest(self, savingfilename):
        # L1 is for nanopore:
        L1 = self.calculate_list_elements(self.A.count_of_nucleotid_in_nanopore, self.sumNanopore()) + \
             self.calculate_list_elements(self.C.count_of_nucleotid_in_nanopore, self.sumNanopore()) + \
             self.calculate_list_elements(self.G.count_of_nucleotid_in_nanopore, self.sumNanopore()) + \
             self.calculate_list_elements(self.T.count_of_nucleotid_in_nanopore, self.sumNanopore()) + \
             self.calculate_list_elements(self.N.count_of_nucleotid_in_nanopore, self.sumNanopore()) + \
             self.calculate_list_elements(self.Gap.count_of_nucleotid_in_nanopore, self.sumNanopore())

        L2 = self.calculate_list_elements(self.A.count_of_nucleotid_in_illumina, self.sumIllumina()) + \
             self.calculate_list_elements(self.C.count_of_nucleotid_in_illumina, self.sumIllumina()) + \
             self.calculate_list_elements(self.G.count_of_nucleotid_in_illumina, self.sumIllumina()) + \
             self.calculate_list_elements(self.T.count_of_nucleotid_in_illumina, self.sumIllumina()) + \
             self.calculate_list_elements(self.N.count_of_nucleotid_in_illumina, self.sumIllumina()) + \
             self.calculate_list_elements(self.Gap.count_of_nucleotid_in_illumina, self.sumIllumina())

        L_joint = self.calculate_list_elements(
            (self.A.count_of_nucleotid_in_nanopore + self.A.count_of_nucleotid_in_illumina),
            self.sum()) + \
                  self.calculate_list_elements(
                      (self.C.count_of_nucleotid_in_nanopore + self.C.count_of_nucleotid_in_illumina),
                      self.sum()) + \
                  self.calculate_list_elements(
                      (self.G.count_of_nucleotid_in_nanopore + self.G.count_of_nucleotid_in_illumina),
                      self.sum()) + \
                  self.calculate_list_elements(
                      (self.T.count_of_nucleotid_in_nanopore + self.T.count_of_nucleotid_in_illumina),
                      self.sum()) + \
                  self.calculate_list_elements(
                      (self.N.count_of_nucleotid_in_nanopore + self.N.count_of_nucleotid_in_illumina),
                      self.sum()) + \
                  self.calculate_list_elements(
                      (self.Gap.count_of_nucleotid_in_nanopore + self.Gap.count_of_nucleotid_in_illumina),
                      self.sum())
        print ('N1: ',self.sumNanopore(),'L1 : ',L1 ,'N2: ',self.sumIllumina(),' L2: ', L2 ,' L_joint: ', L_joint)
        # firstListCount, L1, secondListCount, L2, L_joint):
        StatisticalTest.LikelihoodRatioTest(self.sumNanopore(), L1, self.sumIllumina(), L2, L_joint, savingfilename)

    def fisher(self, p_value_file_name):
        """
        This function calculating data for table of Fisher's exact test. Then pass them for calculating Fisher's exact test to StatisticalTest
        class and save them as p_value
        :return: none
        """
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
                                                         not_A_illumina, p_value_file_name)
        self.C.p_value = StatisticalTest.FisherExactTest(self.C.count_of_nucleotid_in_nanopore,
                                                         self.C.count_of_nucleotid_in_illumina, not_C_nanopore,
                                                         not_C_illumina, p_value_file_name)
        self.G.p_value = StatisticalTest.FisherExactTest(self.G.count_of_nucleotid_in_nanopore,
                                                         self.G.count_of_nucleotid_in_illumina, not_G_nanopore,
                                                         not_G_illumina, p_value_file_name)
        self.T.p_value = StatisticalTest.FisherExactTest(self.T.count_of_nucleotid_in_nanopore,
                                                         self.T.count_of_nucleotid_in_illumina, not_T_nanopore,
                                                         not_T_illumina, p_value_file_name)

    def to_print(self):
        """
        This function generates a String that contains every element that we want to print in a file
        :return: a string
        """
        return 'Nanopore- A:' + str(self.A.count_of_nucleotid_in_nanopore) + '|C:' + str(
            self.C.count_of_nucleotid_in_nanopore) + '|G:' + str(self.G.count_of_nucleotid_in_nanopore) + '|T:' + str(
            self.T.count_of_nucleotid_in_nanopore) + '|N:' + str(self.N.count_of_nucleotid_in_nanopore) + '|Gap:' + str(
            self.Gap.count_of_nucleotid_in_nanopore) + ' --|illumina- A:' + str(
            self.A.count_of_nucleotid_in_illumina) + '|C:' + str(self.C.count_of_nucleotid_in_illumina) + '|G:' + str(
            self.G.count_of_nucleotid_in_illumina) + '|T:' + str(self.T.count_of_nucleotid_in_illumina) + '|N:' + str(
            self.N.count_of_nucleotid_in_illumina) + '|Gap:' + str(
            self.Gap.count_of_nucleotid_in_illumina) + ' --|pvalue: A: ' + str(self.A.p_value) + '  |C: ' + str(
            self.C.p_value) + ' |G: ' + str(self.G.p_value) + ' |T: ' + str(self.T.p_value) + '\n'


def setcontext(featuresDictionary, seq, dictionary_counter, line_counter, ):
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
        nucleotidesDictionary[i].add_nucleotide(line[i], tech)


def process_fasta_file(fasta_address, bp_number):
    """This function reads modified Fasta file and count number of nucleotides for every vertical cuts and also calculate p-value
    :param fasta_address: address of fasta file that we want to be read and processed
    :return: none
    """
    featuresDictionary = {}
    infoDictionary = {}
    nucleotidesDictionary = {}

    nucleotide_dict_address = 'files/Canada_NucleotideDictionary_.txt'.replace('.txt', str(bp_number) + '.txt')
    nucleotide_count_dict_address = 'files/Canada_NucleotidcountDictionary_.txt'.replace('.txt',
                                                                                         str(bp_number) + '.txt')
    feature_dict_address = 'files/Canada_FeatureDictionary_.txt'.replace('.txt', str(bp_number) + '.txt')
    save_pvalue_address = 'files/sum_of_significant_p_values_.txt'.replace('.txt', str(bp_number) + '.txt')
    p_value_file_name = 'files/p_value_.txt'.replace('.txt', str(bp_number) + '.txt')
    likelihoodRatio_filename = 'files/likelihood.txt'.replace('.txt', str(bp_number) + '.txt')
    likelihood_dictionary_address = 'files/likelihooddictionary.txt'.replace('.txt', str(bp_number) + '.txt')

    dictionary_counter = 0
    is_first_time_to_make_nucleotides_dictionary = True
    fastafile_line_counter = 0

    """nucleotide_within_line_counter for context"""
    nwl_context_counter = 0

    with open(fasta_address) as infile:
        for rline in infile:
            line = rline.strip()
            if '>' in line:
                infoDictionary[fastafile_line_counter] = Info(line)
            else:
                """ the first time  we see a line of sequence, we make a dictionary of [index of nucleotide, NucleotidesCount()]
                with length len(line) -4 ( start from 2 , end at line -2 )  
                """
                if is_first_time_to_make_nucleotides_dictionary:
                    for i in range(2, len(line) - 2):
                        nucleotidesDictionary[i] = NucleotidesCount()
                    is_first_time_to_make_nucleotides_dictionary = False

                countNucleotides(nucleotidesDictionary, line, infoDictionary[fastafile_line_counter].technology)
                nwl_context_counter = setcontext(featuresDictionary, line, nwl_context_counter, fastafile_line_counter)

                fastafile_line_counter += 1
    likelihoodDictionary = {}
    i = 0
    for elem in nucleotidesDictionary:
        likelihoodDictionary[i] = nucleotidesDictionary[elem].likelihoodRatioTest(likelihoodRatio_filename)
        i += 1

    """save data for all dictionaries in file """
    ReadAndWrite.save_dict_with_toprint(infoDictionary, nucleotide_dict_address)
    ReadAndWrite.save_dict_with_toprint(featuresDictionary, feature_dict_address)
    ReadAndWrite.save_dict_with_toprint(nucleotidesDictionary, nucleotide_count_dict_address)
    #ReadAndWrite.save_dict(likelihoodDictionary, likelihood_dictionary_address)

    """
    calculate the percentage of p_value and significancy and save it in the file
    """
    '''
    significance_level=0.01
    significant_p_valuesA = [nucleotidesDictionary[v].A.p_value for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].A.p_value < significance_level]
    ReadAndWrite.save_data(save_pvalue_address,
                           'A: percentage: {0}  A_count: {1}  total: {2} \n'.format(str(str(len(significant_p_valuesA) / len(nucleotidesDictionary))),
                                                     str(len(significant_p_valuesA)), str(len(nucleotidesDictionary))))

    significant_p_valuesC = [nucleotidesDictionary[v].C.p_value for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].C.p_value < significance_level]
    ReadAndWrite.save_data(save_pvalue_address,
                           'C: percentage: {0}  C_count: {1}  total: {2} \n'.format(str(str(len(significant_p_valuesC) / len(nucleotidesDictionary))),
                                                     str(len(significant_p_valuesC)), str(len(nucleotidesDictionary))))

    significant_p_valuesG = [nucleotidesDictionary[v].G.p_value for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].G.p_value < significance_level]
    ReadAndWrite.save_data(save_pvalue_address,
                           'G: percentage: {0}  G_count: {1}  total: {2} \n'.format(str(str(len(significant_p_valuesG) / len(nucleotidesDictionary))),
                                                     str(len(significant_p_valuesG)), str(len(nucleotidesDictionary))))

    significant_p_valuesT = [nucleotidesDictionary[v].T.p_value for v in nucleotidesDictionary if
                            nucleotidesDictionary[v].T.p_value < significance_level]
    ReadAndWrite.save_data(save_pvalue_address,
                           'T: percentage: {0}  T_count: {1}  total: {2} \n'.format(str(str(len(significant_p_valuesT) / len(nucleotidesDictionary))),
                                                     str(len(significant_p_valuesT)), str(len(nucleotidesDictionary))))
'''


process_fasta_file('files/aligned_canada_gisaid_hcov-19_2020_09_24_21_2.fasta', 1)
