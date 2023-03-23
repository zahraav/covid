import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def sliceFastaFile(inputFile, outputFile, head, tail):
    """
    This method gets a fasta input file and trim every sequence from head location to tail location.
    Then saved the out put with it's header into outputAddress.
    :param inputFile: Input Fasta file
    :param outputFile: Address for saving the output fasta file
    :param head: Head location for saving the fasta file
    :param tail: Tail location for saving the fasta file
    :return:
    """
    count = 0
    with open(outputFile, "a") as output:
        with open(inputFile, 'r') as reader:
            for row in reader:
                if row.__contains__('>'):
                    output.write(row)
                else:
                    for char in row:
                        if head <= count <= tail:
                            output.write(char)
                            # seq=char
                        count += 1
                    output.write('\n')

                count = 0


def separateSeqByCount(inFile, outFileAddress, seqCount):
    """
    This method gets a fasta file, sequence count, and nucleotide count as
    input. Then print as many as sequence count of sequences from inFile,
    and each sequence, it cut from 0 to nucleotide count and print the result
    in the output fasta file.
    :param inFile: Fasta file containing all full sequences
    :param outFileAddress: Address of the output fasta file, in the end,
    the split sequences are going to print in this address.
    :param seqCount: Is the number of sequences that should be in the output fasta file.
    :return:
    """
    outFile = open(outFileAddress, "w")

    index = 0
    with open(inFile) as fileReader:
        for line in fileReader:
            if index < seqCount:
                if line.__contains__('>'):
                    outFile.write(line)
                else:
                    # outFile.write(line[0:nucleotideCount])
                    outFile.write(line)
                    outFile.write('\n')
                    index = index + 1
    outFile.close()


def separatePartOfFastaFile(inFasta, sequenceCount):
    """
    This method gets a generate a new fasta file
    :return:
    """
    outFasta = config['separateFiles'].get('output_fasta_file')
    # inFasta = config['outputAddresses'].get('fullFastaFile')
    separateSeqByCount(inFasta, outFasta, sequenceCount)


# input_file = 'files/input/msa_0206_Canada.fasta'
# savingAddress = 'files/input/msa_0206_Canada_1000to20000.fasta'
inputAddress = 'files/input/msa_0206_Canada_10000to20000.fasta'
outputAddress = 'files/input/msa_0206_canada_1000sequence_5000nucleotide.fasta'
outputAddress2 = 'files/input/msa_0206_canada_1000sequence_4000nucleotide.fasta'
sliceFastaFile(outputAddress, outputAddress2, 0, 4000)
# separateSeqByCount(outputAddress, outputAddress2, 1000)
