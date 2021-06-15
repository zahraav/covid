from Bio import Phylo
from io import StringIO
import csv
from datetime import datetime

def drawChart(x,y):
    print(x,y)


def daysDifference(firstDate, secondDate):
    """
    Days differences between two Date
    :param firstDate: first Date
    :param secondDate: second Date
    :return: differences
    """
    firstDate = datetime.strptime(firstDate, "%Y-%m-%d")
    secondDate = datetime.strptime(secondDate, "%Y-%m-%d")
    return abs((secondDate - firstDate).days)


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


'''def getMinAndMaxDate(treeNameList, csvDict):
    """
    return the min and the max of time in the DFS base on Dictionary
    :param nameList: id(name)
    :param csvDict: dictionary base on CSV file [name,[info,date]]
    :return: minName, maxName
    """
    minId, maxId = '', ''
    minDate = datetime.now()
    maxDate = datetime.strptime("2019-01-01", "%Y-%m-%d")

    for name in treeNameList:
        if csvDict.keys().__contains__(name):
            tempDate = csvDict[name][1]
            date_dt3 = datetime.strptime(tempDate, '%Y-%m-%d')
            if date_dt3 < minDate:
                minId = name
                minDate = date_dt3
            if date_dt3 > maxDate:
                maxId = name
                maxDate = date_dt3
    return minId, maxId
'''


def DFSTree(dfsTree, csvDict, minId, maxId, minDate, maxDate):
    """
    DFS which returning ids list of Phylogenic Tree
    :param dfsTree:
    :param csvDict:
    :param minId:
    :param maxId:
    :param minDate:
    :param maxDate:
    :return:
    """
    idsList = []
    collectionDateList=[]
    for elem in dfsTree.get_terminals():
        if elem.is_terminal():
            leafName = str(elem)
            if csvDict.keys().__contains__(leafName):
                idsList.append(leafName)
                tempDate = csvDict[leafName][1]
                date_dt3 = datetime.strptime(tempDate, '%Y-%m-%d')

                collectionDateList.append(date_dt3)

                if date_dt3 < minDate:
                    minId = leafName
                    minDate = date_dt3
                if date_dt3 > maxDate:
                    maxId = leafName
                    maxDate = date_dt3

        else:
            return DFSTree(elem, csvDict, minId, maxId, minDate, maxDate)
    return minId, maxId, idsList, collectionDateList


def readNewickTree(inputFile):
    output=''
    with open(inputFile) as infile:
        for line in infile:
            output += line
    return output


# treeData = readNewickTree('files/GISAID-hCoV-19-phylogeny-2021-06-03/global.tree')

treeData = "(EPI_ISL_2286709:1,(EPI_ISL_1827532:5e-09,EPI_ISL_1827511:5e-09)0.810:3.345e-05," \
           "(EPI_ISL_1827534:0.000133832),(EPI_ISL_413691:3,EPI_ISL_428476:2,(EPI_ISL_1882518:5,EPI_ISL_1883136 " \
           ":3)0.290:5e-09):1,(EPI_ISL_579303:6.7017e-05,(EPI_ISL_2293766:3.3859e-05,(EPI_ISL_1827537:0.000100482," \
           "EPI_ISL_2293886:6.7018e-05))):0); "


tree = Phylo.read(StringIO(treeData), "newick")
#Phylo.draw_ascii(tree)


cladeLen = len(tree.clade.get_nonterminals())
CSVInfo = returnCSVList('files/GISAID-hCoV-19-phylogeny-2021-06-03/metadata.csv')

for cld in tree.clade:
    minDate = datetime.now()
    maxDate = datetime.strptime("2019-01-01", "%Y-%m-%d")

    minId, maxId, idList, collectionDateList = DFSTree(cld, CSVInfo, '', '', minDate, maxDate)
    #print(minId, maxId)
    drawChart(idList,collectionDateList)

    t1, t2 = '', ''
    if minId != '' and maxId != '':
        dd=daysDifference(CSVInfo[minId][1], CSVInfo[maxId][1])
        print(dd , len(idList),'   ',(dd/len(idList)))

 #   print('====')