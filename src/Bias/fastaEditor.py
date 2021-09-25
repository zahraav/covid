import csv


def makeDictionaryOfSeqTech():
    firstRow = True
    with open("files/file.tsv") as fd:
        # {[Accession Id , sequence Technology]}
        seqTecDictionary = {}

        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            if firstRow:
                firstRow = False
                continue
            else:
                seqTecDictionary[row[1]] = row[8]

        # print(seqTecDictionary)
    return seqTecDictionary


def find_accession_id(header):
    split_header = header.split('|')
    for i in split_header:
        if i.__contains__('EPI'):
            return i


def makeFastaFileWithSeqTech(newFastaName):
    seqDictionary = makeDictionaryOfSeqTech()
    f = open(newFastaName, "w")
    isContainsSeq = False
    with open('files/test_MSA_2.fasta') as fastaFile:
        for line in fastaFile:
            if line.__contains__('>'):
                accessionId = find_accession_id(line)
                print(accessionId)
                if seqDictionary.__contains__(accessionId):
                    print(accessionId, '   ', seqDictionary[accessionId])
                    f.write(line.strip())
                    f.write("|")
                    f.write(seqDictionary[accessionId])
                    f.write('\n')
                    isContainsSeq = True

            elif isContainsSeq:
                f.write(line)
                isContainsSeq = False
    f.close()


newFastaFileName = "files/fastaFileWithSeqTechnology.fasta"
makeFastaFileWithSeqTech(newFastaFileName)
