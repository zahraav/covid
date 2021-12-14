def sliceFastaFile(inputFile, outputAddress, head, tail):
    """
    This method gets a fasta input file and trim every sequence from head location to tail location.
    Then saved the out put with it's header into outputAddress.
    :param inputFile: Input Fasta file
    :param outputAddress: Address for saving the output fasta file
    :param head: Head location for saving the fasta file
    :param tail: Tail location for saving the fasta file
    :return:
    """
    count = 0
    with open(outputAddress, "a") as output:
        with open(inputFile, 'r') as reader:
            for row in reader:
                if row.__contains__('>'):
                    output.write(row)
                else:
                    for char in row:
                        if head <= count <= tail:
                            output.write(char)
                            # seq=char
                        count += 1
                    output.write('\n')

                count = 0

# inFile = 'files/output_test_22.fasta'
# savingAddress = 'files/test_222.fasta'

# sliceFastaFile(inFile, savingAddress, 1,3 )
