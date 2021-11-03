import csv
import os

NanoporeNamesList = ["Oxford Nanopore Artic", "ONT_ARTIC", "Oxford Nanopore", "Oxford Nanopore GridION",
                     "Oxford Nanopore ARTIC", "MinION Oxford Nanopore", "Nanopore MinION", "MinION", "Nanopore ARTIC",
                     "GridION", "Nanopore MinIon", "Ion Torrent", "ONT ARTIC", "Nanopore minION",
                     "Nanopore MinION Mk1C",
                     "Nanopore GridION", "Nanopore GridION, ARTIC V3 protocol", "Oxford Nanopore MinION", "Nanopore"]

IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq"]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown"]


def makeDictionaryOfSeqTech(tsvFile):
    """
    This method make a dictionary of sequence Technologies in the given TSV file
    and return the dictionary.seqTecDictionary
    :param tsvFile: tsv file that used for returning dictionary of {accessionId: SequenceTechnology}
    """

    firstRow = True
    with open(tsvFile) as fd:
        # {[Accession Id , sequence Technology]}
        seqTecDictionary = {}

        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            if firstRow:
                firstRow = False
                continue
            else:
                seqTecDictionary[row[1]] = row[8]

    return seqTecDictionary


def makeDictionaryOfSeqTechForEachFile(folderName):
    """
    This method check the folderName and send every TSV file to makeDictionaryOfSeqTech method
    to make one dictionary of {accessionID: SeqTechnology}
    :param folderName: folder that contains TSV files
    :return:
    """
    sequenceTechnologyDictionary = {}
    for fileName in os.listdir(folderName):
        fileName = folderName + "/" + fileName
        sequenceTechnologyDictionary.update(makeDictionaryOfSeqTech(fileName))

    return sequenceTechnologyDictionary


def find_accession_id(header):
    """
    This method get a header line of a fasta file and returns the accession Id of the header.
    :param header: A header line of a fasta file
    :return: accessionID
    """
    split_header = header.split('|')
    for i in split_header:
        if i.__contains__('EPI'):
            return i


def alterSeqTechnologiesName(seqDictionary):
    updatedSeqTech = {}
    for a in seqDictionary:
        if NanoporeNamesList.__contains__(seqDictionary[a]):
            updatedSeqTech[a] = 'Nanopore'
        elif IlluminaNamesList.__contains__(seqDictionary[a]):
            updatedSeqTech[a] = 'Illumina'
    return updatedSeqTech


def addSeqTechToFastaFile(newFastaAddress, tsvFolder, inFastaFile):
    """
    This method make a new fasta file and insert the seq technology from
    {accessionId :sequenceTechnology} dictionary that generated in the
    makeDictionaryOfSeqTechForEachFile(tsvFolder) method
    header, using accession Id
    :param newFastaAddress: New fasta file name
    :param tsvFolder: Name of TSV folder containing all TSV files
    :param inFastaFile: Address of input Fasta File
    :return:
    """
    seqDictionary = makeDictionaryOfSeqTechForEachFile(tsvFolder)
    firstTime = True
    for a in seqDictionary:
        if not NanoporeNamesList.__contains__(seqDictionary[a]) and \
                not IlluminaNamesList.__contains__(seqDictionary[a]) and \
                not unknownSequencerList.__contains__(seqDictionary[a]):
            if firstTime:
                print("newSeqTechnologies: please add them to the list in class FindingBiass:")
                firstTime = False
            else:
                print(seqDictionary[a])

    seqDictionary = alterSeqTechnologiesName(seqDictionary)

    f = open(newFastaAddress, "w")

    isContainsSeq = False

    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):

                accessionId = find_accession_id(line)
                if seqDictionary.__contains__(accessionId):
                    f.write(line.strip())
                    f.write("|")
                    f.write(seqDictionary[accessionId])
                    f.write('\n')
                    isContainsSeq = True

            elif isContainsSeq:
                f.write(line)
                isContainsSeq = False
    f.close()
    # modifySeqTechInFastaFile()


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


def saveToCsv(fileName, csvList, fieldNames, isHeader):
    """
     is_header should set to true for the first time then it should set to false for rest of calls
    this print the header in CSV file.
     if it doesn't set to false it will print the header for every line.
    :param fileName:
    :param csvList:
    :param fieldNames:
    :param isHeader:
    :return:
    """
    x = {}
    for name, elem in zip(fieldNames, csvList):
        x[name] = str(elem)
    with open(fileName, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isHeader:
            writer.writeheader()
        writer.writerow(x)


def printStats(stats, header, csvFile, isHeader, numberOfElement):
    for nElem, iElem in zip(stats['Nanopore'], stats['Illumina']):
        csvList = [sum(nElem)]
        for k in nElem:
            csvList.append(k)
        csvList.append(sum(iElem))
        for n in iElem:
            csvList.append(n)
        percentCsvList = csvList.copy()

        for i in range(1, numberOfElement - 1, ):
            if percentCsvList[0] == 0:
                percentCsvList[i] = 0
            else:
                percentCsvList[i] = percentCsvList[i] / percentCsvList[0] * 100

            if percentCsvList[numberOfElement] == 0:
                percentCsvList[i + numberOfElement] = 0
            else:
                percentCsvList[i + numberOfElement] = \
                    percentCsvList[i + numberOfElement] / percentCsvList[numberOfElement] * 100

        saveToCsv(csvFile, csvList, header, isHeader)
        saveToCsv(csvFile.replace('.csv', 'Percentage.csv'), percentCsvList, header, isHeader)
        isHeader = False


def parse(inputFile, csvFile):
    """
    This method get a fasta file as an input , then send the file to analyzeFasta() method and as result
    it gets an dictionary full of nucleotide's count in every index in sequence for different sequence
    technology. And save them in two files, one CSV file that contains count and another CSV file which
    contains the percentage.
    :param csvFile:
    :param inputFile: fasta file (MSA file)
    :return:
    """
    isHeader = True
    stats = analyzeFasta(inputFile, ChangedIUPACNucleotideCodes)
    iupacStats = analyzeFasta(inputFile, IUPACNucleotideCodes)

    printStats(stats, ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1',
                       '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2'],
               csvFile, isHeader, 7)

    iupacHeader = ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'U1', 'R1', 'Y1',
                   'S1', 'W1', 'K1',
                   'M1', 'B1', 'D1', 'H1', 'V1', 'N1', 'Gap1',
                   '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'U2', 'R2', 'Y2',
                   'S2', 'W2', 'K2',
                   'M2', 'B2', 'D2', 'H2', 'V2', 'N2', 'Gap2']

    printStats(iupacStats, iupacHeader, csvFile.replace('.csv', 'IUPAC.csv'), isHeader, 18)


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
                        #print(maxNucleotide)
                        return 'N'
    return '.'


def returnCorrectValue(i):
    header = ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1',
              '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2']

    if header.__contains__(i):
        # for converting A1,A2,C1,C2 which remained from csv to ... to A,A,C, ...
        return i[0]
    else:
        return i


def transfacGenerator(csvFile, transfacFile):
    header = ['index', 'A1', 'C1', 'G1', 'T1', 'consensus1', 'A2', 'C2', 'G2', 'T2', ' consensus2']
    lineCounter = 0
    with open(transfacFile, 'w') as outFile:

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
                    # newCsvLine.append(i)
                    columnCount = columnCount + 1

                if maxNucleotide.__len__() > 1:
                    maxNucleotide = [getConsensus(maxNucleotide)]

                outFile.write(maxNucleotide[0][0])
                outFile.write("\t")

                maxNucleotide = ['-']
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


def analyseSeqTechnologyBias(TSVFolder, fastaFile, outFastaFile, transfacFile, csvFile):
    addSeqTechToFastaFile(outFastaFile, TSVFolder, fastaFile)
    parse(outFastaFile, csvFile)

    transfacGenerator(csvFile, transfacFile)
# analyseSeqTechnologyBias("files/26-9-2021-lastVersion/input/TSV",
#                         "files/26-9-2021-lastVersion/input/test_MSA_2.fasta",
#                         "files/26-9-2021-lastVersion/output/test_MSAWithSequenceTechnology.fasta")
