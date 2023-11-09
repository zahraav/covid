import csv
import matplotlib.pyplot as plt
import numpy as np


def count_sequencing_technologies(input_fasta_file):
    nanopore_count = 0
    illumina_count = 0
    with open(input_fasta_file) as infile:
        with open('files/sequenceTechnologiesList.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sequencing_technologies'])
            for line in infile:
                if line.__contains__('>'):
                    st = line.split("|")[4]
                    if st.strip() == "Illumina":
                        illumina_count += 1
                    elif st.strip() == "Nanopore":
                        nanopore_count += 1
                    else:
                        st_list = [st.strip()]
                        writer.writerow(st_list)

    return nanopore_count, illumina_count


def count_sequences_with_consensus_sequences(input_fasta_file):
    nanopore_count = 0
    illumina_count = 0
    iupac_codes = ['W', 'M', 'D', 'V', 'Y', 'B', 'H', 'S', 'R', 'K', 'U', 'N']
    st = ""
    see_header = False
    with open(input_fasta_file) as infile:
        for line in infile:
            if line.__contains__('>'):
                st = line.split("|")[4]
                see_header = True
            elif see_header:
                if any(char in iupac_codes for char in line.strip()):
                    if st.strip() == "Illumina":
                        illumina_count += 1
                    elif st.strip() == "Nanopore":
                        nanopore_count += 1
                see_header = False

    return nanopore_count, illumina_count


def count_consensus_nucleotide(input_fasta_file):
    illumina_count = 0
    nanopore_count = 0
    see_header = False
    with open(input_fasta_file) as infile:
        for line in infile:
            if line.__contains__('>'):
                st = line.split("|")[4]
                see_header = True
            elif see_header:
                for x in line:
                    if x == 'Y':
                        if st.strip() == "Illumina":
                            illumina_count += 1
                        elif st.strip() == "Nanopore":
                            nanopore_count += 1
                see_header = False
    print(nanopore_count, "  ", illumina_count)


def technologyConsensusNucleotide():
    """
    This method gets an Multiple sequence alignment file as an input.
    Then generate the sequence technology/letter bar chart.
    first by passing the input file to returnDictionarybyTechnologyLetter method it gets a dictionary
    containing the relationship between sequenced technology and IUPAC nucleotide code
    -except 'A', 'C', 'G', 'T'-
    between sequence technology and letters
    :return:
    """
    nanopore_list = [1.3812, 3.2235, 3.3352, 1.5415, 1.8131, 5.0902, 0.2433, 1.1235, 0, 1.005]
    illumina_list = [98.6187, 96.7764, 96.6647, 98.4584, 98.1868, 94.9097, 99.7566, 98.8764, 100, 98.9949]

    # create plot
    _, ax = plt.subplots()
    index = np.arange(10)
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, nanopore_list, bar_width, alpha=opacity, color='blue', label='Nanopore')
    plt.bar(index + bar_width, illumina_list, bar_width, alpha=opacity, color='green', label='Illumina')

    plt.xlabel('Consensus nucleotides')
    plt.ylabel('Count')
    plt.title('Distribution of consensus nucleotides in sequencing technologies')
    plt.xticks(index + bar_width, ["Y", "S", "W", "K", "R", "M", "H", "D", "B", "V"])

    plt.legend()
    plt.tight_layout()
    bar_output_address = 'files/output/Bias/technology_letter.jpeg'
    plt.savefig(bar_output_address, dpi=800)

    plt.show()


def draw_pie_chart_for_proportion_of_sequencing_technologies(data_without_iupac_array, output_file):
    data1 = data_without_iupac_array

    plt.bar(range(len(data1)), data1, color=['orange', 'blue'])
    plt.xlabel('Sequencing technologies')
    plt.ylabel('Count')
    plt.xticks(np.arange(2), ('Nanopore', 'Illumina'))
    plt.title("proportion of consensus nucleotides per sequencing technologies",fontsize=8)
    plt.savefig(output_file, dpi=800)
    plt.show()
    plt.close()


def consensus_nucleotide():
    # nanopore_count, illumina_count = count_sequencing_technologies("files/MSA_NoSpace_without_reference_genome.fasta")
    # nanopore_count_with_iupac_codes, illumina_count_with_iupac_codes = count_sequences_with_consensus_sequences(
    #    "files/MSA_NoSpace_without_reference_genome.fasta")
    # print(nanopore_count, " ", illumina_count)
    # print(nanopore_count_with_iupac_codes, "  ", illumina_count_with_iupac_codes)

    # draw_pie_chart_for_proportion_of_sequencing_technologies([nanopore_count_with_iupac_codes /
    #                                                          (nanopore_count ) * 100,
    #                                                          illumina_count_with_iupac_codes /
    #                                                          (illumina_count) * 100],
    #                                                         'files/output/Bias/sequencingTechnology.png')
    draw_pie_chart_for_proportion_of_sequencing_technologies(
        [45032 / (94059) * 100, 148486 / (308972) * 100]
        , 'files/output/BarCharts/BarCharts/sequencingTechnology2.png')


consensus_nucleotide()
#count_consensus_nucleotide("files/MSA_NoSpace_without_reference_genome.fasta")
#technologyConsensusNucleotide()