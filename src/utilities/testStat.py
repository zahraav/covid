import csv
import math

from ReadAndWrite import saveToCsv

is_header = True
inputFile = 'files/test_MSA_2.csv'
with open(inputFile, 'r') as file:
    reader = csv.reader(file)
    isReadHeader = False
    for row in reader:
        statInfo = {'N1': 0, 'L1': 0, 'N2': 0, 'L2': 0, 'L_joint': 0, 'T': 0}
        if isReadHeader is False:
            isReadHeader = True
            continue

        for i in range(1, 7, ):
            prop = int(row[i]) / int(row[0])
            result = 0 if prop == 0 else prop * math.log10(prop)
            statInfo['L1'] = +statInfo['L1'] + result
        statInfo['N1'] = int(row[0])

        for i in range(8, 13, ):
            prop = int(row[i]) / int(row[7])
            result = 0 if prop == 0 else prop * math.log10(prop)
            statInfo['L2'] = +statInfo['L2'] + result
        statInfo['N2'] = int(row[7])

        for i in range(1, 7, ):
            nsum = int(row[i]) + int(row[i + 7])
            sum = int(row[0]) + int(row[7])
            prop = nsum / sum
            result = 0 if prop == 0 else prop * math.log10(prop)
            statInfo['L_joint'] = +statInfo['L_joint'] + result

        statInfo['T'] = 2 * (statInfo['N1'] * statInfo['L1'] + statInfo['N2'] * statInfo['L2'] - (
                statInfo['N1'] + statInfo['N2']) * statInfo['L_joint'])

        #        print(statInfo.values())

        saveToCsv(inputFile.replace('.csv', '_testStat.csv'), statInfo.values(),
                  ['N1', 'L1', 'N2', 'L2', 'L_joint', 'T'], is_header)
        is_header = False
