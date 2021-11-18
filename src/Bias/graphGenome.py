import configparser
import matplotlib.pyplot as plt

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


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


def getSequenceTechnology(header):
    """
    This method get a header line of a fasta file and returns the sequence technology from the header.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    return header.split('|')[4].strip()


def makeLinePlot(inFastaFile):
    graphGenome = config['outputAddresses'].get('graphGenome')

    isFirst = True
    count = 0
    yList = []

    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):
                accessionId = getAccessionId(line)
                seqTechnology = getSequenceTechnology(line)
            else:
                xList = list(line.strip())
                if isFirst:
                    for i in range(1, xList.__len__() + 1):
                        yList.append(str(i))
                    isFirst = False

                if seqTechnology == 'Illumina':
                    lineColor = "blue"
                elif seqTechnology == 'Nanopore':
                    lineColor = "red"

                plt.plot(yList, xList, label=str(accessionId), color=lineColor)
                count = count + 1

    plt.savefig(graphGenome)
    plt.close()


def makeGraphGenome(FastaFile):
    makeLinePlot(FastaFile)
