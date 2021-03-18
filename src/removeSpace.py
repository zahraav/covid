import re


input='files/slice/output_slice_seq.fasta'
output=input.replace('.fasta','_2.fasta')
with open(input) as infile:
    for line in infile:
        line=line.rstrip()
        with open(output, 'a+', newline='') as file:
            if line.__contains__('>'):
                line=re.sub("\s","_",line)
            file.write(line)
            file.write('\n')

