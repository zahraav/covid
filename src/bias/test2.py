import os
from PIL import Image, ImageDraw

import configparser

CONFIG_FILE = r'config/config.cfg'

nucleotideCut = 1000  # '-'  #1000
numberOfSeq = 100  # '-'  #100
height = 250


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()

# This dictionary counts the number of repeat for every nucleotide in a location. Then the numbers of
# this dictionary is going to be added to a list- one nucleotide for each dictionary.
# So that we can add to the pixels when there is a repeat on a location.
repeatNDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                     'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                     'N': 0, '-': 0, '.': 0}

# Dictionary containing the locations and the dictionary of nucleotide on that location
# example
# {0:{'A':0,'C':1},1:{'C':0},...}
#listOfYDictionary = {}


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
    if lengthOfCut != '-':
        return rGenome[0:lengthOfCut]
    else:
        return rGenome



nucleotideDictLists = {}
for i in range(0, getReferenceGenomeList(nucleotideCut).__len__()):
    # add nucleotides of reference genome to the dictionary
    nucleotideDictLists[i] = {getReferenceGenomeList(nucleotideCut)[i]: 0}

def getSequenceTechnology(header):
    """
    This method get a header line of a fasta file and returns the sequence technology from the header.
    :param header: A header line of a fasta file
    :return: Sequence Technology
    """
    if header.split("|").__len__() < 4:
        return '-'
    else:
        return header.split("|")[4].strip()


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
    if not os.path.isdir('files/output/GraphGenome'):
        os.mkdir('files/output/GraphGenome')

    # set to '-' if you want whole rGenome
    rGenome = getReferenceGenomeList(nucleotideCut)
    threshold=100
    sequenceList = [[rGenome, '-']]
    seqTech = ''
    with open(inFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                seqTech = getSequenceTechnology(line)
                continue
            else:
                sequenceList.append((line.strip(), seqTech))

    repeatList = [{} for _ in range(rGenome.__len__())]
    for z in repeatList:
        z.update(repeatNDictionary)

    generateYaxis(sequenceList, rGenome, threshold, repeatList)


def generateYaxis(seqList, rGenome, threshold, positionList):
    img = Image.new("RGB", (2200, 2200), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    xList = list(range(0, rGenome.__len__()))
    segmentList = []

    previousSet = set()
    newLine = rGenome

    count = 0
    yAxis = [0] * rGenome.__len__()
    nucleotideCount = [0] * rGenome.__len__()
    for seq in seqList:

        for pre in previousSet.copy():
            for i in range(0, pre.__len__()):  # iterate on nucleotides
                nucleotide = seq[0][i]
                checkNucleotide = pre[i]
                # check if the nucleotide in previousList are equal to the nucleotide in the sequenceList
                # in i location,
                # - if they are equal and it's not the last nucleotide of the sequence add the nucleotide to
                #   the segment list , which contains the similar , and if it is the last nucleotide add the
                #   to the newline
                # - else if they're not equal add the segment to the newline and clear the segment and
                #   increase the repeatList for the nucleotides in the segment
                if checkNucleotide != '*':
                    if nucleotide == checkNucleotide:
                        count = count + 1
                        segmentList.append(nucleotide)
                        # last nucleotide in the sequence and the count is less than threshold:
                        if i == pre.__len__() - 1 and count < threshold:
                            segSize = segmentList.__len__()
                            for nu in segmentList:
                                newLine = newLine + nu
                                if positionList[i - segSize][nucleotide] != 0:
                                    yAxis[i - segSize] = positionList[i - segSize][nu]
                                else:
                                    nucleotideCount[i - segSize] = nucleotideCount[i - segSize] + 1
                                    yAxis[i - segSize] = positionList[i - segSize][nu] = nucleotideCount[i - segSize]

                            segmentList.clear()
                            count = 0
                            continue
                        # last element in sequence and count is greater and equal to threshold:
                        elif i == pre.__len__() - 1 and count >= threshold:
                            segSize = segmentList.__len__()
                            for nu in segmentList:
                                newLine = newLine + '*'
                                yAxis[i - segSize] = positionList[i - segSize][nu]
                                segSize = segSize + 1
                            segmentList.clear()
                            count = 0
                            continue

                    elif nucleotide != checkNucleotide:
                        # The count is bigger or equal to threshold and the current nucleotides are not equal:
                        if count >= threshold:
                            segSize = segmentList.__len__()
                            for nu in segmentList:
                                newLine = newLine + '*'
                                yAxis[i - segSize] = positionList[i - segSize][nu]
                                segSize = segSize + 1

                            newLine = newLine + nucleotide
                            if positionList[i][nucleotide] != 0:
                                yAxis[i] = positionList[i][nucleotide]
                            else:
                                nucleotideCount[i] = nucleotideCount[i] + 1
                                yAxis[i] = positionList[i][nucleotide] = nucleotideCount[i]
                        # if count is less than threshold and nucleotides are not equal:
                        else:
                            segSize = segmentList.__len__()
                            for nu in segmentList:
                                newLine = newLine + nu
                                yAxis[i - segSize] = positionList[i - segSize][nu]
                                segSize = segSize + 1

                            if positionList[i][nucleotide] != 0:
                                yAxis[i] = positionList[i][nucleotide]
                            else:
                                nucleotideCount[i] = nucleotideCount[i] + 1
                                yAxis[i] = positionList[i][nucleotide] = nucleotideCount[i]

                            newLine = newLine + nucleotide
                        segmentList.clear()
                        count = 0

                    # After checking the equality, we check if the similar count is greater or equal to the threshold
                    # if it is we add the segment to the new line and don't change the repeat list
                    # if count >= threshold:
                    # if count >= threshold:
                    #    print('cant believe')
                    #    newLine.extend(segmentList)
                    #    segmentList.clear()
                else:
                    newLine = newLine + '*'
                    count = 0
            previousSet.add(newLine)
            drawGraph(yAxis, seq[1], draw, xList)
            yAxis = [0] * rGenome.__len__()

            newLine = ''
            segmentList.clear()
            count = 0
        newLine = ''
        if previousSet.__len__() == 0:
            previousSet.add(seq[0])

        # remove the sequences that are all '*'
        for check in previousSet.copy():
            if check == '*' * check.__len__():
                previousSet.remove(check)

    img.save("files/FullGraphGenome43.png", "PNG")


def drawGraph(yList, seqTechnology, draw, xList):
    """
    This method
    :param yList:
    :param seqTechnology:
    :param draw:
    :param xList:
    :return:
    """
    clr = getColor(seqTechnology)
    newYList = [element * 100 for element in yList]
    pointsList = list(zip(xList, newYList))
    draw.line(pointsList, fill=clr, width=1)


# img.save("files/FullGraphGenome.png", "PNG")


def getColor(seqTechnology):
    if seqTechnology == '-':
        return 'red'
    elif seqTechnology == 'Nanopore':
        return 'blue'
    elif seqTechnology == 'Illumina':
        return 'green'
    else:
        return 'purple'
