import os
# from newParser import parse


def addCSVFiles():
    directory = os.path.join('../files/allfiles', "path")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f = open(file, 'r')
                #  perform calculation
                f.close()


"""def runFastaFiles():
   for i in range(1, 10, ):
        fileName = 'files/allfiles/' + str(i) + '.fasta'
         parse(fileName)
         print(fileName)
"""

# runFastaFiles()
