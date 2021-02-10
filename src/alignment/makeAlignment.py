import logging

from utilities.DBConnection import readSeqTech, readMetadata
from utilities.DBConnection import addColumnToTable
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
                if line.split('|')[0].split('/')[1].lower():
                    header = line
                else:
                    header = None
            else:
                if header is None:
                    sequence = None
                else:
                    sequence = str(sequence).rstrip("\n") + str(line).rstrip("\n")

                tempseq = sequence
                temph = header
                header = ''
                sequence = ''
                yield temph, tempseq


def parseFastaFile(inputFastaFile, outputFastaFile):
    tableName='world2'
    #addSeqTechToMSAMetaData(tableName)
    isHeader = True
    try:
        with open(outputFastaFile, 'w', encoding='utf-8') as f1:
            for header, seq in nextData(inputFastaFile):

                if header is None:
                    continue

                else:
                    virusName, country, accessionId, collectionDate, continent = parseHeader(header)

                    technology = findSeqTechByID(accessionId)
                    newHeader = str(header.rstrip()) + '|' + str(technology)
                    f1.write(str(newHeader) + '\n' + str(seq) + '\n')
                    saveToCsv('files/MSAAlignedMatrix.csv', [accessionId, seq],
                              ['Accession id', 'Seq align'], isHeader)
                    isHeader = False

    except MemoryError as e:
        logger.error(e)


def updateHeader(header, accessionId):
    return header + '|' + readSeqTech(accessionId)


def getMetadata(accessionID):
    return readMetadata(accessionID)


def parseHeader(header):
    headerSplitList = header.split('|')
    virusNameSplitList = headerSplitList[0].split('/')
    country = virusNameSplitList[1]
    virusName = country + '/' + virusNameSplitList[2] + '/' + virusNameSplitList[3]

    accessionId = headerSplitList[1]
    collectionDate = headerSplitList[2]
    continent = headerSplitList[3]

    return virusName, country, accessionId, collectionDate, continent


def findSeqTechByID(accessionId):
    return readSeqTech('world2',accessionId)


def addSeqTechToMSAMetaData(tableName):
    addColumnToTable(tableName, 'Sequencing_technology')

