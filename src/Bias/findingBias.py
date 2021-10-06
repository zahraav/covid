import csv
import os


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


# def modifySeqTechInFastaFile():
#    print('a')


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

        print('analyze', stats)
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


def printStats(stats, header, fileName, isHeader, numberOfElement):
    # print('printStat', header, fileName)
    print(stats['Nanopore'], '      ', stats['Illumina'])
    for nElem, iElem in zip(stats['Nanopore'], stats['Illumina']):
        csvList = [sum(nElem)]
        for k in nElem:
            csvList.append(k)
        csvList.append(sum(iElem))
        for n in iElem:
            csvList.append(n)
        percentCsvList = csvList.copy()

        # print(header.__len__(), ' length')

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

        saveToCsv(fileName.replace('.fasta', 'Normal.csv'), csvList, header, isHeader)
        saveToCsv(fileName.replace('.fasta', 'Percentage.csv'), percentCsvList, header, isHeader)
        isHeader = False


def parse(inputFile):
    """
    This method get a fasta file as an input , then send the file to analyzeFasta() method and as result
    it gets an dictionary full of nucleotide's count in every index in sequence for different sequence
    technology. And save them in two files, one CSV file that contains count and another CSV file which
    contains the percentage.
    :param inputFile: fasta file (MSA file)
    :return:
    """
    isHeader = True
    stats = analyzeFasta(inputFile, ChangedIUPACNucleotideCodes)
    iupacStats = analyzeFasta(inputFile, IUPACNucleotideCodes)
    # print(stats)
    printStats(stats,
               ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1',
                '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2',
                'N2', 'GAP2'], inputFile, isHeader, 7)
    iupacHeader = ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'U1', 'R1', 'Y1',
                   'S1', 'W1', 'K1',
                   'M1', 'B1', 'D1', 'H1', 'V1', 'N1', 'Gap1',
                   '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'U2', 'R2', 'Y2',
                   'S2', 'W2', 'K2',
                   'M2', 'B2', 'D2', 'H2', 'V2', 'N2', 'Gap2']
    printStats(iupacStats, iupacHeader, inputFile.replace('.fasta', 'IUPAC.fasta'), isHeader, 18)


def analyseSeqTechnologyBias(TSVFolder, fastaFile, outFastaFile):
    addSeqTechToFastaFile(outFastaFile, TSVFolder, fastaFile)
    parse(outFastaFile)

# analyseSeqTechnologyBias("files/26-9-2021-lastVersion/TSV", "files/26-9-2021-lastVersion/input/test_MSA_2.fasta",
#                         "files/26-9-2021-lastVersion/test_MSAWithSequenceTechnology.fasta")
