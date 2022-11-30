import csv

NanoporeNamesList = ["Oxford Nanopore Artic", "ONT_ARTIC", "Oxford Nanopore", "Oxford Nanopore GridION",
                     "Oxford Nanopore ARTIC", "MinION Oxford Nanopore", "Nanopore MinION", "MinION", "Nanopore ARTIC",
                     "GridION", "Nanopore MinIon", "Ion Torrent", "ONT ARTIC", "Nanopore minION",
                     "Nanopore MinION Mk1C", "Oxford Nanopore Technologies ARTIC", "Nanopore GridION",
                     "Nanopore GridION, ARTIC V3 protocol", "Oxford Nanopore MinION", "Nanopore",
                     "Oxford Nanopore - Artic", "Nanopore GridION", "Oxford Nanopore Technologies ARTIC"]

IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq"]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown"]


def generateCanadaTsv(inputTsvAddress, outputAddress):
    with open(outputAddress, 'w', encoding='UTF8', newline='') as wf:
        writer = csv.writer(wf)
        with open(inputTsvAddress, encoding="utf8") as rf:
            csv_reader = csv.reader(rf)

            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:  # header
                    writer.writerow(line)
                else:
                    if line.__contains__("Canada"):
                        writer.writerow(line)


def addSequencingTechnology(inputCSVFile, inputFastaFile, outputFastaFile):
    with open(outputFastaFile, 'a', encoding='utf-8') as outFastaFile:
        with open(inputFastaFile) as infile:
            for line in infile:
                if line.__contains__('>'):
                    accessionId = line.split("|")[1]
                    with open(inputCSVFile, encoding="utf8") as rf:
                        csv_reader = csv.reader(rf)
                        next(csv_reader)  # skip the header
                        for csvLine in csv_reader:
                            if csvLine.__contains__(accessionId):
                                sequencingTechnology = csvLine[8]
                                if IlluminaNamesList.__contains__(sequencingTechnology):
                                    sequencingTechnology = "Illumina"
                                elif NanoporeNamesList.__contains__(sequencingTechnology):
                                    sequencingTechnology = "Nanopore"
                                elif unknownSequencerList.__contains__(sequencingTechnology):
                                    sequencingTechnology = "-"
                                else:
                                    print(sequencingTechnology)
                                line = line.strip() + "|" + sequencingTechnology
                                outFastaFile.write(str(line) + "\n")
                                writeFlag = True
                elif writeFlag:
                    outFastaFile.write(line)
                    writeFlag = False


inputMetadataFile = 'files/input/statisticalAnalysis/BC/mergedFile.csv'
inputFile = 'files/input/statisticalAnalysis/msa_0206_BC.fasta'
outputFile = 'files/input/statisticalAnalysis/msa_0206_BC_WithSeqTech.fasta'
addSequencingTechnology(inputMetadataFile, inputFile, outputFile)
