import scipy.stats as stats
import ReadAndWrite


def FisherExactTest(nucleotide_in_nanopore, nucleotide_in_illumina, not_nucleotide_in_nanopore,
                    not_nucleotide_in_illumina, p_value_file='files/p_value.txt'):
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
    str_p_value = 'n_n: ' + str(nucleotide_in_nanopore) + '  n_i: ' + str(nucleotide_in_illumina) + '  nn_n: ' + str(
        not_nucleotide_in_nanopore) + '  nn_i: ' + str(not_nucleotide_in_illumina) + '  p_value: ' + str(
        p_value) + ' \n'
    ReadAndWrite.save_data(p_value_file, str_p_value)
    return p_value
