import configparser
import csv
import os

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getContentOfFile(inputFile):
    with open(inputFile) as infile:
        for line in infile:
            if not line.__contains__(">"):
                return line


def compareToUCSCSpike():
    UCSCSpike = config['inputAddresses'].get('UCSCSpike')
    rGenomeUCSCSpike = getContentOfFile(UCSCSpike)
    spikesFile = config['outputAddresses'].get('spikeFastaFile')
    comparedFile = config['outputAddresses'].get('comparedFile')
    referenceGenomeFile = config['inputAddresses'].get('spikeReferenceGenome')

    spikeList = {}
    header = ""
    with open(spikesFile) as infile:
        for line in infile:
            if line.__contains__('>'):
                header = line.strip()
            else:
                spikeList[header] = line.strip()
                header = ""
    spikeList['referenceGenome']=getContentOfFile(referenceGenomeFile)

    if os.path.exists(comparedFile):
        print('Existing UCSC comparison csv file for spike removed successfully!!')
        os.remove(comparedFile)
    isHeader = True
    for i in spikeList:
        count = 0
        for x in range(rGenomeUCSCSpike.__len__()):
            if rGenomeUCSCSpike[x] != spikeList[i][x]:
                count += 1

        with open(comparedFile, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            if isHeader:
                writer.writerow(["number of differences", "header"])
                isHeader = False
            writer.writerow([count, i])