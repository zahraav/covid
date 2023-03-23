import glob
import os.path

import pandas as pd
import re


def convert_tsv_to_csv_files_in_a_directory(input_tsv_folder):
    # tsv1 = "files/input/Bias/tsv_2/tsv1.tsv"
    csv_path = "files/input/Bias/csvFiles/"
    if not os.path.isdir('files/input/Bias/csvFiles'):
        os.mkdir('files/input/Bias/csvFiles')

    file_list = os.listdir(input_tsv_folder)
    for tsv_file in file_list:
        tsv_address = input_tsv_folder + tsv_file
        with open(tsv_address, 'r',encoding="utf8") as my_file:
            csv_address = csv_path + tsv_file.replace('.tsv', '.csv')
            with open(csv_address, 'w',encoding="utf8") as csv_file:
                for line in my_file:
                    file_content = re.sub(",", "-", line)
                    file_content = re.sub("\t", ",", file_content)

                    csv_file.write(file_content)


def concatenate_csv_files(csv_folder):
    os.chdir(csv_folder)
    csv_files = glob.glob('*.{}'.format('csv'))

    df_concat = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

    df_concat.to_csv('C:/Users/others/Desktop/covid_project/covid/files/input/Bias/metadata.csv')


input_tsv_directory = r'files/input/Bias/TSV/'
convert_tsv_to_csv_files_in_a_directory(input_tsv_directory)
concatenate_csv_files('files/input/Bias/csvFiles')
