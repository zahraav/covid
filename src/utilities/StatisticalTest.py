import math
import scipy.stats as stats
from utilities import ReadAndWrite


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
    ReadAndWrite.saveData(p_value_file, str_p_value)
    return p_value


def calculate_list_elements(ni, sum_):
    if sum_==0: return 0
    prop = ni / sum_
    return 0 if prop == 0 else prop * math.log10(prop)


def LikelihoodRatioTest(N1, L1, N2, L2, L_joint, filename, is_header, csv_address):
    """
    T = 2 * [N_1 * L_1 + N_2 * L_2 - (N_1 + N_2) * L_{joint}]
    """
    result = 2 * (N1 * L1 + N2 * L2 - (N1 + N2) * L_joint)

    printstr = str(N1) + '  L1: ' + str(L1) + '  N2: ' + str(N2) + '  L2: ' + str(L2) + '  L_joint: ' + str(L_joint) + \
               '  T: ' + str(result) + '\n'
    ReadAndWrite.saveData(filename, printstr)
    csv_list = [str(N1), str(L1), str(N2), str(L2), str(L_joint), str(result)]
    ReadAndWrite.saveToCsv(csv_address, csv_list, ['N1', 'L1', 'N2', 'L2', 'L_joint', 'result'],
                           is_header)

    return result
