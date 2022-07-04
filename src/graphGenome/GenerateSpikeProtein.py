import configparser
import os

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def generateSpikes(inFastaFile):
    """
    This method generate Spike protein from MSA FASTA file, and save the result in the spikeFastaFile
    Address in the config, to change the folder for result change the address in config file.
    :param inFastaFile: MSA FASTA File
    :return: the spike file will be saved in the spike directory in graph genome directory
    """

    spikeFile = config['outputAddresses'].get('spikeFastaFile')
    # spike protein location in sequence
    spikeStartPoint = 21563
    spikeEndPoint = 25384

    firstLineFlag = True
    if os.path.exists(spikeFile):
        print('Existing Spikes File removed successfully!!')
        os.remove(spikeFile)

    with open(spikeFile, 'a') as output_handle:
        with open(inFastaFile) as mainFastaFile:
            for line in mainFastaFile:
                if line.__contains__('>'):
                    if firstLineFlag:
                        firstLineFlag = False
                    else:
                        output_handle.write('\n')
                    output_handle.write(line)
                else:
                    spike = line[spikeStartPoint:spikeEndPoint]
                    output_handle.write(spike)
    return spikeFile
