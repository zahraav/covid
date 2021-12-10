import matplotlib.pyplot as plt
import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getReferenceGenomeList(lengthOfCut):
    """
    This Method returns part/ whole reference Genome as a list depends on length of cut.
    :return: List containing the nucleotide list of reference genome.
    """
    referenceGenomeFile = config['inputAddresses'].get('referenceGenome')
    rGenome = ''
    with open(referenceGenomeFile) as rFile:
        for line in rFile:
            if line.__contains__('>'):
                continue
            else:
                rGenome = rGenome + line.strip()
    if lengthOfCut is not 0:
        return list(rGenome[0:lengthOfCut])
    else:
        return list(rGenome)


# Dictionary of color for points
colorList = {'A': 'red', 'C': 'green', 'G': 'blue', 'T': 'black', 'U': 'orange', 'R': 'violet', 'Y': 'gold',
             'S': 'dimgray',
             'W': 'lightcoral', 'K': 'aqua', 'M': 'palegreen', 'B': 'slategray', 'D': 'hotpink', 'H': 'tomato',
             'V': 'lime',
             'N': 'peru', '-': 'maroon', '.': 'maroon'}


def drawLine(yLists, rGenome):
    """
    This method gets lists of nucleotide and sequence technology and reference genome ,
    and draw the graph genome
    it change the color of lines depends on sequence technology
    and change the color of points depends on nucleotide. the colorList above this Method is the dictionary
    of color for points
    :param yLists: a list containing both yList and sequence technology
    :param rGenome: Reference Genome
    :return:
    """
    graphGenomeFile = config['outputAddresses'].get('graphGenome')

    f, ax = plt.subplots(1)
    xList = list(range(0, rGenome.__len__()))
    clr = 'purple'

    for li in reversed(yLists):
        if li[1] == '-':
            clr = 'red'
        elif li[1] == 'Nanopore':
            clr = 'blue'
        elif li[1] == 'Illumina':
            clr = 'green'
        elif li[1] == 'unknown':
            clr = 'purple'
        index = 0

        for nu in li[0]:

            for nucleotide, location in nucleotideDictLists[index].items():
                if nu == location:
                    pointColor = colorList.get(nucleotide)
                    plt.plot(index, nu, 'ro', color=pointColor, markersize=3)  # make points
            index = index + 1

        # plt.plot(xList, li[0], 'ro')  # make points

        plt.plot(xList, li[0], 'k-', color=clr, linewidth=1)  # make lines

    plt.xticks(xList, rGenome)
    yLabel = [' '] * 17
    plt.yticks(list(range(0, 17)), yLabel)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    plt.axis('off')

    plt.savefig(graphGenomeFile, bbox_inches='tight', dpi=300)
    plt.close()
    plt.show()


def makeY(seq, referenceGenome):
    """
    TODO: Changing the explanation!
    This method gets a line from Fasta file  and reference genome as an input
    and make a list comparing sequence and reference genome
    also it used a nucleotideDictionary list, which is list of nucleotides that are used until now
    if the current nucleotide in the location was in the previous sequences in this location ,
    then the number from the yaxis allocated to the nucleotide added to the list.
    otherwise the nucleotide is going to be added to the dictionary in the location
    of that nucleotide on the sequence.
    :param seq:
    :param referenceGenome:
    :return:
    """
    newLine = [0] * referenceGenome.__len__()
    startAt = 0

    for nu in seq[0]:
        if list(nucleotideDictLists[startAt].keys()).__contains__(nu):
            newLine[startAt] = nucleotideDictLists[startAt][nu]
        else:
            temp = nucleotideDictLists[startAt].__len__()
            nucleotideDictLists[startAt][nu] = temp

            newLine[startAt] = temp
        startAt = startAt + 1

    return [newLine, seq[1]]

# Dictionary containing the lications and the dictionary of nucleotide on that location
# example
# {0:{'A':0,'C':1},1:{'C':0},...}
listOfYDictionary = {}


def makeYDictionary(sequence, rGenome):
    """
    This Method get a sequence and return a list which is the y axis for graph genome
    :param sequence:
    :param rGenome:
    :return:
    """
    newList = [0] * rGenome.__len__()
    count = 0
    for seq in sequence:
        r = rGenome[count]
        if listOfYDictionary.get(count) is None:
            listOfYDictionary[count] = {r: 0}
        if r is seq:
            newList[count] = 0
        elif listOfYDictionary.get(count).__contains__(seq):
            newList[count] = listOfYDictionary.get(count).get(r)
        else:
            newList[count] = listOfYDictionary[count][seq] = listOfYDictionary[count].__len__()
        count = count + 1

    return newList


def getSequenceTechnology(header):
    """
    This method get a header line of a fasta file and returns the sequence technology from the header.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    return header.split("|")[4].strip()


nucleotideDictLists = {}
nucleotideCut = 1000

for i in range(0, getReferenceGenomeList(1000).__len__()):
    # add nucleotides of reference genome to the dictionary
    nucleotideDictLists[i] = {getReferenceGenomeList(1000)[i]: 0}


def drawGraphGenome(inFile):
    """
    This Method gets a fasta file as input and makes a graph genome for the fasta file.
    :param inFile: Input fasta file
    :return:
    """
    # Two dimention list containing the sequences and sequence technology for every sequence
    # [[Sequence1 , SequenceTechnology],[Sequence2,sequenceTechnology][...,...]
    # sample:
    # [['ACGTAAAG...', 'Nanopore'],['ACGTAAG...', 'Illumina],[..]]
    seqList = []
    seqTech = ''
    with open(inFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                seqTech = getSequenceTechnology(line)
                continue
            else:
                #
                seqList.append([list(line.strip()), seqTech])

    rGenome = getReferenceGenomeList()
    yAxis = [0] * rGenome.__len__()
    yLists = [[yAxis, '-']]

    for li in seqList:
        yAxis = makeY(li, rGenome)
        yLists.append(yAxis)
    drawLine(yLists, rGenome)

# drawLine(yAxis)
