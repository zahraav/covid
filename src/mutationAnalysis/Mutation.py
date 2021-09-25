from Bio import Phylo
from io import StringIO
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

color = {}
collectionDateDictionary = {}  # {cluster: [count,min,max],..}


def getContinents():
    print('a')


def printCollectionDataDictionaryToFile(DateDictionary):
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
    with open(outputFile, '+a') as outfile:
        for cl in clusterDictionary:
            outfile.write(cl)
            outfile.write('  : ')
            outfile.write(str(clusterDictionary[cl]))
            outfile.write('\n')


def printListOfCountries(countriesDictionary):
    with open(CountryFile, '+a') as cFile:
        for cc in countriesDictionary:
            cFile.write(str(cc))
            cFile.write(': ')
            cFile.write(str(collectionDateDictionary[cc][0]))
            cFile.write(str(countriesDictionary[cc]))
            cFile.write('\n')


def drawPieChart(countryCountList, myLabels, fileName):
    y = np.array(countryCountList)  # [35, 25, 25, 15, 5]
    # myLabels = ["Apples", "Bananas", "Cherries", "Dates", "haha"]

    plt.pie(y, labels=myLabels, startangle=90)
    plt.legend(bbox_to_anchor=(0.85, 1.025), loc="upper left")

    plt.show()
    plt.savefig('files/GISAID-hCoV-19-phylogeny-2021-06-03/Plot/books_read_' + str(fileName) + '.png')


def Makeplots(countriesDictionary):
    for cluster in countriesDictionary:
        valueList = []
        for it in countriesDictionary[cluster].values():
            #print(valueList, '   ',it)

            valueList.append(str(it))

        #print(countriesDictionary[cluster].keys())
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
    """
    years = ['2019', '2020', '2021']
    csvDict = {}  # {name:[info,date]
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


def readNewickTree(inputFile):
    output = ''
    with open(inputFile) as infile:
        for line in infile:
            output += line
    return output


def listOfCountries(idCluster, csvInfo):
    countryDictionary = {}

    for node in idCluster:
        if csvInfo.get(node) != None:
            country = csvInfo.__getitem__(node)[0].split('/')[1]
            if countryDictionary.__contains__(idCluster[node]):
                if countryDictionary[idCluster[node]].keys().__contains__(country):
                    count = countryDictionary[idCluster[node]][country]
                    countryDictionary[idCluster[node]][country] = count + 1
                else:
                    countryDictionary[idCluster[node]][country] = 1
            else:
                countryDictionary[idCluster[node]] = {country: 1}
    return countryDictionary


treeData = readNewickTree('files/GISAID-hCoV-19-phylogeny-2021-06-03/global.tree')
CSVInfo = returnCSVList('files/GISAID-hCoV-19-phylogeny-2021-06-03/metadata.csv')

#treeData = "(EPI_ISL_406801:0,((EPI_ISL_1712380:0.000133812)0.10:20,EPI_ISL_578194:22,EPI_ISL_2035877:3):0);"


tree = Phylo.read(StringIO(treeData), "newick")
# Phylo.draw_ascii(tree)
# Phylo.draw(tree)

lenForCount = 1e-4
for cld in tree.clade:
    DFS(cld, lenForCount, 0)

outputFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output.txt'
DateFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output_CollectionDate_count.txt'
CountryFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/country.txt'

printClustersToFile(color)
# print(color)  # id : clusterNum
analyzeTree(color, CSVInfo)
printCollectionDataDictionaryToFile(collectionDateDictionary)
# print(collectionDateDictionary)  # cluster: count, minDate, MaxDate
CountryDictionary = listOfCountries(color, CSVInfo)
printListOfCountries(CountryDictionary)  # cluster: {countriesName: count,...} , ....
Makeplots(CountryDictionary)
