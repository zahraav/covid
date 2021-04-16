import csv
import matplotlib.pyplot as plt

from utilities.ReadAndWrite import saveDictionary, saveData, saveSimpleDictionary

#number of column for letters can be used when counting a sequence for multiple times is not important
def ReturnColumnDictionary(columnNum):
    columnDict = {}
    isFirstRow = True
    with open('files/Msa_NoSpace_withExtraLetter.csv') as csv_file:
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


def barChart(clmnDictionary):
    """
    plt.bar(xAxis,yAxis)
    plt.title('title name')
    plt.xlabel('xAxis name')
    plt.ylabel('yAxis name')
    plt.show()
"""
    xAxis = clmnDictionary.keys()
    yAxis = clmnDictionary.values()

    plt.bar(xAxis, yAxis)
    plt.savefig('files/letterBar.png', dpi=400)
    plt.show()


columnNumber = 5
columnDictionary = ReturnColumnDictionary(columnNumber)
savingAddress = 'files/BarChartDictionaries/column_' + str(columnNumber) + '_Dictionary_Letter.txt'
saveSimpleDictionary(columnDictionary, savingAddress)
barChart(columnDictionary)
