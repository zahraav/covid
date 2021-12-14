import configparser
import csv
import logging
import os
import re

from alignment.makeAlignment import parseFastaFile
from bias.findingBias import analyseSeqTechnologyBias
from mutationAnalysis.mutation import mutationAnalysis
from bias.graphGenome import drawGraphGenome

CONFIG_FILE = r'config/config.cfg'

logging.basicConfig(filename="%s" % 'src/logs/logs.log',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()

# List of Nanopore names in TSV file
NanoporeNamesList = ["Oxford Nanopore Artic", "ONT_ARTIC", "Oxford Nanopore", "Oxford Nanopore GridION",
                     "Oxford Nanopore ARTIC", "MinION Oxford Nanopore", "Nanopore MinION", "MinION", "Nanopore ARTIC",
                     "GridION", "Nanopore MinIon", "Ion Torrent", "ONT ARTIC", "Nanopore minION",
                     "Nanopore MinION Mk1C", "Oxford Nanopore Technologies ARTIC"
                                             "Nanopore GridION", "Nanopore GridION, ARTIC V3 protocol",
                     "Oxford Nanopore MinION", "Nanopore",
                     "Oxford Nanopore - Artic", "Nanopore GridION", "Oxford Nanopore Technologies ARTIC"]

# List of Illumina in TSV file
IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq"]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown"]


def removeSpace(inputFile, outputFile):
    """
    This class remove the spaces in the header lines of fasta file for
    converting metadata from TSV to fasta file
    """
    # inputFile = 'files/slice/output_slice_seq.fasta'
    # outputFile = inputFile.replace('.fasta', '_2.fasta')
    with open(inputFile) as infile:
        for line in infile:
            line = line.rstrip()
            with open(outputFile, 'a+', newline='') as file:
                if line.__contains__('>'):
                    line = re.sub("\s", "_", line)
                file.write(line)
                file.write('\n')


def getSequenceTechnology(header):
    """
    This method get a header line of a fasta file and returns the sequence technology from the header.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    return header.split("|")[4].strip()


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


def alterSeqTechnologiesName(seqDictionary):
    """
    This method change the name for different sequence technologies.
    if the sequence technology that it founds is on the nanopore List, then it's going to be saved as Nanopore
    else if the name is on the Illumina list it's going to be saved as Illumina.
    Otherwise if its on the unknown list( list of sequencer which are not Illumina or Nanopore)
    it is going to be saved as unknown.
    :param seqDictionary: dictionary of sequencers for every sequence
    :return: new list of sequencers which only contains 3 item Illumina, Nanopore and unknown
    """
    updatedSeqTech = {}
    for a in seqDictionary:
        if NanoporeNamesList.__contains__(seqDictionary[a]):
            updatedSeqTech[a] = 'Nanopore'
        elif IlluminaNamesList.__contains__(seqDictionary[a]):
            updatedSeqTech[a] = 'Illumina'
        elif unknownSequencerList.__contains__(seqDictionary[a]):
            updatedSeqTech[a] = 'unknown'
    return updatedSeqTech


def getAccessionId(header):
    """
    This method get a header line of a fasta file and returns the accession Id from the header.
    :param header: A header line of a fasta file
    :return: accessionID
    """
    splitHeader = header.split('|')
    for i in splitHeader:
        if i.__contains__('EPI'):
            return i


def addSeqTechToFastaFile(tsvFolder, inFastaFile):
    """
    This method make a new fasta file and insert the seq technology from
    {accessionId :sequenceTechnology} dictionary that generated in the
    makeDictionaryOfSeqTechForEachFile(tsvFolder) method
    header, using accession Id
    :param tsvFolder: Name of TSV folder containing all TSV files
    :param inFastaFile: Address of input Fasta File
    :return: Fasta file containing sequencing technology
    """

    outFastaFile = config['outputAddresses'].get('fullFastaFile')

    seqDictionary = makeDictionaryOfSeqTechForEachFile(tsvFolder)
    firstTime = True
    for a in seqDictionary:
        if not NanoporeNamesList.__contains__(seqDictionary[a]) and \
                not IlluminaNamesList.__contains__(seqDictionary[a]) and \
                not unknownSequencerList.__contains__(seqDictionary[a]):
            if firstTime:
                print("newSeqTechnologies: please add them to the list in class FindingBias:")
                firstTime = False
            else:
                print(seqDictionary[a])

    seqDictionary = alterSeqTechnologiesName(seqDictionary)

    f = open(outFastaFile, "w")

    isContainsSeq = False

    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):

                accessionId = getAccessionId(line)
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

    return outFastaFile


def main():
    """
    The pipeline starts here,
    For generating the output please uncomment the different parts in the same order as following

    :return:
    """
    inputFastaFile = config['inputAddresses'].get('inputFastaFile')
    tsvFolder = config['inputAddresses'].get('TSVFolder')
    outFastaFile = addSeqTechToFastaFile(tsvFolder, inputFastaFile)

    """
    this method call all f the pipeline.
    Bias:
    """
    analyseSeqTechnologyBias(outFastaFile)

    # alignedFileFame = config['address'] + "aligned_" + config['address'].get('inputFastaFile')
    # parseFastaFile("", 'files/test_MSA_2.fasta', 'files/output_Test_MSA_22.fasta')
    # addSeqTechToMSAMetaData()
    # process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')

    """
    Mutation Analysis
    """

    # globalTree = config['inputAddresses'].get('globalTree')
    # metadataFile = config['inputAddresses'].get('metaDate')
    # mutationAnalysis(globalTree, metadataFile)

    """
    Graph Genome
    """
    # fastaFileWithSequenceTechnology = config['outputAddresses'].get('fullFastaFile')
    # inFasta = config['outputAddresses'].get('fullFastaFile')
    inFasta = config['separateFiles'].get('outputFastaFile')

    # makeGraphGenome(inFasta)

    # makeGraphGenome(config,fastaFileWithSequenceTechnology)
    # drawGraphGenome(fastaFileWithSequenceTechnology)
    drawGraphGenome(inFasta)


if __name__ == '__main__':
    main()

"""
def main():
    config = get_configs()
    basePairCount=config['databaseInfo'].get('basePairCount')
    table_name=config['databaseInfo'].get('table_name')

    input_fasta_file = config['address'].get('folder')+table_name+\
                       config['address'].get('input_fastafile')



    aligned_file_name = config['address'].get('folder')+"aligned_"+\
                  table_name+ config['address'].get('input_fastafile')\
                      .replace(".fasta","_"+basePairCount+".fasta")


    #basePairCount=int(basePairCount)
    is_header=True
    change_fasta_header(aligned_file_name,basePairCount,input_fasta_file,is_header)

    #align_seq(input_fasta_file)

    parseFastaFile(table_name,'files/test_MSA_2.fasta','files/output_Test_MSA_22.fasta')
    #addSeqTechToMSAMetaData()
    #process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')


"""
