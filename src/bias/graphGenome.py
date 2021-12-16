import os

import matplotlib.pyplot as plt
import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getSequenceTechnology(header):
    """
    This method get a header line of a fasta file and returns the sequence technology from the header.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    return header.split("|")[4].strip()


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
    if lengthOfCut != 0:
        return list(rGenome[0:lengthOfCut])
    else:
        return list(rGenome)


# Dictionary of color for points
colorList = {'A': 'red', 'C': 'green', 'G': 'blue', 'T': 'black', 'U': 'orange', 'R': 'violet', 'Y': 'gold',
             'S': 'dimgray',
             'W': 'lightcoral', 'K': 'aqua', 'M': 'palegreen', 'B': 'slategray', 'D': 'hotpink', 'H': 'tomato',
             'V': 'lime',
             'N': 'peru', '-': 'maroon', '.': 'maroon'}


def drawLine(yLists, rGenome, height):
    """
    This method gets lists of nucleotide and sequence technology and reference genome ,
    and draw the graph genome
    it change the color of lines depends on sequence technology
    and change the color of points depends on nucleotide. the colorList above this Method is the dictionary
    of color for points
    :param height:
    :param yLists: a list containing both yList and sequence technology
    :param rGenome: Reference Genome
    :return:
    """
    graphGenomeFile = config['outputAddresses'].get('graphGenome')

    f, ax = plt.subplots(1)
    xList = list(range(0, rGenome.__len__()))
    clr = 'purple'
    # print(nucleotideDictLists)
    for li in reversed(yLists):
        # print(li[0])
        if li[1] == '-':
            clr = 'red'
        elif li[1] == 'Nanopore':
            clr = 'blue'
        elif li[1] == 'Illumina':
            clr = 'green'
        elif li[1] == 'unknown':
            clr = 'purple'

        """
        index = 0
        for nu in li[0]:

            for nucleotide, location in nucleotideDictLists[index].items():
                if nu == location:
                    pointColor = colorList.get(nucleotide)
                    plt.plot(index, nu, 'ro', color=pointColor, markersize=3)  # make points
            index = index + 1
"""
        # plt.plot(xList, li[0], 'ro')  # make points

        # tempYList = [element * numberOfSeq for element in li[0]]
        # sum_list = [a + b for a, b in zip(tempYList, repeatLine)]
        # plt.plot(xList, tempYList, 'k-', color=clr, linewidth=1)  # make lines

        plt.plot(xList, li[0], 'k-', color=clr, linewidth=1)  # make lines

    plt.xticks(xList, rGenome)
    yLabel = [' '] * 17 * height
    plt.yticks(list(range(0, 17 * height)), yLabel)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    plt.axis('off')
    plt.hsv()
    plt.savefig(graphGenomeFile, bbox_inches='tight', dpi=5000)
    plt.close()
    plt.show()


def makeY(seq, referenceGenome, height, repeatList):
    """
    TODO: Changing the explanation!
    This method gets a line from Fasta file  and reference genome as an input
    and make a list comparing sequence and reference genome
    also it used a nucleotideDictionary list, which is list of nucleotides that are used until now
    if the current nucleotide in the location was in the previous sequences in this location ,
    then the number from the yaxis allocated to the nucleotide added to the list.
    otherwise the nucleotide is going to be added to the dictionary in the location
    of that nucleotide on the sequence.
    :param height:
    :param seq:
    :param referenceGenome:
    :return:
    """
    newLine = [0] * referenceGenome.__len__()
    startAt = 0
    for nu in seq[0]:
        if list(nucleotideDictLists[startAt].keys()).__contains__(nu):
            # newLine[startAt] = nucleotideDictLists[startAt][nu]
            newLine[startAt] = repeatList[startAt][nu] + nucleotideDictLists[startAt][nu] * height
            repeatList[startAt][nu] = repeatList[startAt][nu] + 1
            # newLine[startAt] = repeatDictionary[startAt][nu] + nucleotideDictLists[startAt][nu] * height
            # repeatDictionary[startAt][nu] = repeatDictionary[startAt][nu] + 1

        else:
            # temp = nucleotideDictLists[startAt].__len__()
            # nucleotideDictLists[startAt][nu] = temp
            # newLine[startAt] = temp

            temp = nucleotideDictLists[startAt].__len__()
            nucleotideDictLists[startAt][nu] = temp
            # print('--   ',repeatList[startAt])
            newLine[startAt] = temp * height + repeatList[startAt][nu]
            # print(newLine[startAt], '   ', startAt, newLine,'    ',nucleotideDictLists[startAt])
            repeatList[startAt][nu] = 1
        startAt = startAt + 1
    # print(repeatList)
    # print('\n')
    return [newLine, seq[1]], repeatList


# Dictionary containing the locations and the dictionary of nucleotide on that location
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


nucleotideDictLists = {}
nucleotideCut = 1000
numberOfSeq = 100
height = 100000
for i in range(0, getReferenceGenomeList(nucleotideCut).__len__()):
    # add nucleotides of reference genome to the dictionary
    nucleotideDictLists[i] = {getReferenceGenomeList(nucleotideCut)[i]: 0}

# This dictionary counts the number of repeat for every nucleotide in a location. Then the numbers of
# this dictionary is going to be added to a list- one nucleotide for each dictionary.
# So that we can add to the pixels when there is a repeat on a location.
repeatNDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                     'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                     'N': 0, '-': 0, '.': 0}


def drawGraphGenome(inFile):
    """
    This Method gets a fasta file as input and makes a graph genome for the fasta file.
    :param inFile: Input fasta file
    :return:
    """
    # Two dimension list containing the sequences and sequence technology for every sequence
    # [[Sequence1 , SequenceTechnology],[Sequence2,sequenceTechnology][...,...]
    # sample:
    # [['ACGTAAAG...', 'Nanopore'],['ACGTAAG...', 'Illumina],[..]]
    os.mkdir('files/output/GraphGenome')

    seqList = []
    seqTech = ''
    with open(inFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                seqTech = getSequenceTechnology(line)
                continue
            else:
                seqList.append([list(line.strip()), seqTech])

    rGenome = getReferenceGenomeList(nucleotideCut)
    yAxis = [0] * rGenome.__len__()
    yLists = [[yAxis, '-']]

    repeatList = [{} for _ in range(nucleotideCut)]
    for z in repeatList:
        z.update(repeatNDictionary)
    # repeatList = [repeatNDictionary] * nucleotideCut

    # print(repeatList)

    for li in seqList:
        yAxis, repeatList = makeY(li, rGenome, height, repeatList)

        yLists.append(yAxis)
    drawLine(yLists, rGenome, height, repeatList)

# drawLine(yAxis)
