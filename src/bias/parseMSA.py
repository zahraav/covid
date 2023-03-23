import csv


def save_to_csv(file_name, csv_list, is_header):
    """
    :param file_name: address of the CSV file
    :param csv_list: list of one line of data for writing on the CSV file
    :param is_header: It shows whether it is the first time this method is called or not.
    If so, is_header is going to be true. As a result, the method prints the header fields on the CSV file.
    :return: True, if it generates the file. False if it throws any exceptions.
    """
    field_names = ['id', 'date', 'location', 'technology', 'index', 'letter']
    # field_names = ['id', 'date', 'location']
    dict_x = {}
    for name, elem in zip(field_names, csv_list):
        dict_x[name] = str(elem)
    with open(file_name, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        if is_header:
            writer.writeheader()
        writer.writerow(dict_x)


"""
This code separate the sequences with IUPAC codes and the ones without IUPAC codes and 
save them in the csv file and also make a new fasta file that contaings with the IUPAC codes  
"""
# fasta_file = "files/input/test_MSA_2.fasta"
# fastaFile = "files/input/msa_0206.fasta"
fastaFile = "files/Msa_NoSpace_without_reference_genome.fasta"
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
            technology = headerSplit[4]

        else:
            newLetterIndex = 0
            letterIndicesForFile = ' '
            for x in line:
                if x not in nucleotideList:
                    letterIndicesForFile = letterIndicesForFile + ' ' + str(newLetterIndex)

                    # saveCSV(fasta_file.replace('.fasta', '_withExtraLetter.csv'),
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
                save_to_csv(fastaFile.replace('.fasta', '_withoutLetter.csv'),
                            [seqId, date, location,technology], False)
