import csv
import getopt
import os
import sys


def main(argv):
    inputFile = ''
    outputFile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["iFile=", "oFile="])
    except getopt.GetoptError:
        print('ModifyTaxonNames.py -i <inputFile> -o <outputFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ModifyTaxonNames.py -i <inputFile> -o <outputFile>')
            sys.exit()
        elif opt in ("-i", "--iFile"):
            inputFile = arg
        elif opt in ("-o", "--oFile"):
            outputFile = arg

    namesSet = set()
    with open(inputFile, "r") as inFile:
        with open(outputFile, "w", newline='') as outFile:
            reader = csv.reader(inFile, delimiter=";")
            writer = csv.writer(outFile, delimiter=";")
            for row in reader:
                first_col = row[0]
                first_two_words = " ".join(first_col.split(" ")[:2])
                namesSet.add(first_two_words)
            sortedSet = sorted(namesSet)
            for x in sortedSet:
                writer.writerow([x])
    os.remove("names.csv")


if __name__ == "__main__":
    main(sys.argv[1:])
