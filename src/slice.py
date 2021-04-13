inputFile='files/output_test_22.fasta'
saving_address='files/test_222.fasta'
head=1
tail=3
count=0
with open(saving_address, "a") as output:
    with open(inputFile, 'r') as reader:
        for row in reader:
            if row.__contains__('>'):
                output.write(row)
            else:
                for char in row:
                    if head<= count and count <= tail:
                        output.write(char)
                        #seq=char
                    count+=1
                output.write('\n')

            count=0
