import logging

logging.basicConfig(filename="%s" % 'src/logs/log.logs',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)


class CovidSeq:
    def __init__(self, header_, sequence_=None):
        self.sequence = sequence_
        if header_ is None:
            header_ = []
        self.header = header_

    def add_header(self, header_):
        self.header.append(header_)


def main():
    msa_file = 'input/Test.fasta'
    #msa_file = 'input/msa_0902.fasta'
    covid_list = []
    try:
        with open(msa_file) as infile:
            for line in infile:
                if line.__contains__('>'):
                    temp_header = line
                else:
                    sequence = line
                    covid_list.append(CovidSeq(temp_header, sequence))
                    temp_header = ''

    except FileNotFoundError as e:
        print('Cannot fine the file ', e)

    match_list = []

    for d in covid_list:
        # print(count, '  ---  ', d.header, '%%', d.sequence)
        if match_list.__len__() is 0:
            print('lenght ==0 ')
            match_list.append(CovidSeq([d.header], d.sequence))
        else:
            for count, m in enumerate(match_list):
                print('-------------enter-------------')
                print('seq:  ', d.sequence == m.sequence)
                if d.sequence == m.sequence:
                    print(count, '  - match     ', match_list.__len__(), d.header)
                    m.header.append(d.header)
                    break

                print(count, ' - notmatch:   ', m.header, '  #  ', d.header)
                if count is match_list.__len__() - 1:
                    temp = [d.header]
                    match_list.append(CovidSeq(temp, d.sequence))
                    print('%%', match_list.__len__())
                    break

    print('#####################################')
    print('lenght:  ', match_list.__len__())
    for m in match_list:
        print(m.header, '....', m.sequence)


'''
def write_to_file(file_name, sequence):
    # trufile = open(, "a+")
    # file.write(next_line+ "\n")
    save_fasta_file = open(file_name, "a+")
    try:
        save_fasta_file.write(sequence)
    except requests.exceptions.RequestException as exception:
        print(exception)
    except (FileNotFoundError, urllib.error.URLError) as exception:
        print(exception)


'''
if __name__ == '__main__':
    main()
