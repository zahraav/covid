import argparse
import subprocess


def modifyOutputFile(namesFile):
    print(namesFile)


def fetchData(GCFs):
    print("--->", GCFs)
    nameList = 'nameList.txt'
    command = '''LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 esearch -db assembly -query $gcflist | elink -target 
    taxonomy | efetch -format native -mode xml | grep ScientificName | awk -F ">|<" 'BEGIN{ORS=", ";}{print $3;}' > 
    nameList.txt '''
    subprocess.run(command, shell=True, check=True, executable='/bin/bash')
    modifyOutputFile(nameList)
    # https://www.biostars.org/p/367121/

    print(GCFs)


arg_parser = argparse.ArgumentParser(description=".TXT file contains list GCF id")
arg_parser.add_argument("gcfFile")
arguments = arg_parser.parse_args()

gcfFile = arguments.gcfFile
print(gcfFile)
gcfList = ''
count = 0
with open(gcfFile) as infile:
    for line in infile:
        gcfList = gcfList.strip() + ' ' + line.strip()
        count += 1
        if count == 50:
            fetchData(gcfList)
            gcfList = ''
            count = 0
fetchData(gcfList)
# print(gcfList)
'''


read -p 'gcfFile: '  gcfFile
gcflist=`cat $gcfFile`
#echo "$gcflist"

LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 esearch -db assembly -query $gcflist | elink -target taxonomy | efetch 
-format native -mode xml | grep ScientificName | awk -F ">|<" 'BEGIN{ORS=", ";}{print $3;}' > nameList.txt 

# https://www.biostars.org/p/367121/


sed -i 's/,\s/,/g' nameList.txt
sed -i 's/\s/%20/g'  nameList.txt
sed -i 's/,/\n/g'  nameList.txt


value=`cat nameList.txt` #echo "$value" cat nameList.txt | sed 
's+^+https://api.globalbioticinteractions.org/interaction.csv?sourceTaxon=+g' | xargs -L1 curl > results.csv '''
