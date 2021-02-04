from utilities.feature import Feature
from utilities.feature import Info
from utilities import StatisticalTest
from utilities import ReadAndWrite


class Nucleotide:
    def __init__(self, name, name2=None):
        if name2 is None:
            name2 = []
        self.count = 0
        self.name = name
        self.name2 = name2

    def toPrint(self):
        return self.name + ' : ' + str(self.count), self.count


class Technology:
    def __init__(self, technologyName):
        self.A = Nucleotide('A', ['W', 'M', 'D', 'V'])
        self.C = Nucleotide('C', ['Y', 'B', 'H'])
        self.G = Nucleotide('G', ['S', 'R', 'K'])
        self.T = Nucleotide('T', ['U'])
        self.N = Nucleotide('N')
        self.Gap = Nucleotide('.', ['-'])
        self.technologyName = technologyName
        self.__sum = 0

        self.nucleotide_count_list = [self.A, self.C, self.G, self.T, self.N, self.Gap]

    def getSum(self):
        self.__sum = self.A.count + self.C.count + self.G.count + self.T.count + self.N.count + self.Gap.count
        return self.__sum

    def increaseNucleotideCount(self, nucleotide):
        """
            Every time this function is called the counter of the nucleotide is increase by 1
            :param nucleotide:
            :return:
            """

        for elem in self.nucleotide_count_list:
            if elem.name == nucleotide or nucleotide in elem.name2:
                elem.count += 1
        if nucleotide not in ['A', 'W', 'M', 'D', 'V', 'C', 'Y', 'B', 'H', 'G', 'S', 'R', 'K', 'T', 'U', 'W', 'N', '.',
                              '-']:
            print(nucleotide)

    def getL(self):
        L = 0
        for elem in self.nucleotide_count_list:
            L += StatisticalTest.calculate_list_elements(elem.count, self.getSum())
        return L

    def toPrint(self):
        printString = ' '
        csvlist = [self.getSum()]
        for elem in self.nucleotide_count_list:
            ncount, csvelem = elem.toPrint()
            printString = printString + ncount + ' '
            csvlist.append(csvelem)
        return ('sum: ' + str(self.getSum()) + ' ' + printString), csvlist


class VerticalCut:
    def __init__(self):
        self.nanopore = Technology('nanopore')
        self.illumina = Technology('illumina')
        self.vertical_cut_technology = [self.nanopore, self.illumina]
        self.__sum = 0

    def getSum(self):
        self.__sum = self.nanopore.getSum() + self.illumina.getSum()
        return self.__sum

    def add_nucleotide(self, n, technology):
        """
        :param n: nucleotide
        :param technology: Technology that is being used
        :return:
        """
        if technology.lower() == 'nanopore':
            self.nanopore.increaseNucleotideCount(n)
        elif technology.lower() == 'illumina':
            self.illumina.increaseNucleotideCount(n)

    def likelihoodRatioTest(self, filename, is_header, csv_address):
        L_joint = 0

        for nelem, ielem in zip(self.nanopore.nucleotide_count_list, self.illumina.nucleotide_count_list):
            L_joint = L_joint + StatisticalTest.calculate_list_elements(nelem.count + ielem.count, self.getSum())

        StatisticalTest.LikelihoodRatioTest(N1=self.nanopore.getSum(), L1=self.nanopore.getL(),
                                            N2=self.illumina.getSum(), L2=self.illumina.getL(), L_joint=L_joint,
                                            filename=filename, is_header=is_header, csv_address=csv_address)

    def toPrint(self):
        csvlist = []
        nelem, nanocsv = self.nanopore.toPrint()
        ielem, illucsv = self.illumina.toPrint()
        for i in nanocsv:
            csvlist.append(i)
        for j in illucsv:
            csvlist.append(j)
        return '1)Nanopore-  ' + str(nelem) + '   |2) illumina ' + str(ielem) + '\n', csvlist


def setcontext(featuresDictionary, seq, dictionary_counter, line_counter, ):
    """
    This function set Feature in a dictionary and set context and group for the given sequence
    """
    i = 2
    while i < len(seq) - 3:
        featuresDictionary[dictionary_counter] = Feature(seq[i], 0, seq[i - 2:i + 3: 1], i + 1, "info", line_counter)
        dictionary_counter += 1
        i += 1
    return dictionary_counter


def countNucleotides(nucleotidesDictionary, line, tech):
    """
    :param nucleotidesDictionary: Dictionary that contains all the nucleotides and their count for every vertical
            index there is a NucleotideCount Class Which contains the count of every nucleotide in a vertical cut
            of sequences in fasta file
    :param line: last line that is read
    :param tech:technology of reading the current sequence
    :return: none
    """
    for i in range(2, len(line) - 2):
        nucleotidesDictionary[i].add_nucleotide(line[i], tech)


def process_fasta_file(fasta_address, bp_number,prefix):
    """This function reads modified Fasta file and count number of nucleotides for every vertical cuts
    :param bp_number: it's an integer that shows the data belongs to first 100bp or second 100bp or ... of sequence
    :param fasta_address: address of fasta file that we want to be read and processed
    :return: none
    """
    featuresDictionary = {}
    infoDictionary = {}
    nucleotidesDictionary = {}
    #nucleotide_dict_address = 'files/'+prefix+'NucleotideDictionary_.txt'.replace('.txt', bp_number + '.txt')
    #nucleotide_count_dict_address = 'files/'+prefix+'NucleotidcountDictionary_.txt'.replace('.txt',
    #                                                                                     bp_number + '.txt')
    #feature_dict_address = 'files/'+prefix+'FeatureDictionary_.txt'.replace('.txt', bp_number + '.txt')
    likelihoodRatio_filename = 'files/'+prefix+'TestStatisticsData_.txt'.replace('.txt', bp_number + '.txt')
    csv_address = 'files/'+prefix+'NucleotidesCount_.'.replace('.', bp_number + '.csv')
    Test_statistic_result_csv_address = 'files/'+prefix+'TestStaticticsResult_.'.replace('.', bp_number + '.csv')

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
                """ the first time  we see a line of sequence, we make a dictionary of
                    index of nucleotide, NucleotidesCount()]
                    with length len(line) -4 ( start from 2 , end at line -2 )  
                """
                if is_first_time_to_make_nucleotides_dictionary:
                    for i in range(2, len(line) - 2):
                        nucleotidesDictionary[i] = VerticalCut()
                    is_first_time_to_make_nucleotides_dictionary = False

                countNucleotides(nucleotidesDictionary, line, infoDictionary[fastafile_line_counter].technology)
                #nwl_context_counter = setcontext(featuresDictionary, line, nwl_context_counter, fastafile_line_counter)

                fastafile_line_counter += 1

    is_header = True
    for elem in nucleotidesDictionary:
        nucleotidesDictionary[elem].likelihoodRatioTest(likelihoodRatio_filename, is_header,
                                                        Test_statistic_result_csv_address)
        is_header = False

    """save data for all dictionaries in file """
    #ReadAndWrite.saveDictionaryWith_toPrint(infoDictionary, nucleotide_dict_address)
    #ReadAndWrite.saveDictionaryWith_toPrint(featuresDictionary, feature_dict_address)

    #ReadAndWrite.saveDictionaryWith_toprintAndCSV(nucleotidesDictionary, nucleotide_count_dict_address, csv_address)

