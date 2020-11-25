import scipy.stats as stats

"""
             |       Nanopore      | Illumina 
-------------|---------------------|---------------
 Nucleotide  | n_in_Nanopore       |  n_in_Illumina 
-------------|---------------------|---------------
 !Nucleotide | not_n_in_Nanopore   | not_n_in_Illumina
             |                     |
"""
def FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                   not_nucleotide_in_illumina):
    oddsratio, p_value = stats.fisher_exact([[nucleotide_in_nanopore, nucleotide_in_illumina],
                                            [not_nucleotide_in_nanopore, not_nucleotide_in_illumina]])
    #print(oddsratio)
    return p_value