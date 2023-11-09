import csv
import os
import configparser
import datetime

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def get_date_from_header_line(header):
    """
    date in yyyy/mm/dd format
    This method get a header line of a fasta file and returns the collectionDate from the header.
    :param header: A header line of a fasta file
    :return: CollectionDate
    """
    split_header = header.split('|')
    x = get_date(split_header[2])
    return x


def get_date(temp_date):
    """
    temp Date is Date but in string format, so this method make a date from tempDate and return it
    :param temp_date:
    :return: Date
    """
    cd = temp_date.split('-')
    if cd.__len__() == 2 or int(cd[2]) == 0:  # some collection dates in GisAid doesn't have day.
        cd[2] = 1
    if int(cd[1]) == 0:
        cd[1] = 1

    return datetime.datetime(int(cd[0]), int(cd[1]), int(cd[2]))


def is_in_the_peak(peak, temp_time):
    return True if peak[0] < temp_time < peak[1] else False


"""
save IUPAC Nucleotide Codes into 5 number  
"""
ChangedIUPACNucleotideCodes = {'A': 0, 'W': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 1, 'Y': 1,
                               'B': 1, 'H': 1, 'G': 2, 'S': 2, 'R': 2, 'K': 2, 'T': 3,
                               'U': 3, 'N': 4, '-': 5, '.': 5}

IUPACNucleotideCodes = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'U': 4, 'R': 5, 'Y': 6, 'S': 7,
                        'W': 8, 'K': 9, 'M': 10, 'B': 11, 'D': 12, 'H': 13, 'V': 14,
                        'N': 15, '-': 16, '.': 16}


def analyze_fasta(in_fasta_file, codes_dictionary):
    """
    This method get a fasta_file as an input and make a dictionary which contains two arrays
    for different sequence technologies (Nanopore and Illumina). Each of these arrays contains
    some arrays for every index in the sequence in fasta file.
    and in the arrays in every index there is number which shows the count of that nucleotide
    in sequences that used that sequence technology.
    This method is make the arrays with all IUPAC codes.
    :param codes_dictionary: Dictionary that contains the codes
    :param in_fasta_file: input fasta file
    :return: dictionary contains two array one for Nanopore and one for Illumina.
    """

    header_line = 1
    type_ = 'none'
    stats = {'Nanopore': [], 'Illumina': []}

    with open(in_fasta_file, 'r') as fasta_file:
        for line in fasta_file:
            if header_line == 0:
                header_line = 1

                if type_ != 'Nanopore' and type_ != 'Illumina':
                    continue
                pos = 0
                for ch in line.strip().rstrip():
                    if len(stats[type_]) == pos:
                        stats[type_].append([0] * len(set(codes_dictionary.values())))
                    stats[type_][pos][codes_dictionary[ch]] = \
                        stats[type_][pos][codes_dictionary[ch]] + 1

                    pos = pos + 1
                continue
            header_line = 0
            header = line.strip().rstrip().split("|")
            type_ = header[-1]

        return stats


def save_to_csv(csv_file, csv_list, field_names, is_header):
    """
     is_header should set to true for the first time then it should set to false for rest of calls
    this print the header in CSV file.
     if it doesn't set to false it will print the header for every line.
    :param csv_file:
    :param csv_list:
    :param field_names:
    :param is_header:
    :return:
    """
    x = {}
    for name, elem in zip(field_names, csv_list):
        x[name] = str(elem)
    with open(csv_file, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        if is_header:
            writer.writeheader()
        writer.writerow(x)


def print_stats(stats, header, is_header, number_of_element, is_iupac_code):
    """
    :param is_iupac_code: show if the codes are from IUPAC code or not
    :param stats:
    :param header:
    :param is_header:
    :param number_of_element:
    :return: CSV File
    """
    csv_file = config['outputAddresses'].get('csv_file')
    if is_iupac_code:
        csv_file = csv_file.replace('.csv', 'IUPAC.csv')

    for n_elem, i_elem in zip(stats['Nanopore'], stats['Illumina']):
        csv_list = [sum(n_elem)]
        for k in n_elem:
            csv_list.append(k)
        csv_list.append(sum(i_elem))
        for n in i_elem:
            csv_list.append(n)
        percent_csv_list = csv_list.copy()

        for i in range(1, number_of_element - 1, ):
            if percent_csv_list[0] == 0:
                percent_csv_list[i] = 0
            else:
                percent_csv_list[i] = percent_csv_list[i] / percent_csv_list[0] * 100

            if percent_csv_list[number_of_element] == 0:
                percent_csv_list[i + number_of_element] = 0
            else:
                percent_csv_list[i + number_of_element] = \
                    percent_csv_list[i + number_of_element] / percent_csv_list[number_of_element] * 100

        save_to_csv(csv_file, csv_file, header, is_header)
        save_to_csv(csv_file.replace(".csv", "Percentage.csv"), percent_csv_list, header, is_header)
        is_header = False
    return csv_file


def parse(input_file):
    """
    This method gets a fasta file as an input, then sends the file to analyzeFasta() method,
    and as a result, it gets a dictionary full of nucleotide's count in every index in sequence
    for different sequence technology. Then it saves them in two files, one CSV file that contains
    count and another one is a CSV file that contains the percentage.
    :param input_file: fasta file (MSA file)
    :return: CSV file
    """
    is_header = True
    stats = analyze_fasta(input_file, ChangedIUPACNucleotideCodes)
    iupac_stats = analyze_fasta(input_file, IUPACNucleotideCodes)

    csv_file = print_stats(stats,
                           ['nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', 'Illumina- sum', 'A2', 'C2', 'G2',
                            'T2', 'N2', 'GAP2'], is_header, 7, False)

    iupac_header = ['nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'U1', 'R1', 'Y1', 'S1', 'W1', 'K1',
                    'M1', 'B1', 'D1', 'H1', 'V1', 'N1', 'Gap1', 'Illumina- sum', 'A2', 'C2',
                    'G2', 'T2', 'U2', 'R2', 'Y2', 'S2', 'W2', 'K2', 'M2', 'B2', 'D2', 'H2', 'V2',
                    'N2', 'Gap2']

    print_stats(iupac_stats, iupac_header, is_header, 18, True)
    return csv_file


def get_consensus(max_nucleotide):
    """
    This method take a list of Nucleotides that have the same count in the one cut and return the consensus for that
    index.
    :param max_nucleotide: List of nucleotides with same count in a cut
    :return: IUPAC code of the nucleotides
    in the list
    """
    if max_nucleotide.__len__() == 2:
        if max_nucleotide.__contains__('A1') or max_nucleotide.__contains__('A2'):
            if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):  # ['A','G']-->'R'
                return 'R'

            if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):  # ['A','T']-->'W'
                return 'W'

            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):  # ['C','A']-->'M'
                return 'M'

        if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):
            if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):  # ['C','T']-->'Y'
                return 'Y'

        if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):
            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):  # ['C','G']-->'S'
                return 'S'

        if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):
            if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):  # ['T','G']-->'K'
                return 'K'

    if max_nucleotide.__len__() == 3:
        if max_nucleotide.__contains__('A1') or max_nucleotide.__contains__('A2'):
            if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):
                if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):  # ['A','G','T]-->'D'
                    return 'D'

        if max_nucleotide.__contains__('A1') or max_nucleotide.__contains__('A2'):
            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):
                if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):  # ['A','C','T]-->'H'
                    return 'H'

        if max_nucleotide.__contains__('A1') or max_nucleotide.__contains__('A2'):
            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):
                if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):  # ['A','C','G]-->'V'
                    return 'V'

        if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):
            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):
                if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):  # ['T','C','G]-->'B'
                    return 'B'

    if max_nucleotide.__len__() == 4:
        if max_nucleotide.__contains__('A1') or max_nucleotide.__contains__('A2'):
            if max_nucleotide.__contains__('C1') or max_nucleotide.__contains__('C2'):
                if max_nucleotide.__contains__('G1') or max_nucleotide.__contains__('G2'):
                    if max_nucleotide.__contains__('T1') or max_nucleotide.__contains__('T2'):
                        return 'N'
    return '.'


def return_correct_value(i):
    """
    This method check if the data is on the header or is a normal data
    then if it's from header change the header from csv to header to save in the transfacFormat txt file
    :param i: the header item
    :return: header in transfac format or data
    """
    header = ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1',
              '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2', 'GAP2']

    if header.__contains__(i):
        # for converting A1,A2,C1,C2 which remained from csv to ... to A,A,C, ...
        return i[0]
    else:
        return i


def transfac_generator(csv_file, transfac_file_address):
    """
    This Method gets a csv file as an input and generate a transfac format file
    :param transfac_file_address: transfac format file which is going to saved on the transfac_file_address
    :param csv_file: input file, contains all data to transfer into csv format
    :return:
    """
    header = ['index', 'A1', 'C1', 'G1', 'T1', 'consensus1', 'A2', 'C2', 'G2', 'T2', ' consensus2']
    line_counter = 0
    with open(transfac_file_address, 'w') as out_file:

        out_file.write("XX")
        out_file.write("\n")
        out_file.write("ID  .....")
        out_file.write("\n")
        out_file.write("XX")
        out_file.write("\n")

        with open(csv_file, newline='') as csv_file:

            for row in csv.reader(csv_file):
                column_count = 1
                max_nucleotide = []
                if line_counter == 0:  # header Line
                    # newCsvLine.append('PO')
                    out_file.write('P0')
                    out_file.write("\t")
                    max_nucleotide = ['-']
                else:
                    # newCsvLine = [str(line_counter)]
                    out_file.write(str(line_counter))
                    out_file.write("\t")
                max_in_line = 0
                for i in row[1:5]:
                    if line_counter != 0:
                        if int(i) > int(max_in_line):
                            max_in_line = i
                            max_nucleotide = [header[column_count]]
                        elif int(i) == int(max_in_line):
                            max_nucleotide.append(header[column_count])

                    out_file.write(return_correct_value(i))
                    out_file.write("\t")
                    column_count = column_count + 1

                if max_nucleotide.__len__() > 1:
                    max_nucleotide = [get_consensus(max_nucleotide)]

                out_file.write(max_nucleotide[0][0])
                out_file.write("\t")

                max_nucleotide.clear()
                max_in_line = 0
                column_count = 6
                for i in row[8:12]:
                    if line_counter != 0:
                        if int(i) > int(max_in_line):
                            max_in_line = i
                            max_nucleotide = [header[column_count]]
                        elif int(i) == int(max_in_line):
                            max_nucleotide.append(header[column_count])

                    out_file.write(return_correct_value(i))
                    out_file.write("\t")
                    column_count = column_count + 1

                if max_nucleotide.__len__() > 1:
                    max_nucleotide = [get_consensus(max_nucleotide)]
                if max_nucleotide.__len__() == 0:
                    max_nucleotide = ['-']
                out_file.write(max_nucleotide[0][0])
                out_file.write("\n")
                # newCsvLine.append(max_nucleotide[0][0])

                line_counter = line_counter + 1

        out_file.write("XX")
        out_file.write("\n")
        out_file.write("CC Program: ")
        out_file.write("\n")
        out_file.write("XX")
        out_file.write("\n")
        out_file.write("\\\\")
        out_file.write("\n")


def separate_peaks(fasta_file, peak_one_dates, peak_two_dates, peak_three_dates):
    """
    This Function separate sequences in every peak and save them in a different file,
    so That we can make a charts and other analysis by using each of these files.
    :param fasta_file: The main fasta file containing all data.
    :param peak_one_dates: The list for first peak [start Date,end Date]
    :param peak_two_dates: The list for second peak [start Date,end Date]
    :param peak_three_dates: The list for third peak [start Date,end Date]
    :return:
    """

    first_peak_fasta = config['outputAddresses'].get('first_peak')
    second_peak_fasta = config['outputAddresses'].get('second_peak')
    third_peak_fasta = config['outputAddresses'].get('third_peak')

    # open three fasta files to separate sequences of each peak on a different file
    first_peak = open(first_peak_fasta, "w")
    second_peak = open(second_peak_fasta, "w")
    third_peak = open(third_peak_fasta, "w")

    flag = 0

    with open(fasta_file) as mainFastaFile:
        for line in mainFastaFile:
            if line.__contains__('>'):
                collection_date = get_date_from_header_line(line)

                if is_in_the_peak(peak_one_dates, collection_date):
                    first_peak.write(line)
                    flag = 1

                if is_in_the_peak(peak_two_dates, collection_date):
                    second_peak.write(line)
                    flag = 2

                if is_in_the_peak(peak_three_dates, collection_date):
                    third_peak.write(line)
                    flag = 3

            elif flag != 0:
                if flag == 1:
                    first_peak.write(line)
                    flag = 0
                elif flag == 2:
                    second_peak.write(line)
                    flag = 0
                elif flag == 3:
                    third_peak.write(line)
                    flag = 0

    first_peak.close()
    second_peak.close()
    third_peak.close()


def analyse_sequence_technology_bias(fasta_file):
    """
    This method Analyse the sequences
    and CSV files related to the MSA (multiple sequence alignment) and find bias for 3 major
    peak of SARS-COV-2
    :param fasta_file: fasta file containing sequence technology
    :return:
    """
    if not os.path.isdir('files/output/Peaks'):
        os.mkdir('files/output/Peaks')
    if not os.path.isdir('files/output/TransfacFormat'):
        os.mkdir('files/output/TransfacFormat')

    # take the date of three major peak from config file
    firstPeak = config['peaks'].get('firstPeakDate').split(",")
    secondPeak = config['peaks'].get('secondPeakDate').split(",")
    thirdPeak = config['peaks'].get('thirdPeakDate').split(",")

    separate_peaks(fasta_file, [get_date(firstPeak[0]), get_date(firstPeak[1])],
                  [get_date(secondPeak[0]), get_date(secondPeak[1])], [get_date(thirdPeak[0]), get_date(thirdPeak[1])])

    csv_file = parse(fasta_file)

    # testTransfacGenerator:
    # csv_file = config['outputAddresses'].get('csv_file')
    # transfac_file = config['outputAddresses'].get('TransfacFile')

    # transfac_generator(csv_file, transfac_file)
