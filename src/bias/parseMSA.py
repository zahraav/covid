import csv


def saveToCsv(fileName, csvList, isHeader):
    """
    :param fileName: address of the CSV file
    :param csvList: list of one line of data for writing on the CSV file
    :param isHeader: It shows whether it is the first time this method is called or not.
    If so, isHeader is going to be true. As a result, the method prints the header fields on the CSV file.
    :return: True, if it generates the file. False if it throws any exceptions.
    """
    fieldNames = ['id', 'date', 'location', 'technology', 'index', 'letter']
    # fieldNames = ['id', 'date', 'location']
    dictX = {}
    for name, elem in zip(fieldNames, csvList):
        dictX[name] = str(elem)
    with open(fileName, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isHeader:
            writer.writeheader()
        writer.writerow(dictX)


"""
This code separate the sequences with IUPAC codes and the ones without IUPAC codes and 
save them in the csv file and also make a new fasta file that contaings with the IUPAC codes  
"""
# fastaFile = "files/input/test_MSA_2.fasta"
fastaFile = "files/input/msa_0206.fasta"
outFastaFile = fastaFile.replace(".fasta", "_withExtraLetter.fasta")
firstTimeUsingHeader = True
nucleotideList = ['A', 'C', 'G', 'T', 'N', '-']
with open(fastaFile) as infile:
    for line in infile:
        line = line.rstrip()
        if line.__contains__('>'):
            header = line
            headerSplit = header.split(r'|')
            seqId = headerSplit[1]
            date = headerSplit[2]
            location = headerSplit[3]
            # technology = headerSplit[4]

        else:
            newLetterIndex = 0
            letterIndicesForFile = ' '
            for x in line:
                if x not in nucleotideList:
                    letterIndicesForFile = letterIndicesForFile + ' ' + str(newLetterIndex)

                    # saveCSV(fastaFile.replace('.fasta', '_withExtraLetter.csv'),
                    #        [seqId, date, location, technology, newLetterIndex, x], firstTimeUsingHeader)
                    firstTimeUsingHeader = False

                newLetterIndex += 1

            if letterIndicesForFile != ' ':
                letterIndicesForFile = letterIndicesForFile.lstrip()
                """with open(outFastaFile, 'a', encoding='utf-8') as f1:
                    f1.write(str(letterIndicesForFile))
                    f1.write(' | ')
                    f1.write(seqId)
                    f1.write(' ')
                    f1.write(header)
                    f1.write('\n')
                    f1.write(line)
                    f1.write('\n')"""
            else:
                saveToCsv(fastaFile.replace('.fasta', '_withoutLetter.csv'),
                          [seqId, date, location], False)
