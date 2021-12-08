import matplotlib.pyplot as plt
import configparser


CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getReferenceGenomeList():
    referenceGenomeFile = config['inputAddresses'].get('referenceGenome')

    with open(referenceGenomeFile) as rFile:
        for line in rFile:
            if line.__contains__('>'):
                continue
            else:
                return list(line.strip())


colorList = {'A': 'red', 'C': 'green', 'G': 'blue', 'T': 'black', 'U': 'orange', 'R': 'violet', 'Y': 'gold',
             'S': 'dimgray',
             'W': 'lightcoral', 'K': 'aqua', 'M': 'palegreen', 'B': 'slategray', 'D': 'hotpink', 'H': 'tomato',
             'V': 'lime',
             'N': 'peru', '-': 'maroon', '.': 'maroon'}


def drawLine(yLists, rGenome):
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
                    plt.plot(index, nu, 'ro', color=pointColor)  # make points
            index = index + 1

        """for nu in li[0]:
            #print (nu,'   ',colorList.keys().__contains__(nu))
            if nucleotideDictLists[index].__getitem__()==nu:
                nucleotideDictLists[index].
            if colorList.__contains__(:
                pointColor = colorList[nu]
                plt.plot(index, nu, 'ro', color=pointColor)  # make points
            index=index+1
"""
        # plt.plot(xList, li[0], 'ro')  # make points

        plt.plot(xList, li[0], 'k-', color=clr)  # make lines

        # print(xList)
        # print(li)

    plt.xticks(xList, rGenome)
    yLabel = [' '] * 17
    plt.yticks(list(range(0, 16)), yLabel)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    plt.axis('off')

    plt.savefig(graphGenomeFile, bbox_inches='tight')
    plt.close()
    plt.show()


def makeY(seq, referenceGenome):
    # print(seq[0])
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
    # print('-------->', nucleotideDictLists)

    return [newLine, seq[1]]


listOfYDictionary = {}


def makeYDictionary(sequence, rGenome):
    newList = [0] * rGenome.__len__()
    count = 0
    # for r in rGenome:

    # print('-------->', listOfYDictionary.get(count), '   ', listOfYDictionary.get(count).keys().__contains__(r),
    # listOfYDictionary.get(count).get(r))
    for seq in sequence:
        r = rGenome[count]
        if listOfYDictionary.get(count) is None:
            listOfYDictionary[count] = {r: 0}
        #        print(r is seq ,'    ', r,'   ', seq)
        if r is seq:
            newList[count] = 0
        elif listOfYDictionary.get(count).__contains__(seq):
            newList[count] = listOfYDictionary.get(count).get(r)
        else:
            newList[count] = listOfYDictionary[count][seq] = listOfYDictionary[count].__len__()
        count = count + 1

    #    print("***************")
    #    print(listOfYDictionary)
    #    print(newList)
    #    print("***************")
    return newList


def getSequenceTechnology(line):
    return line.split("|")[4].strip()


nucleotideDictLists = {}

for i in range(0, getReferenceGenomeList().__len__()):
    nucleotideDictLists[i] = {getReferenceGenomeList()[i]: 0}  # add nucleotides of reference genome to the dictionary


def drawGraphGenome(inFile):
    seqList = []
    seqTech = ''
    with open(inFile) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                seqTech = getSequenceTechnology(line)
                continue
            else:
                seqList.append([list(line.strip()), seqTech])

    rGenome = getReferenceGenomeList()
    yAxis = [0] * rGenome.__len__()
    yLists = [[yAxis, '-']]

    for li in seqList:
        yAxis = makeY(li, rGenome)
        yLists.append(yAxis)
    print(yLists)
    drawLine(yLists, rGenome)

# print(yAxis)
# drawLine(yAxis)
