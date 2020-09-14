import logging

logging.basicConfig(filename="%s" % 'src/logs/log.logs',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# msa_file = 'input/Test.fasta'
msa_file = 'input/msa_0902.fasta'

class CovidSeq:
    def __init__(self, header_, sequence_=None):
        self.sequence = sequence_
        if header_ is None:
            header_ = []
        self.header = header_

    def add_header(self, header_):
        self.header.append(header_)


def next_data():
    with open(msa_file) as infile:
        for line in infile:
            if line.__contains__('>'):
                temp_header = line
            else:
                sequence = line
                yield CovidSeq(temp_header, sequence)
                temp_header = ''


def main():
    match_list = []
    for d in next_data():
        if match_list.__len__() is 0:
            match_list.append(CovidSeq([d.header], d.sequence))
        else:
            for count, m in enumerate(match_list):
                if d.sequence == m.sequence:
                    m.header.append(d.header)
                    break

                if count is match_list.__len__() - 1:
                    temp = [d.header]
                    match_list.append(CovidSeq(temp, d.sequence))
                    break

    logger.info('length:  ' + str(len(match_list)))
    for m in match_list:
        logger.info(str(m.header) + ' -> ' + m.sequence)


if __name__ == '__main__':
    main()
