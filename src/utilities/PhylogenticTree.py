# Linux:
from Bio.Align.Applications import ClustalwCommandline

import sys
import logging
from Bio.Align.Applications import ClustalwCommandline
import os
logger = logging.getLogger(__name__)

import matplotlib
import matplotlib.pyplot as plt
from Bio import Phylo


def tree_DFS(branch):
    if branch.is_terminal() is True:
        if 'Nanopore' in branch.name:
            branch._set_color('red')
        elif 'Illumina' in branch.name:
            branch._set_color('blue')
        else:
            branch._set_color('orange')
        return
    count = 0
    color = -1
    for i in branch:
        tree_DFS(i)
        if color == -1 or  str(i.color) == str(color):
            count += 1
            color = i.color
    if count == len(branch):
        branch.color='red'#(color)

def draw_tree(input_address):
    # Linux:
    cline = ClustalwCommandline("clustalw", infile=input_address, outfile=input_address.replace('.fasta','.aln'))
    stdout, stderr = cline()
    tree = Phylo.read(input_address.replace('.fasta','.dnd'), "newick")

    # Windows:
    '''clustalw_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=input_address)
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()
'''
    sys.setrecursionlimit(4000)
    tree = Phylo.read(input_address.replace('.fasta', '.dnd'), "newick")

    branches = [x for x in tree.clade.clades if x is not None]

    tree_DFS(tree.clade)
    tree.rooted = True
    matplotlib.rc('font', size=6)
    # matplotlib.rc('red' )
    fig = plt.figure(figsize=(10, 20), dpi=100)
    # tree.clade[0, 0,0,0,0,0].color = "blue"

    axes = fig.add_subplot(1, 1, 1)
    Phylo.draw(tree, axes=axes, do_show=False)
    plt.savefig('files/canada.png', dpi=100)
    plt.show()


#draw_tree('files/test.fasta')
