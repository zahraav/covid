#from feature import Info
import csv


def parseFastafile(fasta_address):
    # infoDictionary = {}
    # FastaFileLineCounter = 0
    index=0

    seqTech = ''
    with open(fasta_address) as infile:
        for line in infile:
            line = line.strip()
            if line.__contains__('>'):
                # infoDictionary[FastaFileLineCounter] = Info(line)
                if line.__contains__('Illumina'):
                    seqTech = 'Illumina'
                    index=index+7
                elif line.__contains__('Nanopore'):
                    seqTech = 'Nanopore'
                    index=0
                else:
                    seqTech = 'NA'
                print(line)
            elif not '>' in line and seqTech == 'NA':
                #for i in range(2, len(line) - 2):
                print('a', seqTech)

    with open('files/csvTest.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f' {", ".join(row)}')
                line_count += 1
            else:
                NCount=int(row[index])
                NCount+=1

                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


parseFastafile('files/test_MSA.fasta')
