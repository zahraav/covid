import logging

from utilities.ReadAndWrite import saveToCsv

logger = logging.getLogger(__name__)


def nextData(fastaFile):
    sequence = ''
    header = ''
    with open(fastaFile) as infile:
        for line in infile:
            line = line.strip()
            if line == '':
                return
            if line.__contains__('>'):
                if header != '':
                    yield header, sequence
                    sequence = ''
                header = line
            else:
                sequence = sequence.rstrip("\n") + line.rstrip("\n")

            #  tempseq = sequence
            #  temph = header
            #  header = ''
            #  sequence = ''
        yield header, sequence


def parseFastaFile(tableName, inputFastaFile, outputFastaFile):
    # addSeqTechToMSAMetaData(tableName)
    isHeader = True
    try:
        with open(outputFastaFile, 'w', encoding='utf-8') as f1:
            for header, seq in nextData(inputFastaFile):

                if header is None:
                    continue

                else:
                    accessionId = header.split('|')[1]
                    technology = findSeqTechByID(tableName, accessionId)
                    # newHeader = header.rstrip() + '|' + str(technology)
                    f1.write(header.rstrip())
                    f1.write('|')
                    f1.write(str(technology))
                    f1.write('\n')
                    f1.write(seq)
                    f1.write('\n')
                    saveToCsv('files/MSAAlignedMatrix.csv', [accessionId, seq],
                              ['Accession id', 'Seq align'], isHeader)
                    isHeader = False

    except MemoryError as e:
        logger.error(e)


def parseHeader(header):
    headerSplitList = header.split('|')
    virusNameSplitList = headerSplitList[0].split('/')
    country = virusNameSplitList[1]
    virusName = country + '/' + virusNameSplitList[2] + '/' + virusNameSplitList[3]

    accessionId = headerSplitList[1]
    collectionDate = headerSplitList[2]
    continent = headerSplitList[3]

    return virusName, country, accessionId, collectionDate, continent
