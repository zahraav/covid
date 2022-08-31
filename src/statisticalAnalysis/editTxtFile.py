import csv


def generateCSVFile(inputFile, csvOutput, csvHeader):
    with open(csvOutput, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)

        with open(inputFile) as infile:
            for line in infile:
                data = line.split(' ')
                data = list(filter(None, data))
                newData = []
                for x in data:
                    if x.__contains__('\n'):
                        newData.append(x.replace("\n", ""))
                    elif x.__contains__(':'):
                        pass
                    else:
                        newData.append(x)
                writer.writerow(newData)


header = ['Nanopore', 'A', 'C', 'G', 'T', 'N', 'Gap', 'Illumina', 'A', 'C', 'G', 'T', 'N', 'Gap', 'P_value', 'A',
          'C', 'G', 'T']
generateCSVFile('files/output/statisticalAnalysis/Canada_NucleotidcountDictionary.txt',
                'files/output/statisticalAnalysis/p_valueAll.csv', header)

# header = ['n in Nanopore', 'n in Illumina', 'not n in Nanopore', 'not n in Illumina', 'p_value']
# generateCSVFile('files/output/statisticalAnalysis/p_value.txt', 'files/output/statisticalAnalysis/p_value.csv',header)
