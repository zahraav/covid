import csv
import math
import scipy.stats as stats


def saveData(saving_address, data):
    """
    This function write the data in the output_address file
    :param saving_address: Address of file which we want to save data
    :param data: data for saving in the file , String
    :return: none
    """
    with open(saving_address, "a") as output_handle:
        output_handle.write(data)


def saveToCsv(fileName, csvList, fieldNames, isHeader):
    """

    :param fileName: address of the CSV file
    :param csvList: list of one line of data for writing on the CSV file
    :param fieldNames: List of fields for header
    :param isHeader: It shows whether it is the first time this method is called or not.
    If so, isHeader is going to be true. As a result, the method prints the header fields on the CSV file.
    :return: True, if it generates the file. False if it throws any exceptions.
    """
    x = {}
    for name, elem in zip(fieldNames, csvList):
        x[name] = str(elem)
    with open(fileName, 'a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        if isHeader:
            writer.writeheader()
        writer.writerow(x)


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
    oddsRatio, p_value = stats.fisher_exact([[nucleotide_in_nanopore, nucleotide_in_illumina],
                                             [not_nucleotide_in_nanopore, not_nucleotide_in_illumina]])

    str_p_value = 'n_n: ' + str(nucleotide_in_nanopore) + '  n_i: ' + str(nucleotide_in_illumina) + '  nn_n: ' + str(
        not_nucleotide_in_nanopore) + '  nn_i: ' + str(not_nucleotide_in_illumina) + '  p_value: ' + str(
        p_value) + ' \n'
    saveData(p_value_file, str_p_value)
    return p_value


def calculate_list_elements(ni, sum_):
    if sum_ == 0:
        return 0
    prop = ni / sum_
    return 0 if prop == 0 else prop * math.log10(prop)


def LikelihoodRatioTest(N1, L1, N2, L2, L_joint, filename, is_header, csv_address):
    """
    T = 2 * [N_1 * L_1 + N_2 * L_2 - (N_1 + N_2) * L_{joint}]
    """
    result = 2 * (N1 * L1 + N2 * L2 - (N1 + N2) * L_joint)

    printstr = str(N1) + '  L1: ' + str(L1) + '  N2: ' + str(N2) + '  L2: ' + str(L2) + '  L_joint: ' + str(L_joint) + \
        '  T: ' + str(result) + '\n'
    saveData(filename, printstr)
    csv_list = [str(N1), str(L1), str(N2), str(L2), str(L_joint), str(result)]
    saveToCsv(csv_address, csv_list, ['N1', 'L1', 'N2', 'L2', 'L_joint', 'result'], is_header)

    return result
