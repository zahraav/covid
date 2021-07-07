from Bio import Phylo
from io import StringIO
import csv
from datetime import datetime

color = {}

CollectionDateArray = [0, 0]  # min,max
collectionDateList = []
MinMaxCollectionDateDictionary = {}
minMaxArray = [0, datetime.now(), datetime.strptime("2019-01-01", "%Y-%m-%d")]  # leaf, min, max


def analyzeTree(DFSTreeDictionary, CSVDictionary):

    for leaf in DFSTreeDictionary:  # from Tree [leaf, cluster]
        # for CSVNode in CSVDictionary:  # csv file [leaf, [metadata->[info, collectionDate]]
        if CSVDictionary.keys().__contains__(leaf):
            minDate = datetime.now()
            maxDate = datetime.strptime("2019-01-01", "%Y-%m-%d")

            if MinMaxCollectionDateDictionary != {} and\
                    MinMaxCollectionDateDictionary.keys().__contains__(DFSTreeDictionary[leaf]):
                # {cluster: [minDate , MaxDate]}
                minDate = MinMaxCollectionDateDictionary[DFSTreeDictionary[leaf]][1]
                maxDate = MinMaxCollectionDateDictionary[DFSTreeDictionary[leaf]][2]
            else:
                MinMaxCollectionDateDictionary[DFSTreeDictionary[leaf]] = [DFSTreeDictionary[leaf], minDate,
                                                                           maxDate]

            date_dt3 = datetime.strptime(CSVDictionary[leaf][1], '%Y-%m-%d')
            if minDate > date_dt3:  # min > collection date[leaf]
                MinMaxCollectionDateDictionary[DFSTreeDictionary[leaf]][1] = date_dt3
            if maxDate < date_dt3:  # max < collection date[leaf]
                MinMaxCollectionDateDictionary[DFSTreeDictionary[leaf]][2] = date_dt3

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
# print(CSVInfo)

#treeData = "(EPI_ISL_406801:0,((EPI_ISL_1712380:0.000133812)0.10:20,EPI_ISL_578194:22):0);"

tree = Phylo.read(StringIO(treeData), "newick")
# Phylo.draw_ascii(tree)

# Phylo.draw(tree)

lenForCount = 1e-04
for cld in tree.clade:
    DFS(cld, lenForCount, 0)

outputFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output.txt'
DateFile = 'files/GISAID-hCoV-19-phylogeny-2021-06-03/output_CollectionDate.txt'
with open(outputFile, '+a') as outfile:
    for cl in color:
        outfile.write(cl)
        outfile.write('  : ')
        outfile.write(str(color[cl]))
        outfile.write('\n')
        # print(cl, color[cl])
    # print(color)

analyzeTree(color, CSVInfo)
#print(color)
with open(DateFile, '+a') as dateFile:
    for mmd in MinMaxCollectionDateDictionary:
        dateFile.write(str(mmd))
        dateFile.write('  : ')
        dateFile.write(str(MinMaxCollectionDateDictionary[mmd][1]))
        dateFile.write(', ')
        dateFile.write(str(MinMaxCollectionDateDictionary[mmd][2]))
        dateFile.write('\n')


#print(MinMaxCollectionDateDictionary)
#Phylo.draw_ascii(tree)