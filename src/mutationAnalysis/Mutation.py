from Bio import Phylo
from io import StringIO
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()

color = {}
collectionDateDictionary = {}  # {cluster: [count,min,max],..}


def getContinents():
    print('a')


def printCollectionDataDictionaryToFile(DateDictionary):
    DateFile = config['outputAddresses'].get('DateFile')

    with open(DateFile, '+a') as dateFile:
        for mmd in DateDictionary:
            dateFile.write(str(mmd))  # clusterNum
            dateFile.write('  : ')
            dateFile.write(str(DateDictionary[mmd][1]))  # minDate
            dateFile.write(', ')
            dateFile.write(str(DateDictionary[mmd][2]))  # maxDAte
            dateFile.write(', ')
            dateFile.write(str(DateDictionary[mmd][0]))  # count
            dateFile.write('\n')


def printClustersToFile(clusterDictionary):
    outputFile = config['outputAddresses'].get('country')

    with open(outputFile, '+a') as outfile:
        for cl in clusterDictionary:
            outfile.write(cl)
            outfile.write('  : ')
            outfile.write(str(clusterDictionary[cl]))
            outfile.write('\n')


def printCountryDictionary(inputDictionary, outputFileName):
    # print('-->', inputDictionary , '    ', outputFileName)
    # print('==>',collectionDateDictionary)
    with open(outputFileName, 'w') as cFile:
        for cc in inputDictionary:
            cFile.write(str(cc))
            cFile.write(': ')

            cFile.write(str(collectionDateDictionary[cc][0]))
            cFile.write(str(inputDictionary[cc]))
            cFile.write('\n')


def printDictionary(inputDictionary, outputFileName):
    print('-->', inputDictionary)
    with open(outputFileName, 'w') as cFile:
        for cc in inputDictionary:
            cFile.write(str(cc))
            cFile.write('\n')


def drawPieChart(countryCountList, myLabels, cluster):
    pieChartsFolder = config['outputAddresses'].get('pieChartsFolder')

    y = np.array(countryCountList)  # [35, 25, 25, 15, 5]
    # myLabels = ["Apples", "Bananas", "Cherries", "Dates", "haha"]

    plt.pie(y, labels=myLabels, startangle=90)
    plt.legend(bbox_to_anchor=(0.85, 1.025), loc="upper left")

    # plt.show()
    plt.savefig(pieChartsFolder + "pieChart_" + str(cluster) + '.png')
    plt.close()


def MakePlots(countriesDictionary):
    for cluster in countriesDictionary:
        valueList = []
        for it in countriesDictionary[cluster].values():
            # print(valueList, '   ',it)

            valueList.append(str(it))

        # print(countriesDictionary[cluster].keys())
        drawPieChart(valueList, countriesDictionary[cluster].keys(), cluster)


def analyzeTree(DFSTreeDictionary, CSVDictionary):
    """
    this Method fill collectionDateDictionary , keys are clusters and the values are minimum Date and
    Maximum Date for every cluster
    :param DFSTreeDictionary:
    :param CSVDictionary:
    :return:
    """

    for leaf in DFSTreeDictionary:  # from Tree [leaf, cluster]
        if CSVDictionary.keys().__contains__(leaf):
            minDate = datetime.now()
            maxDate = datetime.strptime("2019-01-01", "%Y-%m-%d")

            if collectionDateDictionary != {} and \
                    collectionDateDictionary.keys().__contains__(DFSTreeDictionary[leaf]):
                # {cluster: [minDate , MaxDate]}
                minDate = collectionDateDictionary[DFSTreeDictionary[leaf]][1]
                maxDate = collectionDateDictionary[DFSTreeDictionary[leaf]][2]

            else:
                collectionDateDictionary[DFSTreeDictionary[leaf]] = [0, minDate,
                                                                     maxDate]

            date_dt3 = datetime.strptime(CSVDictionary[leaf][1], '%Y-%m-%d')

            if minDate > date_dt3:  # min > collection date[leaf]
                collectionDateDictionary[DFSTreeDictionary[leaf]][1] = date_dt3
            if maxDate < date_dt3:  # max < collection date[leaf]
                collectionDateDictionary[DFSTreeDictionary[leaf]][2] = date_dt3

            collectionDateDictionary[DFSTreeDictionary[leaf]][0] = collectionDateDictionary[DFSTreeDictionary[leaf]][
                                                                       0] + 1


def returnCSVList(inputCSV):
    """
    read CSV Metadata file and return a dictionary base on file
    if the date format is correct add the data to dictionary.
    because some data don't have year and or just mention the year, and don't have month and day, therefore
    I ignore these data.
    :param inputCSV: CSV input file
    :return a dictionary {AccessionId:[info , collectionDate]}
    """
    years = ['2019', '2020', '2021', '2022']
    csvDict = {}  # {accessionId:[info, collectionDate]}
    with open(inputCSV, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row[2]) == 10:
                if row[2][0:4] in years:
                    csvDict[row[0]] = [row[1], row[2]]
    return csvDict


def DFS(v, cutLength, colour):
    if v.is_terminal():
        color[v.name] = colour
    else:
        for node in v:
            if node.branch_length < cutLength:
                DFS(node, cutLength, colour)
            else:
                colour += 1
                DFS(node, cutLength, colour)


def getContentOfFile(inputFile):
    """
    This method read the input file and return the data in the file.
    :param inputFile: Input file
    :return: String contains all the data in the file
    """
    output = ''
    with open(inputFile) as infile:
        for line in infile:
            output += line
    return output


def saveToFile(cluster, collectionDate, country, accessionId):
    timeChartFolder = config['outputAddresses'].get('timeChartCluster')  # for countries

    with open((timeChartFolder+'_'+str(cluster)+'.txt'), '+a') as dateFile:
        dateFile.write(country)
        dateFile.write('\t')
        dateFile.write(accessionId)
        dateFile.write('\t')
        dateFile.write(collectionDate)
        dateFile.write('\n')


def listOfCountries(idCluster, csvInfo):
    # accessionId - country -collectionDate

    countryDictionary = {}

    for node in idCluster:
        if csvInfo.get(node) is not None:  # csvFile contains that node
            country = csvInfo.__getitem__(node)[0].split('/')[1]
            collectionDate = csvInfo[node][1]

            saveToFile(idCluster[node], collectionDate, country, node)

            if countryDictionary.__contains__(idCluster[node]):  # the country already exist on the dictionary
                if countryDictionary[idCluster[node]].keys().__contains__(country):
                    count = countryDictionary[idCluster[node]][country]
                    countryDictionary[idCluster[node]][country] = count + 1
                else:
                    countryDictionary[idCluster[node]][country] = 1

            else:
                countryDictionary[idCluster[node]] = {country: 1}

    return countryDictionary


def mutationAnalysis(globalTree, metadataFile):
    """
    This method gets a phylogeneticTree and metadata File related to phylogenetic Tree.
    Phylogenetic Tree is on the newick format.
    :param globalTree:
    :param metadataFile:
    :return:
    """
    treeData = getContentOfFile(globalTree)
    CSVInfo = returnCSVList(metadataFile)

    # treeData = "(EPI_ISL_406801:0,((EPI_ISL_1712380:0.000133812)0.10:20,EPI_ISL_578194:22,EPI_ISL_2035877:3):0);"

    tree = Phylo.read(StringIO(treeData), "newick")

    lenForCount = 1e-4
    for cld in tree.clade:
        DFS(cld, lenForCount, 0)

    printClustersToFile(color)
    # print(color)  # id : clusterNum
    analyzeTree(color, CSVInfo)
    printCollectionDataDictionaryToFile(collectionDateDictionary)
    # print(collectionDateDictionary)  # cluster: count, minDate, MaxDate
    CountryDictionary = listOfCountries(color, CSVInfo)

    pieChartData = config['outputAddresses'].get('country')  # for countries

    printCountryDictionary(CountryDictionary, pieChartData)  # cluster: {countriesName: count,...} , ....
    MakePlots(CountryDictionary)
# variant -country - collectionDate
