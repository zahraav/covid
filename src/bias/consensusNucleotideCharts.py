import csv

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


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
    x = {}
    for name, elem in zip(fieldNames, csvList):
        x[name] = str(elem)
    with open(fileName, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isFirstTimeUsingHeader:
            writer.writeheader()
        writer.writerow(x)


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


def returnDictionaryByTechnologyLetter(inputFile):
    """
    This method gets a CSV file containing the Sequence technology and
    different letters. Then generates a dictionary with different letters
    as keys and sequence technologies as value.
    example:
    {'S':{'Nanopore': 10, 'Illumina': 20},'N':{'Nanopore': 1, 'Illumina': 3},....}
    :param inputFile: Address for CSV file
    :return: columnDict which is dictionary for letters and Sequence Technology
    """
    # number of column for letters can be used when counting a sequence for multiple times is not important
    columnDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
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


def IUPACAnnotation(inputFile, outFolder):
    df = pd.read_csv(inputFile, index_col=0, encoding='utf-8')
    sns.countplot(x='letter', data=df)
    plt.xlabel('Consensus nucleotides')
    plt.ylabel('Count')
    plt.title('Number of consensus nucleotides found in all sequences')
    plt.savefig(outFolder + 'IUPAC.jpeg')
    # plt.show()


def location(inputFile, outFolder):
    df = pd.read_csv(inputFile, index_col=0, encoding='utf-8')
    sns.countplot(x='location', data=df)
    plt.xlabel('Location')
    plt.ylabel('Count')
    plt.title('Number of consensus nucleotides in every continent')
    plt.xticks(rotation=-15)
    plt.savefig(outFolder + 'Location.jpeg')
    # plt.show()


def sequencingTechnology(inputFile, outFolder):
    df = pd.read_csv(inputFile, index_col=0, encoding='utf-8')
    sns.countplot(x='technology', data=df)
    plt.xlabel('Sequencing technology')
    plt.ylabel('Count')
    plt.title('Number of consensus nucleotides in each sequencing technology')
    plt.xticks(rotation=-15)
    plt.savefig(outFolder + 'sequencingTechnology.jpeg')
    # plt.show()


def ids(inputFile, outFolder):
    df = pd.read_csv(inputFile, index_col=0, encoding='utf-8')
    sns.countplot(x='id', data=df)
    plt.xlabel('ids')
    plt.ylabel('Count')
    plt.title('Number of consensus nucleotides in each sequences')
    plt.xticks(rotation=-15)
    plt.savefig(outFolder + 'id.jpeg')
    # plt.show()


def returnColumnDictionary(inputFile):
    # number of column for letters can be used when counting a sequence for multiple times is not important
    columnDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[5]
            if item in columnDict.keys():
                columnDict[item] = columnDict[item] + 1
            else:
                columnDict[item] = 1
    return columnDict


def indices(inputFile, outFolder):
    yAxis = []
    xAxis = []
    columnDictionary = returnColumnDictionary(inputFile)

    for elem in columnDictionary.keys():
        if columnDictionary[elem] >= 1000:
            yAxis.append(columnDictionary[elem])
            xAxis.append(elem)

    plt.xlabel('indices')
    plt.ylabel('Count')
    plt.title('Number of consensus nucleotides in each location')
    plt.bar(xAxis, yAxis)
    plt.savefig(outFolder + "indices.jpeg")
    # plt.show()


def saveDictionaryWithConsensusNucleotideToCSV(outputFile, inputDictionary, firstItem):
    header = [firstItem, 'M', 'R', 'W', 'S', 'Y', 'K', 'V', 'H', 'D', 'B', 'N', '-']
    with open(outputFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for item in inputDictionary:
            newRow = {firstItem: item}
            newRow.update(inputDictionary[item])
            writer.writerow(newRow)


def generateLocationLettersDictionary(inputFile):
    locationDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[3]
            letter = row[6]
            if not locationDict.keys().__contains__(item):
                locationDict[item] = {'M': 0, 'R': 0, 'W': 0, 'S': 0, 'Y': 0, 'K': 0,
                                      'V': 0, 'H': 0, 'D': 0, 'B': 0, 'N': 0, '-': 0}

            locationDict[item][letter] = locationDict[item][letter] + 1
    return locationDict


def locationConsensusNucleotide(inputFile, outFolder):
    locationDictionary = generateLocationLettersDictionary(inputFile)
    outputFile = outFolder + 'location_letter_ratio.csv'
    saveDictionaryWithConsensusNucleotideToCSV(outputFile, locationDictionary, 'Continent')
    letterBarChart(locationDictionary, 'Count per sequencing (ratio)', 'Continents', 'Ratio of consensus nucleotide in '
                                                                                     'different continents',
                   outFolder + 'location_letter_ratio.jpeg')


def letterBarChart(inputDictionary, yLabel, xLabel, title, BarOutputAddress):
    """
    This method gets an csv file that was generated from MSA file
    as an input.Then generate the region/letter bar chart.
    :param xLabel:
    :param BarOutputAddress:
    :param title:
    :param yLabel:
    :param inputDictionary :
    :return:
    """
    # data to plot
    n_groups = inputDictionary.__len__()
    YList = []
    SList = []
    WList = []
    KList = []
    RList = []
    MList = []
    HList = []
    DList = []
    BList = []
    VList = []
    sumDictionary = {}

    for xx in inputDictionary:
        sumDictionary[xx] = sum(inputDictionary[xx].values())
    for elem in inputDictionary:
        x = sumDictionary[elem]
        YList.append((inputDictionary[elem]['Y']) / x)
        SList.append((inputDictionary[elem]['S']) / x)
        WList.append((inputDictionary[elem]['W']) / x)
        KList.append((inputDictionary[elem]['K']) / x)
        RList.append((inputDictionary[elem]['R']) / x)
        MList.append((inputDictionary[elem]['M']) / x)
        HList.append((inputDictionary[elem]['H']) / x)
        DList.append((inputDictionary[elem]['D']) / x)
        BList.append((inputDictionary[elem]['B']) / x)
        VList.append((inputDictionary[elem]['V']) / x)

    # create plot
    _, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.05
    opacity = 0.8

    plt.bar(index, YList, bar_width, alpha=opacity, color='green', label='Y')
    plt.bar(index + bar_width, RList, bar_width, alpha=opacity, color='pink', label='R')
    plt.bar(index + 2 * bar_width, SList, bar_width, alpha=opacity, color='blue', label='S')
    plt.bar(index + 3 * bar_width, WList, bar_width, alpha=opacity, color='gray', label='W')
    plt.bar(index + 4 * bar_width, KList, bar_width, alpha=opacity, color='yellow', label='K')
    plt.bar(index + 5 * bar_width, MList, bar_width, alpha=opacity, color='red', label='M')
    plt.bar(index + 6 * bar_width, HList, bar_width, alpha=opacity, color='black', label='H')
    plt.bar(index + 7 * bar_width, DList, bar_width, alpha=opacity, color='aqua', label='D')
    plt.bar(index + 8 * bar_width, BList, bar_width, alpha=opacity, color='c', label='B')
    plt.bar(index + 9 * bar_width, VList, bar_width, alpha=opacity, color='orange', label='V')

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.xticks(index + bar_width, inputDictionary.keys())
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(BarOutputAddress, dpi=1600)

    plt.show()


def returnDictionarybyTechnologyLetter(inputFile):
    """
    This method gets a CSV file containing the Sequence technology and
    different letters. Then generates a dictionary with different letters
    as keys and sequence technologies as value.
    example:
    {'S':{'Nanopore': 10, 'Illumina': 20},'N':{'Nanopore': 1, 'Illumina': 3},....}
    :param inputFile: Address for CSV file
    :return: columnDict which is dictionary for letters and Sequence Technology
    """
    # number of column for letters can be used when counting a sequence for multiple times is not important
    columnDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            letter = row[6]  # letter
            tech = row[4]
            if tech == 'Illumina' or tech == 'Nanopore':
                if letter in columnDict.keys():
                    columnDict[letter][tech] = columnDict[letter][tech] + 1
                else:
                    columnDict[letter] = {'Nanopore': 0, 'Illumina': 0}
                    columnDict[letter][tech] = columnDict[letter][tech] + 1
    return columnDict


def technologyConsensusNucleotide(inputFile, outFolder):
    """
    This method gets an Multiple sequence alignment file as an input.
    Then generate the sequence technology/letter bar chart.
    first by passing the input file to returnDictionarybyTechnologyLetter method it gets a dictionary
    containing the relationship between sequenced technology and IUPAC nucleotide code
    -except 'A', 'C', 'G', 'T'-
    between sequence technology and letters
    :return:
    """

    # columnDict[letter] = {'Nanopore': 0, 'Illumina': 0}
    columnDictionary = returnDictionarybyTechnologyLetter(inputFile)
    header = ['letter', 'Nanopore', 'Illumina']
    with open(outFolder + 'technology_letter.csv', 'w', encoding='UTF8', newline='') as f:
        firstItem = 'letter'
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for item in columnDictionary:
            newRow = {firstItem: item}
            newRow.update(columnDictionary[item])
            writer.writerow(newRow)

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

    plt.bar(index, nanoporeList, bar_width, alpha=opacity, color='blue', label='Nanopore')
    plt.bar(index + bar_width, illuminaList, bar_width, alpha=opacity, color='green', label='Illumina')

    plt.xlabel('Consensus nucleotides')
    plt.ylabel('Count')
    plt.title('Distribution of consensus nucleotides in sequencing technologies')
    plt.xticks(index + bar_width, columnDictionary.keys())
    plt.legend()

    plt.tight_layout()
    BarOutputAddress = outFolder + 'technology_letter.jpeg'
    plt.savefig(BarOutputAddress, dpi=800)

    plt.show()


def generateIndicesLetterDictionary(inputFile):
    indicesDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[5]
            letter = row[6]
            if indicesDict.keys().__contains__(item):
                indicesDict[item][letter] = indicesDict[item][letter] + 1
            else:
                indicesDict[item] = {'M': 0, 'R': 0, 'W': 0, 'S': 0, 'Y': 0, 'K': 0,
                                     'V': 0, 'H': 0, 'D': 0, 'B': 0, 'N': 0, '-': 0}

    return indicesDict


def indicesConsensusNucleotide(inputFile, outFolder):
    indicesDictionary = generateIndicesLetterDictionary(inputFile)
    columnDictionary = returnColumnDictionary(inputFile)
    resultDictionary = {}
    for elem in columnDictionary.keys():
        if columnDictionary[elem] >= 1000:
            resultDictionary[elem] = indicesDictionary[elem]
    saveDictionaryWithConsensusNucleotideToCSV(outFolder + 'IndicesLetter.csv', resultDictionary, 'Indices')

    BarOutputAddress = outFolder + 'Indices_Letter.jpeg'
    letterBarChart(resultDictionary, 'Sum of Consensus nucleotide', 'Location in the sequences', 'distribution of '
                                                                                                 'consensus nucleotide'
                                                                                                 ' in loci of '
                                                                                                 'sequences',
                   BarOutputAddress)


def generateLocationDictionary(inputFile):
    columnDict = {}
    isFirstRow = True
    with open(inputFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[2]
            if item in columnDict.keys():
                columnDict[item] = columnDict[item] + 1
            else:
                columnDict[item] = 1
    return columnDict


def indicesCountMoreThan1000(inputFile, outFolder):
    """
    This method get column dictionary as in input and depends on column numbers generate a bar charts.
    :param inputFile:
    :param outFolder:
    :return:
    """
    locationDictionary = generateLocationDictionary(inputFile)

    yAxis = []
    xAxis = []
    BarOutputAddress = outFolder + 'indicesBar.png'
    for elem in locationDictionary.keys():
        if locationDictionary[elem] >= 1000:
            yAxis.append(locationDictionary[elem])
            xAxis.append(elem)

    plt.xlabel('indices')
    plt.ylabel('Count')

    plt.bar(xAxis, yAxis)
    plt.savefig(BarOutputAddress, dpi=800)
    plt.show()


def addTwoArray(list1, list2):
    res_list = []
    for i in range(0, len(list1)):
        res_list.append(list1[i] + list2[i])
    return res_list


def continent(inputFile, outFolder):
    """
    This method gets an csv file that was generated from MSA file
    as an input.Then generate the continent/letter bar chart.
    :return:
    """
    inputDictionary = generateLocationLettersDictionary(inputFile)
    outputFile = outFolder + 'continent_letter.csv'
    saveDictionaryWithConsensusNucleotideToCSV(outputFile, inputDictionary, 'Continent')
    # letterBarChart(inputDictionary, 'Count per sequencing (ratio)', 'Continents', 'Ratio of consensus nucleotide in '
    #                                                                             'different continents',
    #           outFolder + 'location_letter_ratio.jpeg')
    # data to plot
    n_groups = inputDictionary.__len__()
    YList = []
    SList = []
    WList = []
    KList = []
    RList = []
    MList = []
    HList = []
    DList = []
    BList = []
    VList = []
    sumDictionary = {}

    for xx in inputDictionary:
        sumDictionary[xx] = sum(inputDictionary[xx].values())
    for elem in inputDictionary:
        YList.append((inputDictionary[elem]['Y']))
        SList.append((inputDictionary[elem]['S']))
        WList.append((inputDictionary[elem]['W']))
        KList.append((inputDictionary[elem]['K']))
        RList.append((inputDictionary[elem]['R']))
        MList.append((inputDictionary[elem]['M']))
        HList.append((inputDictionary[elem]['H']))
        DList.append((inputDictionary[elem]['D']))
        BList.append((inputDictionary[elem]['B']))
        VList.append((inputDictionary[elem]['V']))

    Y = np.array(YList)
    S = np.array(SList)
    W = np.array(WList)
    K = np.array(KList)
    R = np.array(RList)
    M = np.array(MList)
    H = np.array(HList)
    D = np.array(DList)
    B = np.array(BList)
    V = np.array(VList)

    # create plot
    _, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.8
    plt.bar(index, YList, bar_width, alpha=opacity, color='green', label='Y')
    plt.bar(index, RList, bar_width, alpha=opacity, color='pink', label='R', bottom=Y)
    plt.bar(index, SList, bar_width, alpha=opacity, color='blue', label='S', bottom=Y + R)
    plt.bar(index, WList, bar_width, alpha=opacity, color='gray', label='W', bottom=Y + R + S)
    plt.bar(index, KList, bar_width, alpha=opacity, color='yellow', label='K', bottom=Y + R + S + W)
    plt.bar(index, MList, bar_width, alpha=opacity, color='red', label='M', bottom=Y + R + S + W + K)
    plt.bar(index, HList, bar_width, alpha=opacity, color='black', label='H', bottom=Y + R + S + W + K + M)
    plt.bar(index, DList, bar_width, alpha=opacity, color='aqua', label='D', bottom=Y + R + S + W + K + M + H)
    plt.bar(index, BList, bar_width, alpha=opacity, color='c', label='B', bottom=Y + R + S + W + K + M + H + D)
    plt.bar(index, VList, bar_width, alpha=opacity, color='orange', label='V', bottom=Y + R + S + W + K + M + H + D + B)

    plt.xlabel('Continent')
    plt.ylabel('count')
    plt.title('Distribution of consensus nucleotides in continents')
    plt.xticks(index, inputDictionary.keys())
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(outFolder + 'continent.jpeg', dpi=1600)

    plt.show()


# inputAddress = 'files/test_Msa_withExtraLetter.csv'
inputAddress = 'files/Msa_NoSpace_withExtraLetter.csv'
outputFolder = 'files/output/BarCharts/BarCharts/'
# location(inputAddress, outputFolder)
# IUPACAnnotation(inputAddress, outputFolder)
# sequencingTechnology(inputAddress, outputFolder)
# ids(inputAddress, outputFolder)
# indices(inputAddress, outputFolder)
# locationConsensusNucleotide(inputAddress, outputFolder)
continent(inputAddress, outputFolder)
# technologyConsensusNucleotide(inputAddress, outputFolder)
# indicesConsensusNucleotide(inputAddress, outputFolder)
