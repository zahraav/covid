class Info:
    def __init__(self, line):
        self.technology = self.set_technology(line)
        self.protocol = self.set_protocol(line)
        self.country, self.region = self.set_country_region(line)  # state
        self.date = self.set_date(line)

    def set_technology(self, line):
        if 'Nanopore' in line:
            return 'N'
        else:
            return 'I'

    def set_protocol(self, line):
        protocol= line.rsplit('|')[4]
        if 'v2' in protocol:
            return 'v2'
        else:
            return 'v1'


    def set_country_region(self, line):
        temp = line.rsplit('|')[0].rsplit('/')
        country = temp[1]
        region = temp[2].rsplit('_')[0]  # state
        return country, region

    def set_date(self, line):
        year_and_Month = line.rsplit('|')[2].rsplit('-')
        return year_and_Month[0] + '-' + year_and_Month[1]

    def toprint(self):
        return str(self.technology) + '  ' + str(self.protocol) + '  ' + str(self.country) + '  ' + str(
            self.region) + '  ' + str(self.date)+'\n'


class Feature:
    def __init__(self, groups, count, context, position, info_dictionary,line_nubmber):
        self.groups = groups
        self.count = count
        self.context = context
        self.position = position  # starts from 1
        # TODO change information , data structure!
        self.infoDictionary = info_dictionary
        self.line_number=line_nubmber

    def toprint(self):
        return 'seq num: ' +str(self.line_number)+'  '+str(self.groups) + '  ' + str(self.count) + '  ' + str(self.context) + '  ' + str(
            self.position) + '  ' + '\n'  # str(self.infoDictionary.print_info) + '\n'
