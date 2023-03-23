import csv
import os


def findAssemblyMethod(accessionId, inputAddress):
    # TSVFile = "files/output/BarCharts/TSVFiles/mergedFile_1.tsv"
    with open(inputAddress, 'r') as f:
        csv_reader = csv.reader(f)
        # ignore header
        for line in csv_reader:
            x = line[0].split("\t")
            if x[1] == accessionId:
                if x.__len__() >= 10:
                    return x[9]

    return '-'


def newAccessionFile(accessionFileAddress, tsvFilesAddress):
    newAddress = accessionFileAddress.replace(".csv", "_n.csv")
    with open(newAddress, 'w', encoding='UTF8', newline='') as fWriter:
        writer = csv.writer(fWriter)
        with open(accessionFileAddress, 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                print(line)
                if line[1] == '-':
                    assemblyMethod=findAssemblyMethod(line[0], tsvFilesAddress)
                    writer.writerow([line[0], assemblyMethod])
                else:
                    writer.writerow(line)
    return newAddress


def ignoreLetters(inputAddress, outputAddress):
    accessionIds = set()
    with open(outputAddress, 'w', encoding='UTF8', newline='') as fWriter:
        writer = csv.writer(fWriter)
        # writer.writerow(["id", "assemblyMethod"])
        with open(inputAddress, 'r') as fReader:
            csv_reader = csv.reader(fReader)
            next(csv_reader)
            for line in csv_reader:
                accessionIds.add(line[0])

        for x in accessionIds:
            writer.writerow([x, '-'])


def addProtocolToMSAFile():
    # input_file = "files/Msa_NoSpace_withExtraLetter.csv"
    inputFile = "files/test_Msa_withExtraLetter.csv"
    outputFile = inputFile.replace("_withExtraLetter.csv", "_withoutLetter.csv")


    # TSVFiles = "files/output/BarCharts/TSVFiles/mergedFile_1.tsv"
    #TSVFiles = "files/output/BarCharts/test/test_mergedFile_1.tsv"
    # addProtocolToMSAFile(input_file)
    # drawProtocolChart("files/test_Msa_withExtraLetter_withProtocol.csv")
    #ignoreLetters(input_file, outputFile)
    #newAccessionFile(outputFile, TSVFiles)

    # directory = 'files/output/BarCharts/TSVFiles'
    directory = 'files/output/BarCharts/test'

    # iterate over files in
    # that directory
    ignoreLetters(inputFile, outputFile)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            # newAccessionFile(outputFile, TSVFiles)
            outputFile = newAccessionFile(outputFile, f)


addProtocolToMSAFile()
