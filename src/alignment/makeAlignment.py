import logging

from utilities.DBConnection import readSeqTech, readMetadata
from utilities.DBConnection import addColumnToTable, updateTable
from utilities.ReadAndWrite import saveToCsv

logger = logging.getLogger(__name__)


def nextData(fastaFile, countryFilter):
    sequence = ''
    header = ''
    with open(fastaFile) as infile:
        for line in infile:
            line = line.strip()
            if line == '':
                return
            if line.__contains__('>'):
                if line.split('|')[0].split('/')[1].lower().__contains__(str(countryFilter).lower()):
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


def parseFastaFile(countryFilter, inputFastaFile, outputFastaFile):
    tableName='worldtest'
    #addSeqTechToMSAMetaData(tableName)
    isHeader = True
    try:
        with open(outputFastaFile, 'w', encoding='utf-8') as f1:
            for header, seq in nextData(inputFastaFile, countryFilter):

                if header is None:
                    continue

                else:
                    virusName, country, accessionId, collectionDate, continent = parseHeader(header)

                    technology = findSequenceByCountryDB(accessionId, continent, country)
                    newHeader = header.rstrip() + '|' + technology
                    f1.write(str(newHeader) + '\n' + str(seq) + '\n')
                    saveToCsv('files/MSAAlignedMatrix.csv', [accessionId, seq],
                              ['Accession id', 'Seq align'], isHeader)
                    isHeader = False
                    updateSeqTechInTable(tableName, accessionId, technology)

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


def findSequenceByCountryDB(accessionId, continent, country):
    if continent.__contains__('NorthAmerica'):
        continent = 'North America'
    elif continent.__contains__('SouthAmerica'):
        continent = 'South America'

    return readSeqTech(country, accessionId, continent, country)


def addSeqTechToMSAMetaData(tableName):
    addColumnToTable(tableName, 'Sequencing_technology')


def updateSeqTechInTable(tableName, accessionId, value):
    updateTable(tableName,'gisaid_epi_isl', accessionId, 'Sequencing_technology', value)
