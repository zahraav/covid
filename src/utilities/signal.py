def generateSRRInput(inputFile,address):
    output = ''
    with open(address, 'a', encoding='utf-8') as f1:

        with open(inputFile) as infile:
            for line in infile:
                output += "\""+line.strip()+"\","

        f1.write(str(output))


generateSRRInput('files/output/signal/SRR_ACC_List_canada2.txt','files/output/signal/b.txt')
