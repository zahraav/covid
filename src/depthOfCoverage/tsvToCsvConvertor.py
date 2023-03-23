import re

with open("files/output/depthOfCoverage/Illumina/gisaid_hcov-19_2023_02_15_03.tsv", 'r') as myfile:
    with open("files/output/depthOfCoverage/Illumina/Illumina.csv", 'w') as csv_file:
        for line in myfile:
            newline = re.sub("\t", ",", line)
            csv_file.write(newline)