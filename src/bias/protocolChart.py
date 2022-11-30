import csv

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd


def findProtocol(protocolAddress, accessionId):
    """
    This method returns the protocol for the input accession id
    :param protocolAddress: the input file containing a accession id and protocol
    :param accessionId:
    :return:
    """
    with open(protocolAddress, 'r') as fReader:
        csv_reader = csv.reader(fReader)
        next(csv_reader)
        for line in csv_reader:
            if line[0] == accessionId:
                return line[1]

    return '-'


def generateNewMSACSVFileWithProtocol(inputAddress, protocolAddress, outputAddress):
    """
    This method adds protocol to the CSV file that was generated before for MSA
    :param inputAddress: CSV file for MSA
    :param protocolAddress: a file containing accession Id and protocols for that id
    :param outputAddress: CSV file with protocol
    :return:
    """
    # accessionIds = set()
    accessionIds = {}
    with open(outputAddress, 'w', encoding='UTF8', newline='') as fWriter:
        writer = csv.writer(fWriter)
        # writer.writerow(["id", "assemblyMethod"])
        with open(inputAddress, 'r') as fReader:
            csv_reader = csv.reader(fReader)
            next(csv_reader)
            for line in csv_reader:
                # accessionIds.add(line[0])
                if not accessionIds.keys().__contains__(line[0]):
                    accessionIds[line[0]] = [line[1], line[2], line[3]]

        for x in accessionIds:
            y = [x]
            # print(x , findProtocol(protocolAddress,x))
            y.extend(accessionIds[x])
            y.extend([findProtocol(protocolAddress, x)])
            print(y)
            writer.writerow(y)


NanoporeNamesList = ["Oxford Nanopore Artic", "ONT_ARTIC", "Oxford Nanopore", "Oxford Nanopore GridION",
                     "Oxford Nanopore ARTIC", "MinION Oxford Nanopore", "Nanopore MinION", "MinION", "Nanopore ARTIC",
                     "GridION", "Nanopore MinIon", "Ion Torrent", "ONT ARTIC", "Nanopore minION",
                     "Nanopore MinION Mk1C", "Oxford Nanopore Technologies ARTIC", "Ion_Torrent_S5",
                     "IonTorrent", "Nanopore GridION", "Nanopore GridION, ARTIC V3 protocol",
                     "Oxford Nanopore MinION", "Nanopore", "Ion_Torrent",
                     "Oxford Nanopore - Artic", "Nanopore GridION", "Oxford Nanopore Technologies ARTIC"]

# List of Illumina in TSV file
IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq", "Illumina_iSeq,_2_x_150bp_paired_end_reads,_ARTIC_V3,_Nextera_Flex_prep",
                     "nCoV_NextSeq", "Illumna_MiSeq", "nCoV_MiSeq",
                     "Swift_Amplicon_SARS-CoV-2_Panel+Illumina_MiniSeq Illumina_Miseq,_2_x_250bp_paired_end_reads,"
                     "_ARTIC_V3,_Nextera_Flex_prep", "Illumina_NestSeq500"]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown"]


def alterSequencingTechnology(inputAddress):
    """
    This method check the CSV file and alter the sequencing technology column to Illumina,Nanopore, and unknown
    :param inputAddress: CSV input file
    :return:
    """
    outputAddress = inputAddress.replace(".csv", "alteredST.csv")
    with open(outputAddress, 'w', encoding='UTF8', newline='') as fWriter:
        writer = csv.writer(fWriter)
        with open(inputAddress) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                st = row[3]
                x = row
                if NanoporeNamesList.__contains__(st):
                    x[3] = 'Nanopore'
                elif IlluminaNamesList.__contains__(st):
                    x[3] = 'Illumina'
                elif unknownSequencerList.__contains__(st):
                    x[3] = 'unknown'
                else:
                    print(st)
                    x[3] = 'unknown'
                writer.writerow(x)


def alterCSVFile(inputAddress, outputAddress):
    """
    This method alters the CSV file, changes the upper case and lower case and makes a unified file.
    :param inputAddress:
    :param outputAddress:
    :return:
    """
    count = 0
    countV1 = 0
    countV2 = 0
    countV3 = 0
    otherCount = 0
    with open(outputAddress, 'w', encoding='UTF8', newline='') as fWriter:
        writer = csv.writer(fWriter)
        with open(inputAddress, encoding="utf8") as fReader:
            csv_reader = csv.reader(fReader)
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:
                    writer.writerow(line)
                else:
                    x = line
                    if x[4] == 'unknown':
                        x[4] = 'Other'
                    if len(line) == 5:
                        x.append("Other")
                    else:
                        protocol = line[5].lower()
                        if protocol == "Artic".lower():
                            x[5] = "ARTIC"
                            count += 1
                        elif protocol == "Artic v1".lower():
                            x[5] = "ARTIC V1"
                            countV1 += 1
                        elif protocol == "Artic v2".lower():
                            x[5] = "ARTIC V2"
                            countV2 += 1
                        elif protocol == "Artic v3".lower():
                            x[5] = "ARTIC V3"
                            countV3 += 1
                        else:
                            x[5] = 'Other'
                            otherCount += 1
                    if x[5] != 'Other':
                        writer.writerow(x)
                    else:
                        print(x)
    print(count, '    ', countV1, '    ', countV2, '    ', countV3, '    ', otherCount)


def drawProtocol(inputAddress):
    """
    This method draws the protocol-sequencing technology-location chart.
    :param inputAddress:
    :return:
    """
    protocol_colors = ['#000066',  # ARTIC V1
                       '#660000',  # ARTIC V2
                       '#003300',  # ARTIC V3
                       '#CCCC00',  # ARTIC
                       '#C0C0C0',  # Other
                       ]

    dt = pd.read_csv(inputAddress, index_col=0, encoding='latin')

    # Categorical Plot
    g = sns.catplot(x='SequencingTechnology',
                    data=dt,
                    palette=protocol_colors,
                    col_wrap=3,
                    hue='Protocol',  # Color by stage
                    col='Location',  # Separate by stage
                    kind='count')  #

    g.set_xticklabels(rotation=-10)
    plt.savefig("files/output/BarCharts/protocol/Msa_FULL_catPlot_withoutOther.jpeg")
    plt.show()


# inputFile = "files/test_Msa_withExtraLetter.csv"
# protocolFile = "files/test_Msa_NoSpace_withoutLetter_WithProtocolsNEW.csv"
inputFile = "files/Msa_NoSpace_withExtraLetter.csv"
protocolFile = "files/Msa_NoSpace_withoutLetter_WithProtocolsNEW.csv"
outputFile = inputFile.replace(".csv", "_withProtocol.csv")
generateNewMSACSVFileWithProtocol(inputFile, protocolFile, outputFile)
alterSequencingTechnology("files/Msa_NoSpace_withExtraLetter_withProtocol_withSequenceTechnology.csv")


inputFile = "files/Msa_FULL.csv"
outputFile = inputFile.replace(".csv", "new_2.csv")
alterCSVFile(inputFile, outputFile)
drawProtocol(outputFile)
