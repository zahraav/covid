unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown", "-"]


def removeSequence(inputAddress, outputAddress):
    """
    This method removes sequences with unknown sequencing technology.
    :return:
    """
    writingFlag = False
    with open(outputAddress, 'a', encoding='utf-8') as outFastaFile:
        with open(inputAddress) as infile:
            for line in infile:
                if line.__contains__('>'):
                    if not unknownSequencerList.__contains__(line.split("|")[4].strip()):
                        outFastaFile.write(line)
                        writingFlag = True
                    else:
                        writingFlag = False
                elif writingFlag:
                    outFastaFile.write(line)


inputFile = 'files/input/statisticalAnalysis/msa_0206_BC_WithSeqTech.fasta'
outputFile = 'files/input/statisticalAnalysis/msa_0206_BC_WithSeqTech_1.fasta'
# inputFile = 'files/input/statisticalAnalysis/test.fasta'
# outputFile = 'files/input/statisticalAnalysis/test2.fasta'

removeSequence(inputFile, outputFile)
