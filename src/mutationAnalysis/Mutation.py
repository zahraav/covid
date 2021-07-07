from Bio import Phylo
from io import StringIO
import csv
from datetime import datetime

color = {}

CollectionDateArray = [0, 0]  # min,max
collectionDateList = []
collectionDateDictionary = {}  # {cluster: [count,min,max],..}


def printCollectionDataDictionaryToFile():
    with open(DateFile, '+a') as dateFile:
        for mmd in collectionDateDictionary:
            dateFile.write(str(mmd))
            dateFile.write('  : ')
            dateFile.write(str(collectionDateDictionary[mmd][1]))
            dateFile.write(', ')
            dateFile.write(str(collectionDateDictionary[mmd][2]))
            dateFile.write(', ')
            dateFile.write(str(collectionDateDictionary[mmd][0]))
            dateFile.write('\n')


def printClustersToFile():
    with open(outputFile, '+a') as outfile:
        for cl in color:
            outfile.write(cl)
            outfile.write('  : ')
            outfile.write(str(color[cl]))
            outfile.write('\n')


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
    # print('---', v.name, v.branch_length)
    # color[v]=v.branch_length
    if v.is_terminal():
        # print(type(v.name))
        color[v.name] = colour
        # print(colour)
        # print(v, v.branch_length, colour)
    else:
        for node in v:
            # print('----',type(node.branch_length), node.branch_length, node, node.is_terminal())

            if node.branch_length < cutLength:
                DFS(node, cutLength, colour)
            else:
                colour += 1
                # print(colour)
                DFS(node, cutLength, colour)


def readNewickTree(inputFile):
    output = ''
    with open(inputFile) as infile:
        for line in infile:
            output += line
    return output


treeData = readNewickTree('files/GISAID-hCoV-19-phylogeny-2021-06-03/global.tree')
CSVInfo = returnCSVList('files/GISAID-hCoV-19-phylogeny-2021-06-03/metadata.csv')

# treeData = "(EPI_ISL_406801:0,((EPI_ISL_1712380:0.000133812)0.10:20,EPI_ISL_578194:22):0);"

tree = Phylo.read(StringIO(treeData), "newick")
# Phylo.draw_ascii(tree)
# Phylo.draw(tree)

lenForCount = 1e-04
for cld in tree.clade:
    DFS(cld, lenForCount, 0)

outputFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output.txt'
DateFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output_CollectionDate_count.txt'

printClustersToFile()
analyzeTree(color, CSVInfo)
printCollectionDataDictionaryToFile()
