import numpy as np
import matplotlib.pyplot as plt

NanoporeCountDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                           'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                           'N': 0, '-': 0, '.': 0}

IlluminaCountDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                           'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                           'N': 0, '-': 0, '.': 0}


def addToDictionary(line):
    # print(line)
    if not ['A', 'C', 'G', 'T'].__contains__(line[5]):
        NanoporeCountDictionary[line[5]] = NanoporeCountDictionary[line[5]] + 1
    if not ['A', 'C', 'G', 'T'].__contains__(line[10]):
        IlluminaCountDictionary[line[10]] = IlluminaCountDictionary[line[10]] + 1


def readFile(inFile):
    """
    This method read the input fasta file and generate a dictionary of nucleotides
    :param inFile:
    :return:
    """
    with open(inFile) as f:
        lines = f.readlines()
        for line in lines:
            if str.isdigit(line[0]):
                addToDictionary(line.strip().split(","))


def plotBar():
    # create plot
    _, ax = plt.subplots()
    index = np.arange(NanoporeCountDictionary.__len__())
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, NanoporeCountDictionary.values(), bar_width, alpha=opacity, color='b', label='Nanopore')
    plt.bar(index + bar_width, IlluminaCountDictionary.values(), bar_width, alpha=opacity,
            color='g', label='Illumina')

    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title('Technology Letter ')
    plt.xticks(index + bar_width, NanoporeCountDictionary.keys())
    plt.legend()

    plt.tight_layout()
    BarOutputAddress = 'files/output/BarCharts/Letter_technology.png'
    plt.savefig(BarOutputAddress, dpi=800)

    plt.show()


def BarChart(txtFile):
    readFile(txtFile)
    plotBar()


BarChart('files/output/test/test.txt')
