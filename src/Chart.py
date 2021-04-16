import csv
import matplotlib.pyplot as plt

from utilities.ReadAndWrite import saveSimpleDictionary


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


def returnTechnologyDictionaryById(inputFileAddress, columnNum, initializedDictionary):
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


def barChart(columnDict):
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
    if columnNumber == 1:
        BarOutputAddress = 'files/BarCharts/idBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()

    elif columnNumber == 3:
        BarOutputAddress = 'files/BarCharts/technologyBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()

    elif columnNumber == 4:  # indices
        BarOutputAddress = 'files/BarCharts/indicesBar_2.png'
        for elem in columnDict.keys():
            if columnDict[elem] >= 200:
                yAxis.append(columnDict[elem])
                xAxis.append(elem)

    elif columnNumber == 5:  # letter
        BarOutputAddress = 'files/BarCharts/LetterBar_2.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()

    plt.bar(xAxis, yAxis)
    plt.savefig(BarOutputAddress, dpi=400)
    plt.show()


# realFile
inputFile = 'files/Msa_NoSpace_withExtraLetter.csv'
#test
#inputFile = 'files/test_2_withExtraLetter.csv'
# columnNumber=1 # id
# columnNumber = 5 # Letter
#columnNumber = 4  # index
columnNumber = 3  # technology

columnDictionary = {}
if columnNumber == 1 or columnNumber == 4 or columnNumber == 5:
    columnDictionary = returnColumnDictionary(inputFile, columnNumber)
elif columnNumber == 3:
    techDictionary = {'Nanopore': 0, 'Illumina': 0}
    columnDictionary = returnTechnologyDictionaryById(inputFile, columnNumber, techDictionary)

savingAddress = 'files/BarCharts/column_' + str(columnNumber) + '_Dictionary.txt'
saveSimpleDictionary(columnDictionary, savingAddress)
barChart(columnDictionary)
