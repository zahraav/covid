import configparser
import logging

from alignment.makeAlignment import parseFastaFile
from Bias.findingBias import analyseSeqTechnologyBias

CONFIG_FILE = r'config/config.cfg'

logging.basicConfig(filename="%s" % 'src/logs/logs.log',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


def main():
    config = get_configs()

    inputFastaFile = config['address'].get('inputFastaFile')
    tsvFolder = config['address'].get('TSVFolder')

    outFastaFile = config['output'].get('outFastaFile')

    transfacFile = config['output'].get('TransfacFile')
    csvFile = config['output'].get('csvFile')

    # this method call the first module of the pipeline.
    analyseSeqTechnologyBias(tsvFolder, inputFastaFile, outFastaFile, transfacFile, csvFile)

    # alignedFileFame = config['address'] + "aligned_" + config['address'].get('inputFastaFile')

    # parseFastaFile("", 'files/test_MSA_2.fasta', 'files/output_Test_MSA_22.fasta')
    # addSeqTechToMSAMetaData()
    # process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')


if __name__ == '__main__':
    main()
