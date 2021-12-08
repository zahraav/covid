import configparser
import logging

# from alignment.makeAlignment import parseFastaFile
from Bias.findingBias import analyseSeqTechnologyBias
from mutationAnalysis.Mutation import mutationAnalysis
from Bias.graphGenome import makeGraphGenome
from Bias.test4 import drawGraphGenome

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

    """
    this method call the first module of the pipeline.
    Bias:
    """
    inputFastaFile = config['inputAddresses'].get('inputFastaFile')
    tsvFolder = config['inputAddresses'].get('TSVFolder')

    #analyseSeqTechnologyBias(tsvFolder, inputFastaFile)

    # alignedFileFame = config['address'] + "aligned_" + config['address'].get('inputFastaFile')
    # parseFastaFile("", 'files/test_MSA_2.fasta', 'files/output_Test_MSA_22.fasta')
    # addSeqTechToMSAMetaData()
    # process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')

    """
    Mutation Analysis
    """

    # globalTree = config['inputAddresses'].get('globalTree')
    # metadataFile = config['inputAddresses'].get('metaDate')
    # mutationAnalysis(globalTree, metadataFile)

    """
    Graph Genome
    """
    fastaFileWithSequenceTechnology = config['outputAddresses'].get('fullFastaFile')
    inFasta = config['outputAddresses'].get('fullFastaFile')

    # makeGraphGenome(inFasta)

    # makeGraphGenome(config,fastaFileWithSequenceTechnology)

    drawGraphGenome(fastaFileWithSequenceTechnology)


if __name__ == '__main__':
    main()
