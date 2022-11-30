import csv
import os
import configparser
import datetime

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getDateFromHeaderLine(header):
    """
    date in yyyy/mm/dd format
    This method get a header line of a fasta file and returns the collectionDate from the header.
    :param header: A header line of a fasta file
    :return: CollectionDate
    """
    splitHeader = header.split('|')
    x = getDate(splitHeader[2])
    return x


def getDate(tempDate):
    """
    temp Date is Date but in string format, so this method make a date from tempDate and return it
    :param tempDate:
    :return: Date
    """
    cd = tempDate.split('-')
    if cd.__len__() == 2 or int(cd[2]) == 0:  # some collection dates in GisAid doesn't have day.
        cd[2] = 1
    if int(cd[1]) == 0:
        cd[1] = 1

    return datetime.datetime(int(cd[0]), int(cd[1]), int(cd[2]))


def isInThePeak(peak, tempTime):
    return True if peak[0] < tempTime < peak[1] else False


"""
save IUPAC Nucleotide Codes into 5 number  
"""
ChangedIUPACNucleotideCodes = {'A': 0, 'W': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 1, 'Y': 1,
                               'B': 1, 'H': 1, 'G': 2, 'S': 2, 'R': 2, 'K': 2, 'T': 3,
                               'U': 3, 'N': 4, '-': 5, '.': 5}

IUPACNucleotideCodes = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'U': 4, 'R': 5, 'Y': 6, 'S': 7,
                        'W': 8, 'K': 9, 'M': 10, 'B': 11, 'D': 12, 'H': 13, 'V': 14,
                        'N': 15, '-': 16, '.': 16}


def analyzeFasta(inFastaFile, codesDictionary):
    """
    This method get a fastaFile as an input and make a dictionary which contains two arrays
    for different sequence technologies (Nanopore and Illumina). Each of these arrays contains
    some arrays for every index in the sequence in fasta file.
    and in the arrays in every index there is number which shows the count of that nucleotide
    in sequences that used that sequence technology.
    This method is make the arrays with all IUPAC codes.
    :param codesDictionary: Dictionary that contains the codes
    :param inFastaFile: input fasta file
    :return: dictionary contains two array one for Nanopore and one for Illumina.
    """

    headerLine = 1
    type_ = 'none'
    stats = {'Nanopore': [], 'Illumina': []}

    with open(inFastaFile, 'r') as fasta_file:
        for line in fasta_file:
            if headerLine == 0:
                headerLine = 1

                if type_ != 'Nanopore' and type_ != 'Illumina':
                    continue
                pos = 0
                for ch in line.strip().rstrip():
                    if len(stats[type_]) == pos:
                        stats[type_].append([0] * len(set(codesDictionary.values())))
                    stats[type_][pos][codesDictionary[ch]] = \
                        stats[type_][pos][codesDictionary[ch]] + 1

                    pos = pos + 1
                continue
            headerLine = 0
            header = line.strip().rstrip().split("|")
            type_ = header[-1]

        return stats


def saveToCsv(csvFile, csvList, fieldNames, isHeader):
    """
     is_header should set to true for the first time then it should set to false for rest of calls
    this print the header in CSV file.
     if it doesn't set to false it will print the header for every line.
    :param csvFile:
    :param csvList:
    :param fieldNames:
    :param isHeader:
    :return:
    """
    x = {}
    for name, elem in zip(fieldNames, csvList):
        x[name] = str(elem)
    with open(csvFile, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isHeader:
            writer.writeheader()
        writer.writerow(x)


def printStats(stats, header, isHeader, numberOfElement, isIupacCode):
    """

    :param isIupacCode: show if the codes are from IUPAC code or not
    :param stats:
    :param header:
    :param isHeader:
    :param numberOfElement:
    :return: CSV File
    """
    csvFile = config['outputAddresses'].get('csvFile')
    if isIupacCode:
        csvFile = csvFile.replace('.csv', 'IUPAC.csv')

    for nElem, iElem in zip(stats['Nanopore'], stats['Illumina']):
        csvList = [sum(nElem)]
        for k in nElem:
            csvList.append(k)
        csvList.append(sum(iElem))
        for n in iElem:
            csvList.append(n)
        percentCSVList = csvList.copy()

        for i in range(1, numberOfElement - 1, ):
            if percentCSVList[0] == 0:
                percentCSVList[i] = 0
            else:
                percentCSVList[i] = percentCSVList[i] / percentCSVList[0] * 100

            if percentCSVList[numberOfElement] == 0:
                percentCSVList[i + numberOfElement] = 0
            else:
                percentCSVList[i + numberOfElement] = \
                    percentCSVList[i + numberOfElement] / percentCSVList[numberOfElement] * 100

        saveToCsv(csvFile, csvList, header, isHeader)
        saveToCsv(csvFile.replace(".csv", "Percentage.csv"), percentCSVList, header, isHeader)
        isHeader = False
    return csvFile


def parse(inputFile):
    """
    This method gets a fasta file as an input, then sends the file to analyzeFasta() method,
    and as a result, it gets a dictionary full of nucleotide's count in every index in sequence
    for different sequence technology. Then it saves them in two files, one CSV file that contains
    count and another one is a CSV file that contains the percentage.
    :param inputFile: fasta file (MSA file)
    :return: CSV file
    """
    isHeader = True
    stats = analyzeFasta(inputFile, ChangedIUPACNucleotideCodes)
    iupacStats = analyzeFasta(inputFile, IUPACNucleotideCodes)

    csvFile = printStats(stats,
                         ['nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', 'Illumina- sum', 'A2', 'C2', 'G2',
                          'T2', 'N2',
                          'GAP2'], isHeader, 7, False)

    iupacHeader = ['nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'U1', 'R1', 'Y1', 'S1', 'W1', 'K1',
                   'M1', 'B1', 'D1', 'H1', 'V1', 'N1', 'Gap1', 'Illumina- sum', 'A2', 'C2',
                   'G2', 'T2', 'U2', 'R2', 'Y2', 'S2', 'W2', 'K2', 'M2', 'B2', 'D2', 'H2', 'V2',
                   'N2', 'Gap2']

    printStats(iupacStats, iupacHeader, isHeader, 18, True)
    return csvFile


def getConsensus(maxNucleotide):
    """
    This method take a list of Nucleotides that have the same count in the one cut and return the consensus for that
    index.
    :param maxNucleotide: List of nucleotides with same count in a cut
    :return: IUPAC code of the nucleotides
    in the list
    """
    if maxNucleotide.__len__() == 2:
        if maxNucleotide.__contains__('A1') or maxNucleotide.__contains__('A2'):
            if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):  # ['A','G']-->'R'
                return 'R'

            if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):  # ['A','T']-->'W'
                return 'W'

            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):  # ['C','A']-->'M'
                return 'M'

        if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):
            if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):  # ['C','T']-->'Y'
                return 'Y'

        if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):
            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):  # ['C','G']-->'S'
                return 'S'

        if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):
            if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):  # ['T','G']-->'K'
                return 'K'

    if maxNucleotide.__len__() == 3:
        if maxNucleotide.__contains__('A1') or maxNucleotide.__contains__('A2'):
            if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):
                if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):  # ['A','G','T]-->'D'
                    return 'D'

        if maxNucleotide.__contains__('A1') or maxNucleotide.__contains__('A2'):
            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):
                if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):  # ['A','C','T]-->'H'
                    return 'H'

        if maxNucleotide.__contains__('A1') or maxNucleotide.__contains__('A2'):
            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):
                if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):  # ['A','C','G]-->'V'
                    return 'V'

        if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):
            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):
                if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):  # ['T','C','G]-->'B'
                    return 'B'

    if maxNucleotide.__len__() == 4:
        if maxNucleotide.__contains__('A1') or maxNucleotide.__contains__('A2'):
            if maxNucleotide.__contains__('C1') or maxNucleotide.__contains__('C2'):
                if maxNucleotide.__contains__('G1') or maxNucleotide.__contains__('G2'):
                    if maxNucleotide.__contains__('T1') or maxNucleotide.__contains__('T2'):
                        return 'N'
    return '.'


def returnCorrectValue(i):
    """
    This method check if the data is on the header or is a normal data
    then if it's from header change the header from csv to header to save in the transfacFormat txt file
    :param i: the header item
    :return: header in transfac format or data
    """
    header = ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1',
              '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2']

    if header.__contains__(i):
        # for converting A1,A2,C1,C2 which remained from csv to ... to A,A,C, ...
        return i[0]
    else:
        return i


def transfacGenerator(csvFile, transfacFileAddress):
    """
    This Method gets a csv file as an input and generate a transfac format file
    :param transfacFileAddress: transfac format file which is going to saved on the transfacFileAddress
    :param csvFile: input file, contains all data to transfer into csv format
    :return:
    """
    header = ['index', 'A1', 'C1', 'G1', 'T1', 'consensus1', 'A2', 'C2', 'G2', 'T2', ' consensus2']
    lineCounter = 0
    with open(transfacFileAddress, 'w') as outFile:

        outFile.write("XX")
        outFile.write("\n")
        outFile.write("ID  .....")
        outFile.write("\n")
        outFile.write("XX")
        outFile.write("\n")

        with open(csvFile, newline='') as csvFile:

            for row in csv.reader(csvFile):
                columnCount = 1
                maxNucleotide = []
                if lineCounter == 0:  # header Line
                    # newCsvLine.append('PO')
                    outFile.write('P0')
                    outFile.write("\t")
                    maxNucleotide = ['-']
                else:
                    # newCsvLine = [str(lineCounter)]
                    outFile.write(str(lineCounter))
                    outFile.write("\t")
                maxInLine = 0
                for i in row[1:5]:
                    if lineCounter != 0:
                        if int(i) > int(maxInLine):
                            maxInLine = i
                            maxNucleotide = [header[columnCount]]
                        elif int(i) == int(maxInLine):
                            maxNucleotide.append(header[columnCount])

                    outFile.write(returnCorrectValue(i))
                    outFile.write("\t")
                    columnCount = columnCount + 1

                if maxNucleotide.__len__() > 1:
                    maxNucleotide = [getConsensus(maxNucleotide)]

                outFile.write(maxNucleotide[0][0])
                outFile.write("\t")

                maxNucleotide.clear()
                maxInLine = 0
                columnCount = 6
                for i in row[8:12]:
                    if lineCounter != 0:
                        if int(i) > int(maxInLine):
                            maxInLine = i
                            maxNucleotide = [header[columnCount]]
                        elif int(i) == int(maxInLine):
                            maxNucleotide.append(header[columnCount])

                    outFile.write(returnCorrectValue(i))
                    outFile.write("\t")
                    columnCount = columnCount + 1

                if maxNucleotide.__len__() > 1:
                    maxNucleotide = [getConsensus(maxNucleotide)]
                if maxNucleotide.__len__() == 0:
                    maxNucleotide = ['-']
                outFile.write(maxNucleotide[0][0])
                outFile.write("\n")
                # newCsvLine.append(maxNucleotide[0][0])

                lineCounter = lineCounter + 1

        outFile.write("XX")
        outFile.write("\n")
        outFile.write("CC Program: ")
        outFile.write("\n")
        outFile.write("XX")
        outFile.write("\n")
        outFile.write("\\\\")
        outFile.write("\n")


def separatePeaks(fastaFile, peakOneDates, peakTwoDates, peakThreeDates):
    """
    This Function separate sequences in every peak and save them in a different file,
    so That we can make a charts and other analysis by using each of these files.
    :param fastaFile: The main fasta file containing all data.
    :param peakOneDates: The list for first peak [start Date,end Date]
    :param peakTwoDates: The list for second peak [start Date,end Date]
    :param peakThreeDates: The list for third peak [start Date,end Date]
    :return:
    """

    firstPeakFasta = config['outputAddresses'].get('firstPeak')
    secondPeakFasta = config['outputAddresses'].get('secondPeak')
    thirdPeakFasta = config['outputAddresses'].get('thirdPeak')

    # open three fasta files to separate sequences of each peak on a different file
    firstPeak = open(firstPeakFasta, "w")
    secondPeak = open(secondPeakFasta, "w")
    thirdPeak = open(thirdPeakFasta, "w")

    flag = 0

    with open(fastaFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                collectionDate = getDateFromHeaderLine(line)

                if isInThePeak(peakOneDates, collectionDate):
                    firstPeak.write(line)
                    flag = 1

                if isInThePeak(peakTwoDates, collectionDate):
                    secondPeak.write(line)
                    flag = 2

                if isInThePeak(peakThreeDates, collectionDate):
                    thirdPeak.write(line)
                    flag = 3

            elif flag != 0:
                if flag == 1:
                    firstPeak.write(line)
                    flag = 0
                elif flag == 2:
                    secondPeak.write(line)
                    flag = 0
                elif flag == 3:
                    thirdPeak.write(line)
                    flag = 0

    firstPeak.close()
    secondPeak.close()
    thirdPeak.close()


def analyseSeqTechnologyBias(fastaFile):
    """
    This method Analyse the sequences
    and CSV files related to the MSA (multiple sequence alignment) and find bias for 3 major
    peak of SARS-COV-2
    :param fastaFile: fasta file containing sequence technology
    :return:
    """
    if not os.path.isdir('files/output/Peaks'):
        os.mkdir('files/output/Peaks')
    if not os.path.isdir('files/output/TransfacFormat'):
        os.mkdir('files/output/TransfacFormat')

    # take the date of three major peak from config file
    # firstPeak = config['peaks'].get('firstPeakDate').split(",")
    # secondPeak = config['peaks'].get('secondPeakDate').split(",")
    # thirdPeak = config['peaks'].get('thirdPeakDate').split(",")

    # separatePeaks(fastaFile, [getDate(firstPeak[0]), getDate(firstPeak[1])],
    #              [getDate(secondPeak[0]), getDate(secondPeak[1])], [getDate(thirdPeak[0]), getDate(thirdPeak[1])])

    csvFile = parse(fastaFile)

    # testTransfacGenerator:
    # csvFile = config['outputAddresses'].get('csvFile')
    transfacFile = config['outputAddresses'].get('TransfacFile')

    transfacGenerator(csvFile, transfacFile)