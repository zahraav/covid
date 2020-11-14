class Feature:
    def __init__(self, groups, count, context, position, info):
        self.groups = groups
        self.count = count
        self.context = context
        self.position = position  # starts from 1
        self.info = info

    # def set_features(self, line):
    #    for i in len(line):
    #        print(i)

    def print_features(self):
        return str(self.groups) + '  ' + str(self.count) + '  ' + str(self.context) + '  ' + str(
            self.position) + '  ' + str(self.info) + '\n'
