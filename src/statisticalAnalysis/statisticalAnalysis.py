import csv
import scipy.stats as stats
from utilities.ReadAndWrite import saveData


def generateCSVFile(inputFile, csvOutput, csvHeader):
    """
    This method converts a txt file containing p-value and Nucleotide counts into a CSV file.
    :param inputFile:
    :param csvOutput:
    :param csvHeader:
    :return:
    """
    with open(csvOutput, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)

        with open(inputFile) as infile:
            for line in infile:
                data = line.split(' ')
                data = list(filter(None, data))
                newData = []
                for x in data:
                    if x.__contains__('\n'):
                        newData.append(x.replace("\n", ""))
                    elif x.__contains__(':'):
                        pass
                    else:
                        newData.append(x)
                writer.writerow(newData)


def FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                    not_nucleotide_in_illumina, p_value_file='files/p_value.txt'):
    """
                 |       Nanopore      | Illumina
    -------------|---------------------|---------------
     Nucleotide  | n_in_Nanopore       |  n_in_Illumina
    -------------|---------------------|---------------
     !Nucleotide | not_n_in_Nanopore   | not_n_in_Illumina
                 |                     |
    """
    oddsRatio, p_value = stats.fisher_exact([[nucleotide_in_nanopore, nucleotide_in_illumina],
                                             [not_nucleotide_in_nanopore, not_nucleotide_in_illumina]])

    str_p_value = 'n_n: ' + str(nucleotide_in_nanopore) + '  n_i: ' + str(nucleotide_in_illumina) + '  nn_n: ' + str(
        not_nucleotide_in_nanopore) + '  nn_i: ' + str(not_nucleotide_in_illumina) + '  p_value: ' + str(
        p_value) + ' \n'
    saveData(p_value_file, str_p_value)
    return p_value


def setInfo(line):
    """
    This method gets the header and extract information in the header like
    Sequencing Technology, location, region, time
    :param line: header
    :return:
    """
    info = []
    # sequencing technology
    if 'nanopore' in line.lower():
        info.append('Nanopore')
        sequenceTech = 'Nanopore'
    elif 'illumina' in line.lower():
        info.append('Illumina')
        sequenceTech = 'Illumina'
    else:
        info.append('-')
        sequenceTech = '-'
    splitLine = line.rsplit('|')

    # location
    temp = splitLine[0].rsplit('/')
    country = temp[1]
    region = temp[2].rsplit('-')[0]  # state
    info.append(country)
    info.append(region)
    # time
    year_and_Month = splitLine[2].rsplit('-')
    time = ''
    if len(year_and_Month) > 1:
        if year_and_Month[1]:
            time = '-' + year_and_Month[1]

    time = year_and_Month[0] + time
    info.append(time)
    # print(info)
    return info, sequenceTech


def VerticalCutNucleotideCount(line, sequenceTechnology, verticalDictionary):
    """
    This method saves nucleotide counts in the vertical cut separately for Nanopore and Illumina
    :param verticalDictionary:
    :param sequenceTechnology:
    :param line:
    :return:
    """
    """ i started from location 2 of real sequence"""
    for x in range(0, len(line), 1):
        if sequenceTechnology == 'Nanopore':
            verticalDictionary[x][0][line[x]] += 1
        elif sequenceTechnology == 'Illumina':
            verticalDictionary[x][1][line[x]] += 1
        else:
            pass
    return verticalDictionary


def savePValueDataToCSV(allCSV, city):
    csvOutputFile = "Files/output/statisticalAnalysis/location/p_value_" + city + ".csv"
    header = ['NA', 'NC', 'NG', 'NT', 'IA', 'IC', 'IG', 'IT', 'A', 'C', 'G', 'T']
    with open(csvOutputFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in allCSV:
            j = list(map(str, i))
            writer.writerow(j)


def fisherExactTest(allDictionary, seqLength, city):
    """
    :param city:
    :param allDictionary: first Nanopore dictionary then Illumina dictionary
    :param seqLength:
    :return:
    """

    mainNucleotides = ['A', 'C', 'G', 'T']

    CsvData = [[], [], []]  # [[Nanopore: A,C,G,T][Illumina : A,C,G,T][pValue]]
    allCSVData = []
    for ll in range(seqLength):
        for x in range(mainNucleotides.__len__()):
            # print(allDictionary[l][0][x])
            nucleotide_in_nanopore = allDictionary[ll][0][mainNucleotides[x]]
            nucleotide_in_illumina = allDictionary[ll][1][mainNucleotides[x]]
            not_nucleotide_in_nanopore = sum(allDictionary[ll][0].values()) - nucleotide_in_nanopore
            not_nucleotide_in_illumina = sum(allDictionary[ll][1].values()) - nucleotide_in_illumina
            pValue = FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                                     not_nucleotide_in_illumina, 'files/output/statisticalAnalysis/'
                                                                 'location/p_value' + city + '.txt')
            CsvData[0].append(nucleotide_in_nanopore)
            CsvData[1].append(nucleotide_in_illumina)
            CsvData[2].append(pValue)

        j = []
        for i in CsvData:
            j = j.__add__(i)

        allCSVData.append(j)
        CsvData = [[], [], []]
    savePValueDataToCSV(allCSVData, city)


def process_fasta_file(fasta_address, city):
    infoDictionary = {}

    verticalTotalNucleotideDictionary = {}
    isFirstSequence = True
    sequenceLength = 0
    with open(fasta_address) as infile:
        for rLine in infile:
            line = rLine.strip()
            if '>' in line:
                accessionId = line.rsplit('|')[1]
                infoDictionary[accessionId], sequencingTechnology = setInfo(line)
            else:
                tempLine = line[2:len(line) - 2]

                if isFirstSequence:
                    count = 0
                    sequenceLength = len(tempLine)
                    for x in range(len(tempLine)):
                        nanopore = {'A': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 0, 'Y': 0, 'B': 0, 'H': 0, 'G': 0, 'S': 0,
                                    'R': 0, 'K': 0, 'T': 0, 'U': 0, 'W': 0, 'N': 0, '.': 0, '-': 0}
                        illumina = {'A': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 0, 'Y': 0, 'B': 0, 'H': 0, 'G': 0, 'S': 0,
                                    'R': 0, 'K': 0, 'T': 0, 'U': 0, 'W': 0, 'N': 0, '.': 0, '-': 0}

                        verticalTotalNucleotideDictionary[count] = [nanopore, illumina]
                        count += 1
                    isFirstSequence = False
                """ the first time  we see a line of sequence, we make a dictionary of
                    index of nucleotide, NucleotidesCount()]
                    with length len(line) -4 ( start from 2 , end at line -2 )
                """
                """verticalCutNucleotide is a method completing the dictionary containing all the vertical cuts of
                sequence"""
                verticalTotalNucleotideDictionary = VerticalCutNucleotideCount(tempLine, sequencingTechnology,
                                                                               verticalTotalNucleotideDictionary)

                sequencingTechnology = ''

    fisherExactTest(verticalTotalNucleotideDictionary, sequenceLength, city)


def statisticalAnalysis(inputFile):
    # Time
    # 'files/output/peaks/firstTest.fasta'
    # 'files/output/peaks/secondPeak.fasta'
    # 'files/output/peaks/thirdPeak.fasta'
    # process_fasta_file(inputFile)

    # header = ['Nanopore', 'A', 'C', 'G', 'T', 'N', 'Gap', 'Illumina', 'A', 'C', 'G', 'T', 'N', 'Gap', 'P_value', 'A',
    #          'C', 'G', 'T']
    # generateCSVFile('files/output/statisticalAnalysis/Canada_NucleotideCountDictionary.txt',
    #                'files/output/statisticalAnalysis/p_valueAll.csv', header)

    # location: BC, QC
    # process_fasta_file('files/input/statisticalAnalysis/msa_0206_BC_WithSeqTech.fasta', 'BC')
    process_fasta_file(inputFile, 'BC')
