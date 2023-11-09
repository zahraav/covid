import csv


def save_data_to_csv(data):
    """
    Save data to a CSV file.

    :param data: Data to be saved.
    :return: None
    """
    output_file = "Files/output/Peaks/thirdPeak.csv"
    header = ['NA', 'NC', 'NG', 'NT', 'IA', 'IC', 'IG', 'IT', 'reference']

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)


def set_info(line):
    """
    Extract information from the header such as Sequencing Technology,
    location, region, and time.
    :param line: Header string.
    :return: Tuple containing a list of extracted information and the sequencing technology.
    """
    info = []

    # Sequencing Technology
    sequence_tech = '-'
    if 'nanopore' in line.lower():
        sequence_tech = 'Nanopore'
    elif 'illumina' in line.lower():
        sequence_tech = 'Illumina'
    info.append(sequence_tech)

    # Location
    split_line = line.rsplit('|')
    if len(split_line) >= 3:
        location_parts = split_line[0].rsplit('/')
        if len(location_parts) >= 3:
            country = location_parts[1]
            region = location_parts[2].rsplit('-')[0]  # state
            info.extend([country, region])
        else:
            info.extend(['-', '-'])
    else:
        info.extend(['-', '-'])

    # Time
    if len(split_line) >= 3:
        year_and_month = split_line[2].rsplit('-')
        time = year_and_month[0] + ('-' + year_and_month[1] if len(year_and_month) > 1 and year_and_month[1] else '')
        info.append(time)
    else:
        info.append('-')

    return info, sequence_tech


def vertical_cut_nucleotide_count(line, sequence_technology, vertical_dictionary):
    """
    Save nucleotide counts in the vertical cut separately for Nanopore and Illumina.
    :param vertical_dictionary: A 3D dictionary to store counts.
    :param sequence_technology: Sequencing technology ('Nanopore' or 'Illumina').
    :param line: DNA sequence.
    :return: Updated vertical dictionary.
    """
    """ i started from location 0 of real sequence"""
    for position, nucleotide in enumerate(line):
        if sequence_technology == 'Nanopore':
            vertical_dictionary[position][0][nucleotide] += 1
        elif sequence_technology == 'Illumina':
            vertical_dictionary[position][1][nucleotide] += 1
        else:
            pass

    return vertical_dictionary


def save_nucleotide_counts_to_csv(all_dictionary, seq_length, ref_genome):
    """
    Process Nanopore and Illumina data and save to a CSV file.
    :param all_dictionary: A list containing two dictionaries (nanopore and Illumina) for each sequence.
    :param seq_length: Length of the sequences.
    :param ref_genome: Reference genome
    :return: None
    """
    main_nucleotides = ['A', 'C', 'G', 'T']
    csv_data = []
    for ll in range(seq_length):
        row_data = [all_dictionary[ll][0][nucleotide] for nucleotide in main_nucleotides] + \
                   [all_dictionary[ll][1][nucleotide] for nucleotide in main_nucleotides] + \
                   [ref_genome[ll]]
        csv_data.append(row_data)

    save_data_to_csv(csv_data)


def load_reference_genome(ref_genome_address):
    ref_genome = ""
    with open(ref_genome_address) as infile:
        for r_line in infile:
            line = r_line.strip()
            if '>' not in line:
                ref_genome=line
    return ref_genome


def process_fasta_file(fasta_address, ref_genome_address):
    info_dictionary = {}
    vertical_total_nucleotide_dictionary = {}
    is_first_sequence = True
    sequence_length = 0
    ref_genome = load_reference_genome(ref_genome_address)

    with open(fasta_address) as infile:
        for r_line in infile:
            line = r_line.strip()

            if '>' in line:
                accession_id = line.rsplit('|')[1]
                info_dictionary[accession_id], sequencing_technology = set_info(line)
            else:
                temp_line = line[0:len(line)]

                if is_first_sequence:
                    sequence_length = len(temp_line)
                    vertical_total_nucleotide_dictionary = initialize_vertical_nucleotide_dictionary(sequence_length)
                    is_first_sequence = False

                vertical_total_nucleotide_dictionary = vertical_cut_nucleotide_count(
                    temp_line, sequencing_technology, vertical_total_nucleotide_dictionary
                )
                sequencing_technology = ''

    save_nucleotide_counts_to_csv(vertical_total_nucleotide_dictionary, sequence_length, ref_genome)


def initialize_vertical_nucleotide_dictionary(length):
    """
    Initialize a dictionary for storing vertical nucleotide counts.

    :param length: Length of the sequences.
    :return: Initialized vertical nucleotide dictionary.
    """
    vertical_nucleotide_dictionary = {}
    for count in range(length):
        nanopore = {'A': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 0, 'Y': 0, 'B': 0, 'H': 0, 'G': 0, 'S': 0,
                    'R': 0, 'K': 0, 'T': 0, 'U': 0, 'W': 0, 'N': 0, '.': 0, '-': 0}
        illumina = {'A': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 0, 'Y': 0, 'B': 0, 'H': 0, 'G': 0, 'S': 0,
                    'R': 0, 'K': 0, 'T': 0, 'U': 0, 'W': 0, 'N': 0, '.': 0, '-': 0}
        vertical_nucleotide_dictionary[count] = [nanopore, illumina]

    return vertical_nucleotide_dictionary


process_fasta_file("Files/output/Peaks/thirdPeak.fasta","Files/input/referenceG.txt")
'''def count_length(add):
    linelength=0
    flag=1
    temp_line=""
    with open(add) as infile:
        for r_line in infile:
            line = r_line.strip()
            if '>' in line:
                if flag==2:
                    print(len(temp_line))
                    break
                flag=2
            else:
                temp_line += line



count_length("Files/output/Peaks/firstPeak_1.fasta")'''