import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def separateSeqByCount(inFile, outFileAddress, seqCount, nucleotideCount):
    """
    This method gets a fasta file, sequence count, and nucleotide count as
    input. Then print as many as sequence count of sequences from inFile,
    and each sequence, it cut from 0 to nucleotide count and print the result
    in the output fasta file.
    :param inFile: Fasta file containing all full sequences
    :param outFileAddress: Address of the output fasta file, in the end,
    the split sequences are going to print in this address.
    :param seqCount: Is the number of sequences that should be in the output fasta file.
    :param nucleotideCount: Is the number of nucleotides that every sequence should split to that count.
    :return:
    """
    outFile = open(outFileAddress, "w")

    index = 0
    with open(inFile) as inputFile:

        for line in inputFile:
            if index < seqCount:
                if line.__contains__('>'):
                    outFile.write(line)
                else:
                    outFile.write(line[0:nucleotideCount])
                    outFile.write('\n')
                    index = index + 1
    outFile.close()


def separatePartOfFastaFile(inFasta, sequenceCount, nucleotideCount):
    """

    :return:
    """
    outFasta = config['separateFiles'].get('outputFastaFile')
    inFasta = config['outputAddresses'].get('fullFastaFile')
    separateSeqByCount(inFasta, outFasta, 100, 1000)
