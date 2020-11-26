import scipy.stats as stats
import SaveToFile


def FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                    not_nucleotide_in_illumina):
    """
                 |       Nanopore      | Illumina
    -------------|---------------------|---------------
     Nucleotide  | n_in_Nanopore       |  n_in_Illumina
    -------------|---------------------|---------------
     !Nucleotide | not_n_in_Nanopore   | not_n_in_Illumina
                 |                     |
    """
    oddsratio, p_value = stats.fisher_exact([[nucleotide_in_nanopore, nucleotide_in_illumina],
                                             [not_nucleotide_in_nanopore, not_nucleotide_in_illumina]])
    SaveToFile.save_data()
    # print(oddsratio)
    return p_value
