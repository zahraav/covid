def separate_data_for_a_location(inputAddress, outputAddress):
    """
    This Method separates data for a specific region from input file, and save it into outputAddress.
    :param inputAddress:
    :param outputAddress:
    :return:
    """
    output = ''
    flag = False
    with open(outputAddress, 'a', encoding='utf-8') as output_handle:
        with open(inputAddress) as infile:
            for line in infile:
                if line.__contains__('>') and line.__contains__('Qc'):
                    output += line
                    flag = True
                elif flag:
                    output += line
                    flag = False
                    output_handle.write(output)
                    output = ''


inputFile = 'files/input/msa_0206_NorthAmerica.fasta'
outputFile = 'files/input/msa_0206_Canada.fasta'
outputFile2 = 'files/input/msa_0206_QC.fasta'
separate_data_for_a_location(outputFile, outputFile2)
