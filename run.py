import configparser
import logging
from src.utilities import DBConnection
from src.utilities import PylogenticTree

logging.basicConfig(filename="%s" % 'src/logs/log.logs',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_FILE = r'..//config/config.cfg'


def get_configs():
    # app_config = configparser.ConfigParser()
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


def find_accession_id(header):
    split_header = header.split('|')
    for i in split_header:
        if i.__contains__('EPI'):
            return i


table_name = "south_america"


def generate_new_header(covid_sequence):
    seq_technology = DBConnection.get_technology(table_name, "Accession_ID", covid_sequence.accession_id)
    seq_assembly_method = DBConnection.get_assembly_method(table_name, "Accession_ID", covid_sequence.accession_id)

    return (str(covid_sequence.header).rstrip("\n") + "|" + str(seq_technology).rstrip("\n") + "|" + str(
        seq_assembly_method).rstrip("\n")) \
        .replace(' ', '_')


class CovidSequence:

    def __init__(self, header_, sequence_=None):
        self.sequence = sequence_
        self.header = header_
        self.accession_id = find_accession_id(self.header)
        self.new_header = generate_new_header(self)

        ''' def add_header(self, header_):
        self.header.append(header_)'''


# every time this function is called it will read and make a
# CovidSequence class and return it
def next_data(fastafile):
    count = 1
    sequence = ''
    header = ''
    with open(fastafile) as infile:
        for line in infile:
            if line.__contains__('>'):
                if count is 2:
                    count = 1
                    temp_sequence = sequence[0:100:]
                    temp_header = header
                    sequence = ''
                    yield CovidSequence(temp_header, temp_sequence)
                header = line
            else:
                sequence = (str(sequence)).rstrip("\n") + str(line.rstrip("\n"))
                count = 2


def main():
    config = get_configs()

    input_fasta_file = config['address'].get('input_address')
    aligned_file = config['address'].get('aligned_file')

    try:
        with open(aligned_file, 'w', encoding='utf-8') as f1:
            for d in next_data(input_fasta_file):
                f1.write(d.new_header + '\n' + d.sequence + '\n')

    except MemoryError as e:
        logger.error(e)

    PylogenticTree.draw_tree(aligned_file)


if __name__ == '__main__':
    main()
