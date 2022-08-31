import os
import re
from Bio.Align.Applications import ClustalwCommandline


def removeSpace(inputFile, outputFile):
    """
    This method remove the spaces in the header lines of fasta file for
    converting metadata from TSV to fasta file
    """
    with open(inputFile) as infile:
        for line in infile:
            line = line.rstrip()
            with open(outputFile, 'a+', newline='') as file:
                if line.__contains__('>'):
                    line = re.sub("\s", "_", line)
                file.write(line)
                file.write('\n')

    makeAlnFile(outputFile)


def makeAlnFile(inputFile):
    # Linux:
    # cline = ClustalwCommandline("clustalw", infile=input_address, outfile=input_address.replace('.fasta','.aln'))
    # stdout, stderr = cline()
    # Windows:
    clustalW_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalW_cline = ClustalwCommandline(clustalW_exe, infile=inputFile)
    assert os.path.isfile(clustalW_cline), "Clustal W executable missing"
    stdout, stderr = clustalW_cline()
