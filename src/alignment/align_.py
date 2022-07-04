from Bio import SeqIO
from Bio.Align.Applications import MuscleCommandline  # Read in unfiltered data


def alignFastaFile(fastaFile):
    # fastaFile="files/test.fasta"
    unfiltered = SeqIO.parse(fastaFile, "fasta")  # Drop data without (close to) full length sequences
    full_length_records = []
    for record in unfiltered:
        if len(record.seq) > 29000:
            full_length_records.append(record)  # Write filtered data to file
    SeqIO.write(full_length_records, fastaFile.replace('.fasta', "_2") + ".fasta", "fasta")
    # Align sequences with MUSCLE (using parameters to make the alignment
    # process as fast as possible)
    muscle_cline = MuscleCommandline(input=fastaFile,
                                     out=fastaFile.replace('.fasta', "_aligned") + ".fasta",
                                     diags=True,
                                     maxiters=1,
                                     log="files/align_log.txt")
    muscle_cline()


alignFastaFile("files/quebec_seqtech_gisaid_hcov-19_2021_01_13_23_1.fasta")