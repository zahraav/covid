from ReadAndWrite import saveToCsv


code = {'A': 0, 'W': 0, 'M': 0, 'D': 0, 'V': 0, 'C': 1, 'Y': 1,
        'B': 1, 'H': 1, 'G': 2, 'S': 2, 'R': 2, 'K': 2, 'T': 3, 'U': 3, 'N': 4, '-': 5, '.': 5}


def analyze_fasta(file_name):
    headerLine = 1
    type = 'none'
    stats = {'Nanopore': [], 'Illumina': []}
    with open(file_name, 'r') as fasta_file:
        for line in fasta_file:
            if headerLine == 0:
                headerLine = 1
                if type != 'Nanopore' and type != 'Illumina':
                    continue
                pos = 0
                for ch in line.strip().rstrip():
                    if len(stats[type]) == pos:
                        stats[type].append([0] * len(set(code.values())))
                    stats[type][pos][code[ch]] = stats[type][pos][code[ch]] + 1
                    pos = pos + 1
                continue
            headerLine = 0
            header = line.strip().rstrip().split("|")
            type = header[-1]
        return stats


def parse(inputFile):
    is_header = True

    stats = analyze_fasta(inputFile)
    for nelem, ielem in zip(stats['Nanopore'], stats['Illumina']):
        csvList = [sum(nelem)]
        for k in nelem:
            csvList.append(k)
        csvList.append(sum(ielem))
        for n in ielem:
            csvList.append(n)
        percentCsvList = csvList.copy()
        for i in range(1 ,6,):
            percentCsvList[i] = percentCsvList[i]/percentCsvList[0]*100
            percentCsvList[i+7]=percentCsvList[i+7]/percentCsvList[7]*100

        saveToCsv(inputFile.replace('.fasta', '_normal.csv'), csvList,
                  ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2',
                   'GAP2'],
                  is_header)
        saveToCsv(inputFile.replace('.fasta', '_percent.csv'), percentCsvList,
                  ['1-nanopore- sum', 'A1', 'C1', 'G1', 'T1', 'N1', 'GAP1', '2-Illumina- sum', 'A2', 'C2', 'G2', 'T2', 'N2',
                   'GAP2'],
                  is_header)
        is_header = False

parse('files/test_MSA_2.fasta')
