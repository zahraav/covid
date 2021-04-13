from utilities.ReadAndWrite import saveToCsv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    fieldNames = ['id', 'reference', 'seq', 'index']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)


referenceFasta = "files/reftest_2.fasta"
fastaFile = "files/test_2.fasta"
referenceSeq = ''
compareFile = fastaFile.replace(".fasta", "_compareToReference.csv")
with open(referenceFasta) as referenceFile:
    for rLine in referenceFile:
        if rLine.__contains__('>'):
            continue
        else:
            referenceSeq = rLine.rstrip()


firstTimeUsingHeader = True

indexCounter = 0
with open(fastaFile) as infile:
    for fLine in infile:
        fLine = fLine.rstrip()
        if fLine.__contains__('>'):
            header = fLine
            headerSplit = header.split(r'|')
            print(headerSplit)
            seqId = headerSplit[1]
        else:
            for referenceNucleotide, N in zip(referenceSeq, fLine):
                if referenceNucleotide != N:
                    saveCSV(compareFile,[seqId, referenceNucleotide, N, indexCounter],firstTimeUsingHeader)
                    firstTimeUsingHeader = False

                indexCounter += 1


