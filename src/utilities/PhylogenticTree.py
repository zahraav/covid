# Linux:
# from Bio.Align.Applications import ClustalwCommandline

import sys
import logging
import os
import matplotlib.pyplot as plt
from Bio import Phylo
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator
from ruamel_yaml import constructor
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
from Bio.Cluster import treecluster
from Bio.Cluster import Node, Tree

logger = logging.getLogger(__name__)


def save_to_file(data, address, newline=True):
    try:

        with open(address, 'a', encoding='utf-8') as f1:
            f1.write(str(data) + "\n")

    except MemoryError as e:
        logger.error(e)


### https://github.com/audy/bioinformatics-hacks/blob/master/bin/fasta-to-phylip
# !/usr/bin/env python3

"""
Convert a FASTA alignment to Phylip format.
Dependenies: BioPython
fasta_to_phylip --input-fasta file.fasta --output-phy file.phy
"""

from Bio import AlignIO
import argparse

'''def parse_args(address):
    parser = argparse.ArgumentParser()

    parser.add_argument(address, default="/dev/stdin")
    parser.add_argument(address.replace("/","/phylip_" ), default="/dev/stdout")

    return parser.parse_args()
'''


def fastaToPhylipConvertor(address):
    # = parse_args(address)
    # print('address: ',address)
    # address='files/test2.fasta'
    phyaddress = address.replace('fasta', 'phy')
    # print(phyaddress)
    with open(address) as handle:
        records = AlignIO.parse(handle, "fasta")
        # print(records)
        with open(phyaddress, "w") as output_handle:
            AlignIO.write(records, output_handle, "phylip")
            # The name should be ten characters in length
            # name is lines with > in the fasta file


###

def add_to_begining(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + "\n" + content)


def make_new_fasta_file(address):
    phyaddress = address.replace('/', '/phy_')
    with open(address) as infile:
        for line in infile:
            underscore = ''
            if line.__contains__('>'):
                if line.__contains__('Nanopore'):
                    underscore = '_'
                else:
                    underscore = ''

                temp = '>' + line.rsplit('|')[1].rsplit('_')[2] + underscore
            else:
                temp = str(line.rstrip("\r\n"))
            save_to_file(temp, phyaddress)


def tree_DFS(branch, address):
    # (red,blue)
    if branch.is_terminal() is True:
        #print(branch.name)
        if '_' in branch.name: #'Nanopore' in branch.name:
            branch._set_color('red')
            branch.name=''
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return (1, 0)
        else: # 'Illumina' in branch.name:
            branch._set_color('blue')
            branch.name=''
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return (0, 1)
        # else:
        #    branch._set_color('orange')
        # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
    count = 0
    color = -1
    (r_, b_) = (0, 0)
    for i in branch:
        (r, b) = tree_DFS(i, address)
        if 'Inner' in i.name:
            i.name=''

        # print(' ', r, ' ', b)
        if r != 0 and b != 0 and r + b > 10:
            save_to_file(((r, b), i.branch_length), address)

        r_ = r_ + r
        b_ = b_ + b
        #if color == -1 or str(i.color) == str(color):
        #    print(i.color,color)
        #    count += 1
        #    color = i.color
    if r_+b_==r_ and b_==0:
        branch.color='red'
    elif r_+b_==r and r_==0:
        branch.color='blue'
    #if count == len(branch):
    #    branch.color = 'red'  # (color)
    return (r_, b_)


def draw_tree(input_address):
    # Linux:
    # cline = ClustalwCommandline("clustalw", infile=input_address, outfile=input_address.replace('.fasta','.aln'))
    # stdout, stderr = cline()
    # tree = Phylo.read(input_address.replace('.fasta','.dnd'), "newick")

    # Windows:
    clustalw_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=input_address)
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    sys.setrecursionlimit(8000)
    tree = Phylo.read(input_address.replace('.fasta', '.dnd'), "newick")

    # make fasta file for give Phylip
    newFastaAddress = input_address.replace('/', '/phy_')
    newPhyAddress=newFastaAddress.replace('.fasta', '.phy')
    os.remove(newFastaAddress)
    os.remove(newPhyAddress)
    print(newFastaAddress)

    make_new_fasta_file(input_address)
    fastaToPhylipConvertor(newFastaAddress)

    calculator = DistanceCalculator('identity')
    aln = AlignIO.read(open(newPhyAddress), 'phylip')
    dm = calculator.get_distance(aln)
    # print(dm)

    constructor = DistanceTreeConstructor()
    upgmatree = constructor.upgma(dm)
    # upgmatree.scale()
    tree_ratio_address2 = 'files/treeRatio2.txt'
    os.remove(tree_ratio_address2)
    if 'Inner' in upgmatree.clade.name:
        upgmatree.clade.name=''
    save_to_file(tree_DFS(upgmatree.clade, tree_ratio_address2), tree_ratio_address2)

    print(type(upgmatree))
    Phylo.draw(upgmatree, do_show=False)
    plt.savefig('files/canada2.png', dpi=100, format="png")
    # plt.show()

    # print('constructor', upgmatree)

    # tree_ratio_address = 'files/treeRatio.txt'
    # os.remove(tree_ratio_address)
    # save_to_file(tree_DFS(tree.clade, tree_ratio_address), tree_ratio_address)

    # tree.rooted = True
    # Phylo.draw(tree, do_show=False)
    # plt.savefig('files/canada.png', dpi=100)
    plt.show()
    plt.close()


draw_tree('files/test.fasta')
