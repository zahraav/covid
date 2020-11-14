class Info:
    def __init__(self, line): #technology, protocol, country, region, date):
        self.technology = self.set_technology(line)
        self.protocol = self.set_protocol(line)
        #self.country = country
        #self.region = region
        self.date = self.set_date(line)

    def set_technology(self,line):
        if 'Nanopore' in line:
            return 'N'
        else:
            return 'I'

    def set_protocol(self,line):
        return 'protocol!'

    def set_date(self, line):
        year_and_Month = line.rsplit('|')[2].rsplit('-')
        return year_and_Month[0] + '-' + year_and_Month[1]


    def _print(self):
        return str(self.technology) + '  ' + str(self.date)
    #    return str(self.technology) + '  ' + str(self.protocol) + '  ' + str(self.country) + '  ' + str(
    #        self.region)


class Feature:
    def __init__(self, groups, count, context, position, info_dictionary):
        self.groups = groups
        self.count = count
        self.context = context
        self.position = position  # starts from 1
        # TODO change information , data structure!
        self.infoDictionary = info_dictionary

    def _print(self):
        return 'info:\n ' + str(self.groups) + '  ' + str(self.count) + '  ' + str(self.context) + '  ' + str(
            self.position) + '  ' + '\n' #str(self.infoDictionary.print_info) + '\n'
