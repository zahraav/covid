from utilities.ReadAndWrite import saveToCsv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    fieldNames = ['id', 'reference', 'seq','date', 'location', 'technology', 'index']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)



referenceFasta = "files/ReferenceSequence.fasta"
fastaFile = "files/test_2.fasta"
referenceSeq = ''
compareFile = fastaFile.replace(".fasta", "_compareToReference.csv")
with open(referenceFasta) as referenceFile:
    for rLine in referenceFile:
        if rLine.__contains__('>'):
            continue
        else:
            referenceSeq = referenceSeq+ rLine.rstrip()
            print(referenceSeq)

firstTimeUsingHeader = True


with open(fastaFile) as infile:
    for fLine in infile:
        fLine = fLine.rstrip()
        if fLine.__contains__('>'):
            header = fLine
            headerSplit = header.split(r'|')
            seqId = headerSplit[1]
            date = headerSplit[2]
            location = headerSplit[3]
            technology = headerSplit[4]

        else:
            indexCounter = 0

            for referenceNucleotide, N in zip(referenceSeq, fLine):
                print(indexCounter)
                if referenceNucleotide != N:
                    saveCSV(compareFile,[seqId, referenceNucleotide, N, date, location, technology, indexCounter],firstTimeUsingHeader)
                    firstTimeUsingHeader = False
                    print(N)
                indexCounter += 1


