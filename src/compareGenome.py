from utilities.ReadAndWrite import saveToCsv
import csv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    fieldNames = ['id', 'date', 'location', 'technology', 'index', 'Letter', 'reference Letter']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)


def makeReferenceGenomeFileWithoutExteraEnter(referenceFastaFile, newFile):
    with open(newFile, "a") as output_handle:
        with open(referenceFastaFile) as reference:
            for rLine in reference:
                if rLine.__contains__('>'):
                    continue
                else:
                    output_handle.write(rLine.rstrip())


referenceFasta = "files/ReferenceSequence.fasta"
referenceFastaWithoutHeader = "files/ReferenceSequence_2.fasta"
makeReferenceGenomeFileWithoutExteraEnter(referenceFasta, referenceFastaWithoutHeader)

csvFile = 'files/Msa_NoSpace_withExtraLetter.csv'
outFile = 'files/Msa_2060_withReferenceLetter.csv'

idList = []
isFirstRow = True

with open(csvFile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if isFirstRow:
            isFirstRow = False
            continue
        index = row[4]
        rLetter = ''
        with open(referenceFastaWithoutHeader) as RFastaFile:
            for line in RFastaFile:
                rLetter = line[int(index)]
        row.append(rLetter)
        saveCSV(outFile, row, isFirstRow)
