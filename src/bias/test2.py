repeatNDictionary = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'U': 0, 'R': 0, 'Y': 0, 'S': 0,
                     'W': 0, 'K': 0, 'M': 0, 'B': 0, 'D': 0, 'H': 0, 'V': 0,
                     'N': 0, '-': 0, '.': 0}


def drawGraphGenome():
    x = "GGACA"
    y = "GGATC"
    z = "TGCTC"

    rGenome = "GGACG"
    print('rGenome:  ',rGenome)
    sequenceList = [rGenome]
    sequenceList.extend([x, y, z])

    repeatList = [{} for _ in range(rGenome.__len__())]
    for tempList in repeatList:
        tempList.update(repeatNDictionary)
    print('sequenceList:  ', sequenceList)

    generateYaxis(sequenceList, rGenome, 3, repeatList)


def generateYaxis(seqList, rGenome, threshold, repeatList):
    count = 0
    segmentList = []

    notMatched = ''
    print('--->', seqList)
    newLine = []
    yAxis = []
    for s in range(0, seqList.__len__()):
        # for seq in seqList:
        print('seq:  ', seqList[s])

        for i in range(0, seqList[s].__len__()):
            nucleotide = seqList[s][i]
            if nucleotide == rGenome[i]:
                count = count + 1
                segmentList.append(nucleotide)
            elif nucleotide != rGenome[i]:
                count = 0
                notMatched = notMatched + ''.join(segmentList) + nucleotide
                newLine.extend(segmentList)
                newLine.append(nucleotide)
                segmentList.clear()
                for nu in segmentList:
                    repeatList[i][nu] = repeatList[i][nu] + 1
                repeatList[i][nucleotide] = repeatList[i][nucleotide] + 1

            if count >= threshold:
                newLine.extend(segmentList)
                segmentList.clear()

        getYAxis(newLine, repeatList)
        print(repeatList)
        print('newLine:  ', newLine)
        newLine.clear()
        count = 0


def getYAxis(newLine, repeatList):
    yAxis = []
    print('------>', newLine)
    for i in range(0, newLine.__len__()):
        yAxis.append(repeatList[i][newLine[i]])
    print(yAxis)


"""def checkThreshold(threshold):
    flag = True
    count = 0
    listOfPoints = []
    for seq in seqlist:
        for p in parsedList:
            for i in range(0, seq.__len__()):
                if seq[i] == p[i]:
                    count = count + 1
                    listOfPoints.append(x[i])
                if x[i] != y[i]:
                    count = 0
                    # drawLines()
                    # print('x[i]:', listOfPoints, " -- ",x[i])
                    listOfPoints.clear()

                if count == threshold:
                    # drawOneLine()

                    # print(listOfPoints)
                    listOfPoints.clear()
"""

drawGraphGenome()
