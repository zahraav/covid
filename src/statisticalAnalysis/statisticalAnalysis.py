import csv

from StatisticalTest import FisherExactTest


def setInfo(line):
    """
    This method gets the header and exteract information in the header like
    Sequencing Technology, location, region, time
    :param line: header
    :return:
    """
    info = []
    # sequencing technology
    sequenceTech = ''
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


def savePValueDataToCSV(allCSV):
    csvOutputFile = "Files/output/statisticalAnalysis/p_valueThirdPeak.csv"
    header = ['NA', 'NC', 'NG', 'NT', 'IA', 'IC', 'IG', 'IT', 'A', 'C', 'G', 'T']
    with open(csvOutputFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in allCSV:
            j = list(map(str, i))
            writer.writerow(j)


def fisherExactTest(allDictionary, seqLength):
    """
    :param allDictionary: first Nanopore dictionary then Illumina dictionary
    :param seqLength:
    :return:
    """
    """
    
    def FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                        not_nucleotide_in_illumina, p_value_file='files/p_value.txt'):"""
    mainNucleotides = ['A', 'C', 'G', 'T']

    CSVdata = [[], [], []]  # [[Nanopore: A,C,G,T][Illumina : A,C,G,T][pValue]]
    allCSVData = []
    for l in range(seqLength):
        for x in range(mainNucleotides.__len__()):
            # print(allDictionary[l][0][x])
            nucleotide_in_nanopore = allDictionary[l][0][mainNucleotides[x]]
            nucleotide_in_illumina = allDictionary[l][1][mainNucleotides[x]]
            not_nucleotide_in_nanopore = sum(allDictionary[l][0].values()) - nucleotide_in_nanopore
            not_nucleotide_in_illumina = sum(allDictionary[l][1].values()) - nucleotide_in_illumina
            pValue = FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                                     not_nucleotide_in_illumina, 'files/output/statisticalAnalysis/p_valuePeakthreeNew.txt')
            CSVdata[0].append(nucleotide_in_nanopore)
            CSVdata[1].append(nucleotide_in_illumina)
            CSVdata[2].append(pValue)

        j = []
        for i in CSVdata:
            j = j.__add__(i)

        allCSVData.append(j)
        CSVdata = [[], [], []]
    savePValueDataToCSV(allCSVData)


def process_fasta_file(fasta_address):
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

    fisherExactTest(verticalTotalNucleotideDictionary, sequenceLength)


# process_fasta_file('files/output/peaks/firstTest.fasta')
process_fasta_file('files/output/peaks/thirdPeak.fasta')
