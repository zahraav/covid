def generateSRRInput(inputFile, address):
    output = ''
    with open(address, 'a', encoding='utf-8') as f1:
        with open(inputFile) as infile:
            for line in infile:
                output += "\"" + line.strip() + "\","

        f1.write(str(output))


generateSRRInput('files/output/signal/SRR_Acc_ListOntario.txt', 'files/output/signal/SRR_Ontario.txt')
generateSRRInput('files/output/signal/SRR_Acc_List_NovaScotia.txt', 'files/output/signal/SRR_NovaScotia.txt')
