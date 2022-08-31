import matplotlib.pyplot as plt
import os
import configparser

from graphGenome.GenerateSpikeProtein import generateSpikes
from graphGenome.compareSpikeToUCSCSpike import compareToUCSCSpike

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()

graphHeight = 8000
graphWidth = 3600


def getReferenceGenome(lengthOfCut):
    """
    This method returns part/ whole reference Genome depending on the cut length.
    :return: part/whole reference Genome
    """
    # referenceGenomeFile = config['inputAddresses'].get('referenceGenome')
    referenceGenomeFile = config['inputAddresses'].get('spikeReferenceGenome')
    rGenome = ''
    with open(referenceGenomeFile) as rFile:
        for line in rFile:
            if line.__contains__('>'):
                continue
            else:
                rGenome = rGenome + line.strip()
    if lengthOfCut != '-':
        return rGenome[0:lengthOfCut]
    else:
        return rGenome


def getSequenceTechnology(header):
    """
    This method gets a fasta file header line and returns the sequencing technology from the header.
    If the header does not have the sequencing technology, it returns '-'.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    if header.split("|").__len__() < 4:
        return '-'
    else:
        return header.split("|")[4].strip()


def drawGraphGenome(inFile):
    """
    This Method gets a fasta file as input and makes a graph genome for the fasta file
    :param inFile: Multiple sequence alignment(MSA) file
    :return:
    """

    # making a folder for graphGenome if one is not available in the files/output folder
    if not os.path.isdir('files/output/GraphGenome'):
        os.mkdir('files/output/GraphGenome')
        os.mkdir('files/output/GraphGenome/spike')

    # use spikes instead of whole genome!
    spikeFile = generateSpikes(inFile)
    spikeFile = config['outputAddresses'].get('spikeFastaFile')
    # set to '-' if you want whole rGenome
    nucleotideCutLength = '-'  # '-'  #1000
    # numberOfSeq = 100  # '-'  #100
    interval = 4
    distanceOfLinesInGraph = 900
    rGenome = getReferenceGenome(nucleotideCutLength)

    compareToUCSCSpike()
    """
    A list containing the sequences and sequencing technology for every sequence
    [[Sequence1 , SequenceTechnology],[Sequence2,sequenceTechnology][...,...]
    sample:
    [['ACGTAAAG...', 'Nanopore'],['ACGTAAG...', 'Illumina],[..]]
    at first, we initialize it with the reference genome
    so that when we want to draw the genome, we have access to sequencing technology too.
    """
    sequenceList = [[rGenome, '-']]

    """
    Reading the code and sequencing technology from inFile and make the sequenceList in the following code.
    """
    seqTech = ''
    # with open(inFile) as mainFastaFile:
    with open(spikeFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                seqTech = getSequenceTechnology(line)
                continue
            else:
                sequenceList.append((line.strip(), seqTech))

    """
    This dictionary contains a dictionary for every location in the sequence.
    It keeps the nucleotide that was seen in the previous sequences and the order of seeing the nucleotide in that 
    location. for example, if in location 20 of the first sequence we see nucleotide 'A',
    then in the 20sth dictionary in this dictionary, we add an 'A', and because it is the first sequence,
    that means the order for 'A' is 0, so we add {'A':0}  
    example
    {0:{'A':0,'C':1},1:{'C':0},...}
    """
    nucleotideDictLists = {}
    for i in range(0, rGenome.__len__()):
        # add nucleotides of reference genome to the dictionary
        nucleotideDictLists[i] = {rGenome[i]: 0}

    """
    the repeatList keeps the number of repeats for every nucleotide in a location, 
    if the number of nucleotide that we saw before current nucleotide is equal or greater to 
    interval, the repeat list on that location for the nucleotide is not increase by 1 
    other wise it will increase by 1. 
    so that in the location that we have similar nucleotide equal or greater than interval 
    there is one line  
    """
    # This dictionary counts the number of repeat for every nucleotide in a location. Then the numbers of
    # this dictionary is going to be added to a list- one nucleotide for each dictionary.
    # So that we can add to the pixels when there is a repeat on a location.
    nucleotideRepetitionDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                                      'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                                      'N': 0, '-': 0, '.': 0}

    # add reference genome to repeatList
    repeatList = [{} for _ in range(rGenome.__len__())]
    for z in repeatList:
        z.update(nucleotideRepetitionDictionary)
    tempCount = 0
    for nu in rGenome:
        repeatList[tempCount][nu] = 1
        tempCount = tempCount + 1
    # Call the processSequence function for generating yAxis for every sequence and draw graph genome.
    processSequences(sequenceList, rGenome, repeatList, nucleotideDictLists, interval, distanceOfLinesInGraph)


def processSequences(seqList, rGenome, repetitionList, nucleotideDictLists, interval, distanceOfLinesInGraph):
    """
    This method takes list of sequences and process the sequences and make a yAxis for every sequence
    then by calling the drawGraph method add the line for that sequence to the chart.
    :param distanceOfLinesInGraph:
    :param interval:
    :param seqList: List of sequences
    :param rGenome: Reference genome
    :param repetitionList:
    :param nucleotideDictLists:
    :return:
    """
    yAxes = []

    # information that is needed for drawing the graph,
    # img = Image.new("RGB", (2000, 2000), (255, 255, 255))

    # img = Image.new("RGB", (graphHeight, graphWidth), (255, 255, 255))

    # draw = ImageDraw.Draw(img)

    graphGenomeAddress = config['outputAddresses'].get('graphGenome')
    if os.path.exists(graphGenomeAddress):
        print('Existing graphGenome removed successfully!')
        os.remove(graphGenomeAddress)

    # X axis is the same for all sequences, it started from 0 to the length of  reference genome

    xList = [i * 10 for i in list(range(0, rGenome.__len__()))]

    # segment List is a list that contains nucleotide that are similar between the current sequence and the previous
    # sequence that we are comparing
    segmentList = []

    # The previous set keeps the sequence from the previous sequences; we use the set for
    # previous sequences to not have repetitive sequences.
    # in the previous set if the nucleotides in the interval are equal to thc
    # When we want to add a sequence to the previous list, we check if some nucleotides are
    # equal or greater than the interval similar to the sequence that we are checking, then
    # we put '*' instead of those nucleotides.
    # We do not need to check those parts with other nucleotides because those parts of the
    # sequence are already available on the previous list.
    previousSet = set()
    newLine = rGenome
    sameNucleotideDistance = 10
    count = 0
    yAxis = [0] * rGenome.__len__()
    # In these for loops, we compare every nucleotide in sequences in the sequence list
    # with all sequences compared with the previous ones.
    # Then depending on the equality of nucleotide and previous nucleotide, we decide
    # whether to increase the repetitive list for the nucleotide on this location and add
    # the nucleotide to the nucleotide dictionary.
    # Also, the y axis for every sequence in the sequence list is generated too. Then it
    # will be passed to the drawGraph method for drawing the line related to this sequence.
    for seq in seqList:
        for pre in previousSet.copy():
            for i in range(0, pre.__len__()):  # iterate on nucleotides
                # print(seq[0][i-1] , i, seq[0].__len__(),rGenome.__len__())

                nucleotide = seq[0][i]
                checkNucleotide = pre[i]
                # check if the nucleotide in previousList are equal to the nucleotide in the sequenceList
                # in i location,
                # - if they are equal and it's not the last nucleotide of the sequence add the nucleotide to
                #   the segment list , which contains the similar , and if it is the last nucleotide add the
                #   to the newline
                # - else if they're not equal add the segment to the newline and clear the segment and
                #   increase the repeatList for the nucleotides in the segment

                if nucleotide == checkNucleotide:
                    count = count + 1
                    segmentList.append(nucleotide)
                    # last nucleotide in the sequence and the count is less than interval:
                    if i == pre.__len__() - 1 and count < interval:
                        segSize = segmentList.__len__()
                        for nu in segmentList:
                            newLine = newLine + nu
                            repetitionList[i - segSize + 1][nu] = repetitionList[i - segSize + 1][nu] + 1
                            yAxis[i - segSize + 1] = nucleotideDictLists[i - segSize + 1][nu] * distanceOfLinesInGraph \
                                + repetitionList[i - segSize + 1][nu] * sameNucleotideDistance
                            segSize = segSize - 1
                        segmentList.clear()
                        count = 0
                        continue
                    # last element in sequence and count is greater and equal to interval:
                    elif i == pre.__len__() - 1 and count >= interval:
                        segSize = segmentList.__len__()
                        for nu in segmentList:
                            newLine = newLine + '*'
                            yAxis[i - segSize + 1] = nucleotideDictLists[i - segSize + 1][nu] * distanceOfLinesInGraph
                            segSize = segSize - 1
                        segmentList.clear()
                        count = 0
                        continue

                elif nucleotide != checkNucleotide:
                    segSize = segmentList.__len__()
                    # The count is bigger or equal to interval and the current nucleotides are not equal:
                    if count >= interval:
                        for nu in segmentList:
                            newLine = newLine + '*'
                            yAxis[i - segSize] = nucleotideDictLists[i - segSize][nu] * distanceOfLinesInGraph
                            # yAxis[i - segSize] = positionList[i - segSize][nu]
                            segSize = segSize - 1
                        segmentList.clear()

                    # newLine = newLine + nucleotide

                    # if count is less than interval and nucleotides are not equal:
                    else:
                        for nu in segmentList:
                            newLine = newLine + nu
                            repetitionList[i - segSize][nu] = repetitionList[i - segSize][nu] + 1

                            yAxis[i - segSize] = nucleotideDictLists[i - segSize][nu] * distanceOfLinesInGraph \
                                + repetitionList[i - segSize][nu] * sameNucleotideDistance
                            segSize = segSize - 1
                        segmentList.clear()
                    newLine = newLine + nucleotide
                    if not nucleotideDictLists[i].__contains__(nucleotide):
                        nucleotideDictLists[i][nucleotide] = nucleotideDictLists[i].__len__()

                    repetitionList[i][nucleotide] = repetitionList[i][nucleotide] + 1
                    yAxis[i] = nucleotideDictLists[i][nucleotide] * distanceOfLinesInGraph \
                        + repetitionList[i][nucleotide]
                    segmentList.clear()
                    count = 0

            # adding the sequence to previous set
            previousSet.add(newLine)
            # send the y axis to drawing the line in the graph genome
            yAxes.append([yAxis, seq[1]])
            drawGraph(yAxis, seq[1], xList, graphGenomeAddress)
            yAxis = [0] * rGenome.__len__()

            newLine = ''
            segmentList.clear()
            count = 0
        newLine = ''

        # If the previous set is empty, we add the first sequence of sequence List to the previous
        # sequence and add the nucleotide of the first sequence into the repetition list and
        # nucleotide dictionary.
        if previousSet.__len__() == 0:
            previousSet.add(seq[0])
            for j in range(0, seq[0].__len__()):
                if not nucleotideDictLists[j].__contains__(seq[0][j]):
                    repetitionList[j][seq[0][j]] = repetitionList[j][seq[0][j]] + 1
                    nucleotideDictLists[j][seq[0][j]] = repetitionList[j][seq[0][j]]
        # remove the sequences that are all '*'
        for check in previousSet.copy():
            if check == '*' * check.__len__():
                previousSet.remove(check)

    graphGenomeYList = []
    for xxx in range(0, rGenome.__len__()):
        graphGenomeYList.append(nucleotideDictLists[xxx][rGenome[xxx]])
    drawGraph(graphGenomeYList, '-', xList, graphGenomeAddress)


def drawGraph(yList, seqTechnology, xList, graphGenomeAddress):
    """
    This method take yAxis and draw a line for that axis on the graph.
    color of the line depends on the sequencing technology that is used.
    :param graphGenomeAddress:
    :param yList: yList belongs to the sequence for drawing the line
    :param seqTechnology: sequencing technology for that sequence
    :param xList: A list started from 0 to length of reference genome
    :return:
    """
    newXList = [element * 100 for element in xList]

    plt.plot(newXList, yList, color=getColor(seqTechnology), linewidth=0.2)
    plt.axis('off')
    plt.savefig(graphGenomeAddress, dpi=1200)


def getColor(seqTechnology):
    """
    This method check the sequencing technology and return a specific color for Illumina and Nanopore.
    :param seqTechnology:
    :return:
    """

    if seqTechnology == '-':
        return 'yellow'
    elif seqTechnology == 'Nanopore':
        return 'blue'
    elif seqTechnology == 'Illumina':
        return 'green'
    else:
        return 'purple'
