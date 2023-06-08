
def cut_sequences(input_fasta_file, saving_address):
    """
    This function was used for generating the magnifier for the graph genome picture for the thesis.    :param input_fasta_file:
    :param saving_address:
    :return:
    """
    count = 0
    with open(saving_address, "a") as output_handle:
        with open(input_fasta_file) as infile:
            for line in infile:
                line = line.rstrip()
                if count < 10:
                    if line.__contains__('>'):
                        header = line
                        header_split = header.split(r'|')
                        accession_id = header_split[1]
                        technology = header_split[4]
                    else:
                        info = accession_id + "  " + technology
                        output_handle.write(info)
                        output_handle.write("\n")
                        output_handle.write(line[400:500])
                        output_handle.write("\n")
                        count += 1


output_address = "files/MSA_cut_seq_1.fasta"
input_address = "files/Msa_NoSpace_without_reference_genome.fasta"
cut_sequences(input_address, output_address)
