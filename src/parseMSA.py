from utilities.ReadAndWrite import saveToCsv


def saveCSV(fileName, csvList, isFirstTimeUsingHeader):
    fieldNames = ['id', 'date', 'location', 'technology', 'index', 'letter']
    saveToCsv(fileName, csvList, fieldNames, isFirstTimeUsingHeader)


fastaFile = "files/test_2.fasta"
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
            technology = headerSplit[4]

        else:
            newLetterIndex = 0
            letterIndicesForFile = ' '
            for x in line:
                if x not in nucleotideList:
                    letterIndicesForFile = letterIndicesForFile + ' ' + str(newLetterIndex)

                    saveCSV(fastaFile.replace('.fasta', '_withExtraLetter.csv'),
                            [seqId, date, location, technology, newLetterIndex, x], firstTimeUsingHeader)
                    firstTimeUsingHeader = False

                newLetterIndex += 1

            if letterIndicesForFile != ' ':
                letterIndicesForFile = letterIndicesForFile.lstrip()
                with open(fastaFile.replace(".fasta", "_withExtraLetter.fasta"), 'a', encoding='utf-8') as f1:
                    f1.write(str(letterIndicesForFile))
                    f1.write(' | ')
                    f1.write(seqId)
                    f1.write(' ')
                    f1.write(header)
                    f1.write('\n')
                    f1.write(line)
                    f1.write('\n')
