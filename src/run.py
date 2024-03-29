import configparser
import csv
import logging
import os
import datetime
import sys
from datetime import *

from statisticalAnalysis.generatePeaks import analyse_sequence_technology_bias

# from graphGenome.compareSpikeToUCSCSpike import compareToUCSCSpike
# from graphGenome.graphGenome import drawGraphGenome

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
                     "Nanopore MinION Mk1C", "Oxford Nanopore Technologies ARTIC", "Ion_Torrent_S5",
                     "IonTorrent", "Nanopore GridION", "Nanopore GridION, ARTIC V3 protocol",
                     "Oxford Nanopore MinION", "Nanopore", "Ion_Torrent",
                     "Oxford Nanopore - Artic", "Nanopore GridION", "Oxford Nanopore Technologies ARTIC"]

# List of Illumina in TSV file
IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq", "Illumina_iSeq,_2_x_150bp_paired_end_reads,_ARTIC_V3,_Nextera_Flex_prep",
                     "Illumna_NextSeq", "Illumina_MiniSeq", "Illumina_MiSeq,_2x300bp", "NextSeq_500", "iSeq100",
                     "Illumina_/_iSeq", "NextSeq", "Illumina_MiSeq,_NextSeq", "llumina_NextSeq",
                     "Illumina_Nextseq,_Illumina_Miseq"
                     "MiSeq_V3_2x75_paired_reads_("
                     "Illumina)_+Nextera_Flex_Enrichment_Library_with_Respiratory_Virus_Oligo ", "NextSeq",
                     "nCoV_NextSeq", "Illumna_MiSeq", "nCoV_MiSeq",
                     "Illumina_NestSeq500 Swift_Amplicon_SARS-CoV-2_Panel+Illumina_MiniSeq Illumina_Miseq,"
                     "_2_x_250bp_paired_end_reads, "
                     "_ARTIC_V3,_Nextera_Flex_prep",
                     ]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown", "MGI_CleanPlex"]


def makeDictionaryOfSeqTech(tsvFile):
    """
    This method make a dictionary of sequence Technologies in the given TSV file
    and return the dictionary.seqTecDictionary
    :param tsvFile: tsv file that used for returning dictionary of {accession_id: SequenceTechnology}
    :return: sequence- sequence Technology dictionary
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


def addSeqTechToFastaFile(tsvFolder, inFastaFile, outFastaFile):
    """
    This method make a new fasta file and insert the seq technology from
    {accession_id :sequenceTechnology} dictionary that generated in the
    makeDictionaryOfSeqTechForEachFile(tsvFolder) method
    header, using accession Id
    :param outFastaFile:
    :param tsvFolder: Name of TSV folder containing all TSV files
    :param inFastaFile: Address of input Fasta File
    :return: Fasta file containing sequencing technology
    """

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
    count = 0
    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):

                accessionId = getAccessionId(line)
                if seqDictionary.__contains__(accessionId):
                    count = count + 1
                    f.write(line.strip())
                    f.write("|")
                    f.write(seqDictionary[accessionId])
                    f.write('\n')
                    isContainsSeq = True

            elif isContainsSeq:
                f.write(line)
                isContainsSeq = False

    f.close()


def findReferenceGenome(inputFastaFile):
    accessionIdMin = '1'
    minCollectionDate = datetime.now()
    year = 2020
    month = 1
    day = 1
    rGenome = ''
    with open(inputFastaFile) as infile:
        for line in infile:
            if line.__contains__('>'):
                collectionDate = line.rsplit('|')[2]
                if collectionDate.rsplit('-').__len__() >= 0:
                    year = collectionDate.rsplit('-')[0]
                    if collectionDate.rsplit('-').__len__() >= 1:
                        month = collectionDate.rsplit('-')[1]
                        if month == '00':
                            month = 1
                        if collectionDate.rsplit('-').__len__() >= 2:
                            day = collectionDate.rsplit('-')[2]
                            if day == '00':
                                day = 1
                        else:
                            day = 1
                    else:
                        month = 1
                        day = 1

                d = datetime(int(year), int(month), int(day))

                if d < minCollectionDate:
                    minCollectionDate = d
                    accessionIdMin = line.rsplit('|')[1]
                    header = line

            else:
                rGenome = line
    rGenomeFile = config['inputAddresses'].get('referenceGenome')

    with open(rGenomeFile, "w") as outRG:
        outRG.write(header)
        outRG.write(rGenome)
    print(minCollectionDate, accessionIdMin)


def main(*args):
    """
    The pipeline starts here,
    For generating the output please uncomment the different parts in the same order as following
    1- add sequence technology to fasta file
    2-
    :return:
    """
    """    for x in range(0, args.__len__()):
        if args[x] == "SA":  # statistical Analysis
            print(args[x])
            # address
            print(args[x + 1])
        elif args[x] == "PT":  # phylogenetic Tree
            print(args[x])
        elif args[x] == "GG":  # Graph genome
            print(args[x])"""

    if not os.path.isdir('files'):
        os.makedirs('files/output')
        # os.mkdir('files/output/test')
        os.mkdir('files/output/CSV')

    # input_fasta_file = config['inputAddresses'].get('input_fasta_file')
    # tsvFolder = config['inputAddresses'].get('TSVFolder')
    # outFastaFile = config['outputAddresses'].get('fullFastaFile')
    # findReferenceGenome(input_fasta_file)
    # addSeqTechToFastaFile(tsvFolder, input_fasta_file, outFastaFile)

    """
    this method call all f the pipeline.
    Bias:
    """
    # analyse_sequence_technology_bias(outFastaFile)
    # alignedFileFame = config['address'] + "aligned_" + config['address'].get('input_fasta_file')
    # parseFastaFile("", 'files/test_MSA_2.fasta', 'files/output_Test_MSA_22.fasta')
    #add_seq_techToMSAMetaData()
    # process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')

    """
    Mutation Analysis: -
    """

    # global_tree = config['inputAddresses'].get('global_tree')
    # metadata_file = config['inputAddresses'].get('metaDate')
    # mutationAnalysis(global_tree, metadata_file)

    """
    Charts:
    """
    # input_file = 'files/Msa_NoSpace_withExtraLetter.csv'
    # outputAddress = "files/BarCharts/relationBetweenTechAndLetter_Dictionary.txt"
    # DrawBarChart(input_file,outputAddress)

    """
    Graph Genome:  
    """
    # fastaFileWithSequenceTechnology = config['outputAddresses'].get('fullFastaFile')
    # fastaFileWithSequenceTechnology = config['separateFiles'].get('output_fasta_file')

    # drawGraphGenome(fastaFileWithSequenceTechnology)
    # compareToUCSCSpike()


if __name__ == '__main__':
    options = sys.argv
    main(*options)
