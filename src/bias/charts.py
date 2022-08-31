import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import configparser
from datetime import datetime

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    """
    This method returns config from config file in config/config.
    Configs of project are there so for change the configuration of the project we just need to change
    the config file
    :return: configs of app
    """
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def saveData(saving_address, data):
    """
    This function write the data in the output_address file
    :param saving_address: Address of file which we want to save data
    :param data: data for saving in the file , String
    :return: none
    """
    with open(saving_address, "a") as output_handle:
        output_handle.write(data)


def saveDictionary(inputDictionary, savingAddress):
    """
    This method save a dictionary into a file.
    :param inputDictionary: input dictionary
    :param savingAddress: Output address
    :return:
    """
    for elem in inputDictionary.keys():
        saveData(savingAddress, elem + ':' + str(inputDictionary[elem]) + '\n')


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


def returnColumnDictionary(inputAddress, columnNum):
    """
    :param inputAddress:
    :param columnNum: column number
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
        BarOutputAddress = 'files/output/BarCharts/idBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('Ids')
        plt.ylabel('Count')
        plt.title('Id of sequences with ')
    elif columnNumber == 2:  # location
        BarOutputAddress = 'files/output/BarCharts/locationLetter.jpeg'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('Location')
        plt.ylabel('IUPAC codes')
        plt.title('IUPAC codes in regions')
    elif columnNumber == 3:  # Technology
        BarOutputAddress = 'files/output/BarCharts/technologyBar.png'
        yAxis = columnDict.values()
        xAxis = columnDict.keys()
        plt.xlabel('technology')
        plt.ylabel('Count')

    elif columnNumber == 4:  # indices
        BarOutputAddress = 'files/output/BarCharts/indicesBar.png'
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


def simpleBars(inputAddress):
    """
    This method gets a csv file and depending on the graphName draw one of the bar chart plots.
    :param inputAddress:
    :return:
    """
    # TODO assign Column number
    columnNumber = 0  # id

    # columnNumber = 0 --> id
    # columnNumber = 1 --> date
    # columnNumber = 2 --> location
    # columnNumber = 3 --> technology
    # columnNumber = 4 --> index
    # columnNumber = 5  --> Letter

    columnDictionary = {}
    if columnNumber == 0 or columnNumber == 4 or columnNumber == 5:
        columnDictionary = returnColumnDictionary(inputAddress, columnNumber)
    elif columnNumber == 3:
        techDictionary = {'Nanopore': 0, 'Illumina': 0}
        columnDictionary = returnDictionaryById(inputAddress, columnNumber, techDictionary)

    savingAddress = 'files/BarCharts/column_' + str(columnNumber) + '_Dictionary.txt'
    saveDictionary(columnDictionary, savingAddress)
    changeTxtToCSV(savingAddress, savingAddress.replace('.txt', '.csv'))
    barChart(columnDictionary, columnNumber)


def technologyLetterBarChart(inputFile_, savingAddress):
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

    plt.bar(index, nanoporeList, bar_width, alpha=opacity, color='blue', label='Nanopore')
    plt.bar(index + bar_width, illuminaList, bar_width, alpha=opacity, color='green', label='Illumina')

    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title('Technology Letter ')
    plt.xticks(index + bar_width, columnDictionary.keys())
    plt.legend()

    plt.tight_layout()
    BarOutputAddress = 'files/BarCharts/Letter_technology.png'
    plt.savefig(BarOutputAddress, dpi=800)

    plt.show()


def drawBarChart(inputFile, outputAddress):
    os.mkdir('files/output/BarChart')

    # realFile
    # test
    # inputFile = 'files/test_2_withExtraLetter.csv'
    simpleBars(inputFile)

    technologyLetterBarChart(inputFile, outputAddress)


def generateLocationDictionary(inputAddress):
    columnDict = {}
    isFirstRow = True
    with open(inputAddress) as csv_file:
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


def letterBarChart(inputDictionary, yBarLabel, title, BarOutputAddress):
    """
    This method gets an csv file that was generated from MSA file
    as an input.Then generate the region/letter bar chart.
    :param BarOutputAddress:
    :param title:
    :param yBarLabel:
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

    # create plot
    _, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index + bar_width, YList, bar_width, alpha=opacity, color='green', label='Y')
    plt.bar(index + bar_width, SList, bar_width, alpha=opacity, color='blue', label='S')
    plt.bar(index + bar_width, WList, bar_width, alpha=opacity, color='gray', label='W')
    plt.bar(index + bar_width, KList, bar_width, alpha=opacity, color='yellow', label='K')
    plt.bar(index + bar_width, RList, bar_width, alpha=opacity, color='pink', label='R')
    plt.bar(index + bar_width, MList, bar_width, alpha=opacity, color='red', label='M')
    plt.bar(index + bar_width, HList, bar_width, alpha=opacity, color='black', label='H')
    plt.bar(index + bar_width, DList, bar_width, alpha=opacity, color='aqua', label='D')
    plt.bar(index + bar_width, BList, bar_width, alpha=opacity, color='olive', label='B')
    plt.bar(index + bar_width, VList, bar_width, alpha=opacity, color='orange', label='V')

    plt.xlabel('IUPAC codes')
    plt.ylabel(yBarLabel)
    plt.title(title)
    plt.xticks(index + bar_width, inputDictionary.keys())
    plt.legend()

    plt.tight_layout()
    plt.savefig(BarOutputAddress, dpi=1600)

    plt.show()


def drawLocationBar(inputAddress):
    locationDictionary = generateLocationDictionary(inputAddress)
    savingAddress = 'files/output/BarCharts/column_' + str(2) + '_Dictionary.txt'
    saveDictionary(locationDictionary, savingAddress)

    barChart(locationDictionary, 2)


def generateLocationLettersDictionary(inputAddress):
    locationDict = {}
    isFirstRow = True
    with open(inputAddress) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[2]
            letter = row[5]
            if locationDict.keys().__contains__(item):
                locationDict[item][letter] = locationDict[item][letter] + 1
            else:
                locationDict[item] = {'M': 0, 'R': 0, 'W': 0, 'S': 0, 'Y': 0, 'K': 0,
                                      'V': 0, 'H': 0, 'D': 0, 'B': 0, 'N': 0, '-': 0}
    return locationDict


def saveDictionaryToCSV(outputFile, inputDictionary, firstItem):
    header = [firstItem, 'M', 'R', 'W', 'S', 'Y', 'K', 'V', 'H', 'D', 'B', 'N', '-']
    with open(outputFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

        for item in inputDictionary:
            newRow = {firstItem: item}
            newRow.update(inputDictionary[item])
            writer.writerow(newRow)


def drawLocationLetterBar(inputAddress):
    locationDictionary = generateLocationLettersDictionary(inputAddress)
    outputFile = 'files/output/BarCharts/locationLettersBarDictionary.csv'
    saveDictionaryToCSV(outputFile, locationDictionary, 'region')
    savingAddress = 'files/output/BarCharts/column_LocationLetter_Dictionary.txt'
    saveDictionary(locationDictionary, savingAddress)
    letterBarChart(locationDictionary, 'Count', 'regions', 'files/output/BarCharts/Letter_Location.jpeg')


def changeTxtToCSV(inputAddress, outputFile):
    with open(inputAddress) as infile:
        with open(outputFile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            for line in infile:
                newRow = [line.split(':')[0], line.split(':')[1].strip()]
                writer.writerow(newRow)


def generateIndicesLetterDictionary(inputAddress):
    indicesDict = {}
    isFirstRow = True
    with open(inputAddress) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            item = row[4]
            letter = row[5]
            if indicesDict.keys().__contains__(item):
                indicesDict[item][letter] = indicesDict[item][letter] + 1
            else:
                indicesDict[item] = {'M': 0, 'R': 0, 'W': 0, 'S': 0, 'Y': 0, 'K': 0,
                                     'V': 0, 'H': 0, 'D': 0, 'B': 0, 'N': 0, '-': 0}

    return indicesDict


def drawIndicesLetter(inputAddress):
    indicesDictionary = generateIndicesLetterDictionary(inputAddress)
    columnDictionary = returnColumnDictionary(inputAddress, 4)
    resultDictionary = {}

    for elem in columnDictionary.keys():
        if columnDictionary[elem] >= 1000:
            resultDictionary[elem] = indicesDictionary[elem]
    saveDictionaryToCSV('files/output/BarCharts/IndicesLetter.csv', resultDictionary, 'Indices')
    BarOutputAddress = 'files/output/BarCharts/IndicesLetter.jpeg'
    letterBarChart(resultDictionary, 'IUPAC codes', 'Indices-IUPAC codes', BarOutputAddress)


def timeChart(inFile):
    """
    This method makes the time chart for from the Fasta file
    :param inFile: main fasta file for making the time chart
    :return:
    """
    outputChartFile = config['outputAddresses'].get('timeChart')

    makeTimeChartGraph(inFile, outputChartFile)


def getCountry(line):
    """
    This method returns the country for a line in the
    """
    return line.split('|')[0].split('/')[1].strip()


def getDateOf(line):
    """
    This method returns the country for a line in the
    """
    return line.split('|')[2].strip()


def makeTimeChartGraph(inFastaFile, outputChartAddress):
    """
    This method make the Time Chart for Graph that shows the time of starting the variant and the country
    it initiated and then also shows the time and the countries it moves around the world
    :param inFastaFile: Fasta file containing the sequence technology
    :param outputChartAddress:
    :return:
    """
    countries = {}
    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):
                country = getCountry(line)
                date = getDateOf(line)
                if country in countries:
                    countries[country].append(date)
                else:
                    countries[country] = [date]
    count = 0
    for (country, dates) in countries.items():
        sequenceDates = []
        for dd in dates:
            x = dd.split('-')
            if len(x) >= 2:
                if int(x[1]) == 0:
                    x[1] = 1
                if len(x) == 2:
                    sequenceDates.append(datetime(int(x[0]), int(x[1]), 1, 0))
                elif len(x) == 3:
                    if int(x[2]) == 0:
                        x[2] = 1
                    sequenceDates.append(datetime(int(x[0]), int(x[1]), int(x[2]), 0))
        # dates = [datetime(int(dd.split('-')[0]), int(dd.split('-')[1]), int(dd.split('-')[2]), 0) for dd in dates]

        sequenceDates = sorted(sequenceDates)
        count += 1
        if count < 10:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))], label=str(country))
        else:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))])
    plt.xlabel('Time    Confirmed cases')
    plt.ylabel('Confirmed cases')
    plt.title('Cumulative worldwide confirmed Covid-19 cases')

    plt.legend(loc='best', fontsize='5')
    plt.gcf().autofmt_xdate()
    plt.savefig(outputChartAddress)
    plt.close()


# real data:
# inputFile = 'files/Msa_NoSpace_withExtraLetter.csv'
# Test:
# inputFile = 'files/test_Msa_withExtraLetter.csv'

timeChart('files/input/msa_0206.fasta')
# drawBarChart(inputFile, "files/output/BarCharts/relationBetweenTechAndLetter_Dictionary.txt")
# drawLocationBar(inputFile)
# drawLocationLetterBar(inputFile)
# drawIndicesLetter(inputFile)
# changeTxtToCSV('files/output/BarCharts/column_0_Dictionary.txt','files/output/BarCharts/column_0_Dictionary.csv')
