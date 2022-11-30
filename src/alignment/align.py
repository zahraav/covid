from Bio import SeqIO
from Bio.Align.Applications import MuscleCommandline  # Read in unfiltered data

import logging

from utilities.ReadAndWrite import saveToCsv

logger = logging.getLogger(__name__)


def findSeqTechByID(tableName, accessionId):
    print(tableName, accessionId)
    return ''


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

            #  tempSeq = sequence
            #  tempH = header
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


def alignFastaFile(fastaFile):
    # fastaFile="files/test.fasta"
    unfiltered = SeqIO.parse(fastaFile, "fasta")  # Drop data without (close to) full length sequences
    full_length_records = []
    for record in unfiltered:
        if len(record.seq) > 29000:
            full_length_records.append(record)  # Write filtered data to file
    SeqIO.write(full_length_records, fastaFile.replace('.fasta', "_2") + ".fasta", "fasta")
    # Align sequences with MUSCLE (using parameters to make the alignment
    # process as fast as possible)
    muscle_cline = MuscleCommandline(input=fastaFile,
                                     out=fastaFile.replace('.fasta', "_aligned") + ".fasta",
                                     diags=True,
                                     maxiters=1,
                                     log="files/align_log.txt")
    muscle_cline()

# alignFastaFile("files/quebec_seqtech_gisaid_hcov-19_2021_01_13_23_1.fasta")"""
