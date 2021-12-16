import csv
import os

import matplotlib.pyplot as plt
import numpy as np

from utilities.ReadAndWrite import saveSimpleDictionary, saveToCsv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    """
    This method send data to the saveToCSV method on ReadAndWrite.py to save on CSV file.
    :param fileName: Address of output file
    :param csvList: A list containing data on one CSV line
    :param isFirstTimeUsingHeader: tell the SaveToCsv method if it's the first time the method is called so
    that it print the header on the output file.
    :return:
    """
    fieldNames = ['id', 'reference', 'seq', 'date', 'location', 'technology', 'index']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)


def returnColumnDictionary(inputAddress, columnNum):
    """
    # TODO
    :param inputAddress:
    :param columnNum:
    :return:
    """
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
    # TODO
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
    """
    This method gets a CSV file containing the Sequence technology and
    different letters. Then generates a dictionary with different letters
    as keys and sequence technologies as value.
    example:
    {'S':{'Nanopore': 10, 'Illumina': 20},'N':{'Nanopore': 1, 'Illumina': 3},....}
    :param inputAddress: Address for CSV file
    :return: columnDict which is dictionary for letters and Sequence Technology
    """
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
    This method get column dictionary as in input and depends on column numbers generate a bar charts.
    :param columnDict: Dictionary containing input data
    :param columnNumber: Indicates the kind of bar chart.
    :return:
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
        plt.title('Id of sequences with ')
    elif columnNumber == 3:  # Technology
        BarOutputAddress = 'files/BarCharts/technologyBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('technology')
        plt.ylabel('Count')

    elif columnNumber == 4:  # indices
        BarOutputAddress = 'files/BarCharts/indicesBar.png'
        for elem in columnDict.keys():
            if columnDict[elem] >= 1000:
                yAxis.append(columnDict[elem])
                xAxis.append(elem)

        plt.xlabel('indices')
        plt.ylabel('Count')

    elif columnNumber == 5:  # letter
        BarOutputAddress = 'files/BarCharts/LetterBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('Letter')
        plt.ylabel('Count')

    plt.bar(xAxis, yAxis)
    plt.savefig(BarOutputAddress, dpi=800)
    plt.show()


def simpleBars(inputFile_):
    """
    This method gets a csv file and depending on the graphName draw one of the bar chart plots.
    :param inputFile_:
    :return:
    """
    for i in range(0, 6):
        columnNumber = i  # id

    # columnNumber = 0 --> id
    # columnNumber = 1 --> date
    # columnNumber = 2 --> location
    # columnNumber = 3 --> technology
    # columnNumber = 4 --> index
    # columnNumber = 5  --> Letter

    columnDictionary = {}
    if columnNumber == 0 or columnNumber == 4 or columnNumber == 5:
        columnDictionary = returnColumnDictionary(inputFile_, columnNumber)
    elif columnNumber == 3:
        techDictionary = {'Nanopore': 0, 'Illumina': 0}
        columnDictionary = returnDictionaryById(inputFile_, columnNumber, techDictionary)

    savingAddress = 'files/BarCharts/column_' + str(columnNumber) + '_Dictionary.txt'
    saveSimpleDictionary(columnDictionary, savingAddress)
    barChart(columnDictionary, columnNumber)


def TechnologyLetterBarChart(inputFile_, savingAddress):
    """
    This method gets an Multiple sequence alignment file as an input.
    Then generate the sequence technology/letter bar chart.
    first by passing the input file to returnDictionaryByTechnologyLetter method it gets a dictionary
    containing the relationship between sequenced technology and IUPAC nucleotide code
    -except 'A', 'C', 'G', 'T'-
    :param savingAddress: address for saving the dictionary that shows the relationship
    between sequence technology and letters
    :param inputFile_: input CSV file that was made from MSA file.
    :return:
    """

    # columnDict[letter] = {'Nanopore': 0, 'Illumina': 0}
    columnDictionary = returnDictionaryByTechnologyLetter(inputFile_)

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
    _, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, nanoporeList, bar_width, alpha=opacity, color='b', label='Nanopore')
    rects2 = plt.bar(index + bar_width, illuminaList, bar_width, alpha=opacity, color='g', label='Illumina')

    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title('Technology Letter ')
    plt.xticks(index + bar_width, columnDictionary.keys())
    plt.legend()

    plt.tight_layout()
    BarOutputAddress = 'files/BarCharts/Letter_technology.png'
    plt.savefig(BarOutputAddress, dpi=800)

    plt.show()


def DrawBarChart(inputFile, outputAddress):
    os.mkdir('files/output/BarChart')

    # realFile
    # test
    # inputFile = 'files/test_2_withExtraLetter.csv'
    simpleBars(inputFile)

    TechnologyLetterBarChart(inputFile, outputAddress)
