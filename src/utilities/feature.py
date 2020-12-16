class Info:
    def __init__(self, line):
        self.technology = self.set_technology(line)
        self.protocol = self.set_protocol(line)
        self.country, self.region = self.set_country_region(line)  # state
        self.collection_date = self.set_collection_date(line)

    def get_technology(self):
        return self.technology

    def set_technology(self,line):
        if 'nanopore' in line.lower():
            return 'nanopore'
        elif 'illumina' in line.lower():
            return 'illumina'
        else :
            return '-'

    def set_protocol(self,line):
        protocol = line.rsplit('|')[4]
        if 'v2' in protocol:
            return 'v2'
        else:
            return 'v1'

    def set_country_region(self,line):
        temp = line.rsplit('|')[0].rsplit('/')
        country = temp[1]
        region = temp[2].rsplit('_')[0]  # state
        return country, region

    def set_collection_date(self, line):
        year_and_Month = line.rsplit('|')[2].rsplit('-')
        time = ''
        if len(year_and_Month) > 1:
            if year_and_Month[1]:
                time = '-' + year_and_Month[1]

        time = year_and_Month[0] + time
        return time

    def toPrint(self):
        return str(self.technology) + '  ' + str(self.protocol) + '  ' + str(self.country) + '  ' + str(
            self.region) + '  ' + str(self.collection_date) + '\n'


class Feature:
    def __init__(self, groups, count, context, position, info_dictionary, line_number):
        self.groups = groups
        self.count = count
        self.context = context
        self.position = position  # starts from 1
        self.infoDictionary = info_dictionary
        self.line_number = line_number

    def toPrint(self):
        return 'seq num: ' + str(self.line_number) + '  ' + str(self.groups) + '  ' + str(self.count) + '  ' + str(
            self.context) + '  ' + str(
            self.position) + '  ' + '\n'
