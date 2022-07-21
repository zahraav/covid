def getContentOfFile(inputFile):
    """
    This method read the input file and return the data in the file.
    :param inputFile: Input file
    :return: String contains all the data in the file
    """
    output = ''
    with open(inputFile) as infile:
        for line in infile:
            if line.__contains__('>'):
                output += line
            else:
                output += line.strip()
    return output
