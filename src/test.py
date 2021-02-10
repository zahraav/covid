

line=">hCoV-19/Canada/MB-NML-610/2020|EPI_ISL_632914|2020-03-27|NorthAmerica|Nanopore"
print(line.split('|')[0].split('/')[1].lower())
if(line.split('|')[0].split('/')[1].lower()):
    print(line)
else:
    print('no')