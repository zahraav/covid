import csv

from utilities.ReadAndWrite import saveToCsv


def saveCSV(fileName, csvList, isHeader):
    fieldNames = ['id', 'location', 'letter']
    saveToCsv(fileName, csvList, fieldNames, isHeader)


fastaFile = "files/test_2.fasta"
isHeader = True
nucleotideList = ['A', 'C', 'G', 'T', '.', '-']
with open(fastaFile) as infile:
    for line in infile:
        line = line.rstrip()
        if line.__contains__('>'):
            header = line
            id = header.split(r'|')[1]
        else:
            newLetterIndex = 0
            letterIndicesForFile = ' '
            for x in line:
                if x not in nucleotideList:
                    letterIndicesForFile = letterIndicesForFile + ' ' + str(newLetterIndex)

                    saveCSV(fastaFile.replace('.fasta','_withExtraLetter.csv'),[id, newLetterIndex, x],isHeader)
                    isHeader = False

                newLetterIndex += 1

            if letterIndicesForFile is not ' ':
                letterIndicesForFile = letterIndicesForFile.lstrip()
                with open(fastaFile.replace(".fasta", "_withExtraLetter.fasta"), 'a', encoding='utf-8') as f1:
                    f1.write(str(letterIndicesForFile))
                    f1.write(' | ')
                    f1.write(id)
                    f1.write(' ')
                    f1.write(header)
                    f1.write('\n')
                    f1.write(line)
                    f1.write('\n')
                print(letterIndicesForFile, ': ', id, ' - ', header, '\n', line)


with open('employee_file2.csv', mode='w') as csv_file:
    fieldnames = ['emp_name', 'dept', 'birth_month']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

# یه فایل اکسل اینا رو اضافه کنم هر بار حرف جدید دیدم
