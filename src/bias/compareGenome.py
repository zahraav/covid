from utilities.ReadAndWrite import saveToCsv
import csv


def save_csv(file_name, csv_list, is_first_time_using_header):
    """
    This method save the data into CSV file
    :param file_name: Name of CSV file
    :param csv_list: list of Data for saving on csv file
    :param is_first_time_using_header:  flag for indicating whether it's the first time sending data to a CSV file
    if it's the first time, it means the filed names will be written too.
    :return:
    """
    field_names = ['id', 'date', 'location', 'technology', 'index', 'Letter', 'reference Letter']
    saveToCsv(file_name, csv_list, field_names, is_first_time_using_header)


def makeReferenceGenomeFileWithoutExtraEnter(referenceFastaFile, newFile):
    """
    There are some new line at the end of every line in reference genome,
    this method remove those new lines at the end of the line and generate a new file without those errors.
    :param referenceFastaFile: input file of reference genome.
    :param newFile: new reference genome file without enter at the end of the lines.
    :return:
    """
    with open(newFile, "a") as output_handle:
        with open(referenceFastaFile) as reference:
            for rLine in reference:
                if rLine.__contains__('>'):
                    continue
                else:
                    output_handle.write(rLine.rstrip())


def compareGenome(referenceGenome):
    """
    # TODO
    :param referenceGenome:
    :return:
    """
    # referenceFasta = "files/ReferenceSequence.fasta"
    # referenceFastaWithoutHeader = "files/ReferenceSequence_2.fasta"
    newReferenceGenome = referenceGenome.replace('.fasta', 'WithoutHeaderAndExtraLine.fasta')
    makeReferenceGenomeFileWithoutExtraEnter(referenceGenome, newReferenceGenome)

    csvFile = 'files/Msa_NoSpace_withExtraLetter.csv'
    outFile = 'files/Msa_2060_withReferenceLetter.csv'

    isFirstRow = True

    with open(csvFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstRow:
                isFirstRow = False
                continue
            index = row[4]
            rLetter = ''
            with open(newReferenceGenome) as RFastaFile:
                for line in RFastaFile:
                    rLetter = line[int(index)]
            row.append(rLetter)
            save_csv(outFile, row, isFirstRow)
