"""import configparser
import logging

from alignment.makeAlignment import parseFastaFile, addSeqTechToMSAMetaData
from utilities.ReadAndWrite import saveSeqAlignmentToCSV, saveToCsv
from utilities.featureExtraction import process_fasta_file
from utilities import DBConnection
from utilities import phylogeneticTree

CONFIG_FILE = r'config/config.cfg'

logging.basicConfig(filename="%s" % 'src/logs/logs.log',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


def find_accession_id(header):
    split_header = header.split('|')
    for i in split_header:
        if i.__contains__('EPI'):
            return i




def generate_new_header(covid_sequence):
    config = get_configs()
    table_name = config['databaseInfo'].get('table_name')

    seq_technology = DBConnection.get_technology(table_name, "Accession_ID", covid_sequence.accession_id)
    seq_assembly_method = DBConnection.get_assembly_method(table_name, "Accession_ID", covid_sequence.accession_id)

    return (str(covid_sequence.header).rstrip("\n") + "|" + str(seq_technology).rstrip("\n") + "|" + str(
        seq_assembly_method).rstrip("\n")).replace(' ', '_')


class CovidSequence:

    def __init__(self, header_, sequence_=None):
        self.sequence = sequence_
        self.header = header_
        self.accession_id = find_accession_id(self.header)
        self.new_header = generate_new_header(self)


# every time this function is called it will read and make a
# CovidSequence class and return it
def next_data(fastafile,basePairCount):
    count = 1
    sequence = ''
    header = ''
    print(fastafile)
    with open(fastafile) as infile:
        for line in infile:
            if line.__contains__('>'):
                if count == 2:
                    count = 1
                    #temp_sequence = sequence[(basePairCount-1)*100:(basePairCount)*100:]
                    temp_sequence=sequence
                    temp_header = header
                    sequence = ''
                    yield CovidSequence(temp_header, temp_sequence)
                header = line
            else:
                sequence = str(sequence.rstrip("\n")) + str(line.rstrip("\n"))
                count = 2


def change_fasta_header(output,basePairCount,input_fasta_file,is_header):
    try:
        with open(output.replace("files/","files/test_"), 'w', encoding='utf-8') as f1:
            for d in next_data(input_fasta_file,basePairCount):

                #f1.write(d.new_header + '\n' + d.sequence + '\n')

                f1.write(d.header+'\n'+d.sequence+'\n')
                saveToCsv('files/aligedMatrix.csv', [find_accession_id(d.new_header),d.sequence],
                          ['Accession_id', 'Seq-align'], is_header)
                is_header=False;
    except MemoryError as e:
        logger.error(e)



def main():
    config = get_configs()
    basePairCount=config['databaseInfo'].get('basePairCount')
    table_name=config['databaseInfo'].get('table_name')

    input_fasta_file = config['address'].get('folder')+table_name+\
                       config['address'].get('input_fastafile')



    aligned_file_name = config['address'].get('folder')+"aligned_"+\
                  table_name+ config['address'].get('input_fastafile')\
                      .replace(".fasta","_"+basePairCount+".fasta")


    #basePairCount=int(basePairCount)
    is_header=True
    change_fasta_header(aligned_file_name,basePairCount,input_fasta_file,is_header)

    #align_seq(input_fasta_file)

    parseFastaFile(table_name,'files/test_MSA_2.fasta','files/output_Test_MSA_22.fasta')
    #addSeqTechToMSAMetaData()
    #process_fasta_file('files/outputCanada_msa_0120-Copy.fasta', '1', table_name+'_')


if __name__ == '__main__':
    main()
"""