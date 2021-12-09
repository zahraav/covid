import configparser

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def separateBySeqCount(inFile, outFile):
    outFile = open(outFile, "w")

    seqCount = 0
    with open(inFile) as input:

        for line in input:
            if seqCount < 100:
                if line.__contains__('>'):
                    outFile.write(line)
                else:
                    outFile.write(line[0:1000])
                    outFile.write('\n')
                    seqCount = seqCount + 1
    outFile.close()


outFasta = config['separateFiles'].get('outputFastaFile')
inFasta = config['outputAddresses'].get('fullFastaFile')
separateBySeqCount(inFasta,outFasta)
