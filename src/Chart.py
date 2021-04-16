import csv
import matplotlib.pyplot as plt
import numpy as np

from utilities.ReadAndWrite import saveSimpleDictionary, saveToCsv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    fieldNames = ['id', 'reference', 'seq', 'date', 'location', 'technology', 'index']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)


def returnColumnDictionary(inputAddress, columnNum):
    # number of column for letters can be used when counting a sequence for multiple times is not important
    columnDict = {}
    isFirstRow = True
    with open(inputAddress) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[columnNum]
            if item in columnDict.keys():
                columnDict[item] = columnDict[item] + 1
            else:
                columnDict[item] = 1
    return columnDict


def returnDictionaryById(inputFileAddress, columnNum, initializedDictionary):
    idList = []
    isFirstRow = True
    with open(inputFileAddress) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            seqId = row[0]
            if seqId not in idList:  # we didn't see id before
                idList.append(seqId)
                temp = row[columnNum]
                if temp in initializedDictionary.keys():
                    initializedDictionary[temp] = initializedDictionary[temp] + 1
    return initializedDictionary


def returnDictionaryByTechnologyLetter(inputAddress):
    # number of column for letters can be used when counting a sequence for multiple times is not important
    columnDict = {}
    isFirstRow = True
    with open(inputAddress) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            letter = row[5]  # letter
            tech = row[3]
            if tech == 'Illumina' or tech == 'Nanopore':
                if letter in columnDict.keys():
                    columnDict[letter][tech] = columnDict[letter][tech] + 1
                else:
                    columnDict[letter] = {'Nanopore': 0, 'Illumina': 0}
                    columnDict[letter][tech] = columnDict[letter][tech] + 1
    return columnDict


def barChart(columnDict, columnNumber):
    """
    plt.bar(xAxis,yAxis)
    plt.title('title name')
    plt.xLabel('xAxis name')
    plt.yLabel('yAxis name')
    plt.show()
"""

    yAxis = []
    xAxis = []
    BarOutputAddress = ''
    if columnNumber == 0:  # id
        BarOutputAddress = 'files/BarCharts/idBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('Ids')
        plt.ylabel('Count')

    elif columnNumber == 3:  # Technology
        BarOutputAddress = 'files/BarCharts/technologyBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('technology')
        plt.ylabel('Count')

    elif columnNumber == 4:  # indices
        BarOutputAddress = 'files/BarCharts/indicesBar_2.png'
        for elem in columnDict.keys():
            if columnDict[elem] >= 200:
                yAxis.append(columnDict[elem])
                xAxis.append(elem)

        plt.xlabel('indices')
        plt.ylabel('Count')

    elif columnNumber == 5:  # letter
        BarOutputAddress = 'files/BarCharts/LetterBar_2.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('Letter')
        plt.ylabel('Count')

    plt.bar(xAxis, yAxis)
    plt.savefig(BarOutputAddress, dpi=400)
    plt.show()


def simpleBars(inputfile):
    columnNumber = 0  # id
    # columnNumber=1 # date
    # columnNumber=2 # location
    # columnNumber = 3  # technology
    # columnNumber = 4  # index
    # columnNumber = 5 # Letter

    columnDictionary = {}
    if columnNumber == 0 or columnNumber == 4 or columnNumber == 5:
        columnDictionary = returnColumnDictionary(inputFile, columnNumber)
    elif columnNumber == 3:
        techDictionary = {'Nanopore': 0, 'Illumina': 0}
        columnDictionary = returnDictionaryById(inputFile, columnNumber, techDictionary)

    savingAddress = 'files/BarCharts/column_' + str(columnNumber) + '_Dictionary.txt'
    saveSimpleDictionary(columnDictionary, savingAddress)
    barChart(columnDictionary, columnNumber)


def TechnologyLetterBarChart():
    # simpleBars(inputFile)
    savingAddress = "files/BarCharts/relationBitweenTechAndLetter_Dictionary.txt"
    columnDictionary = returnDictionaryByTechnologyLetter(inputFile)
    # saveDictionary(columnDictionary, "files/BarCharts/relationBitweenTechAndLetter_Dictionary.txt")

    with open(savingAddress, "a") as output_handle:
        for elem in columnDictionary.keys():
            output_handle.write(elem)
            output_handle.write(',')
            output_handle.write(str(columnDictionary[elem]))
            output_handle.write('\n')

    # data to plot
    n_groups = columnDictionary.__len__()
    nanoporeList = []
    illuminaList = []
    for elem in columnDictionary:
        nanoporeList.append(columnDictionary[elem]['Nanopore'])
        illuminaList.append(columnDictionary[elem]['Illumina'])

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, nanoporeList, bar_width, alpha=opacity, color='b', label='Nonopore')
    rects2 = plt.bar(index + bar_width, illuminaList, bar_width, alpha=opacity, color='g', label='Illumina')

    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title('Technoloty Letter ')
    plt.xticks(index + bar_width, columnDictionary.keys())
    plt.legend()

    plt.tight_layout()
    BarOutputAddress = 'files/BarCharts/LetterBar_tech.png'
    plt.savefig(BarOutputAddress, dpi=400)

    plt.show()


# realFile
inputFile = 'files/Msa_NoSpace_withExtraLetter.csv'
# test
# inputFile = 'files/test_2_withExtraLetter.csv'
simpleBars(inputFile)
