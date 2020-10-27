# Linux:
#from Bio.Align.Applications import ClustalwCommandline

import sys
import logging
from Bio.Align.Applications import ClustalwCommandline
import os
logger = logging.getLogger(__name__)

import matplotlib
import matplotlib.pyplot as plt
from Bio import Phylo

def save_to_file(data):
    try:
        with open('files/treeRatio.txt', 'a', encoding='utf-8') as f1:
            f1.write(str(data)+'\n')

    except MemoryError as e:
        logger.error(e)

def tree_DFS(branch):
    # (red,blue)
    if branch.is_terminal() is True:
        if 'Nanopore' in branch.name:
            branch._set_color('red')
            return(1,0)
        elif 'Illumina' in branch.name:
            branch._set_color('blue')
            return(0,1)
        else:
            branch._set_color('orange')
        #branch.name = str(branch.total_branch_length()) #(branch.name.split('|')[0]).split('/')[2]
        return(0,0)
    count = 0
    color = -1
    (r_,b_)=(0,0)
    for i in branch:
        (r,b)=tree_DFS(i)

        #print(' ', r, ' ', b)
        if r != 0 and b != 0 and r+b > 10:
            save_to_file((r,b))
        r_=r_+r
        b_=b_+b
        if color == -1 or  str(i.color) == str(color):
            count += 1
            color = i.color

    if count == len(branch):
        branch.color='red'#(color)
    return (r_,b_)




def draw_tree(input_address):
    # Linux:
    #cline = ClustalwCommandline("clustalw", infile=input_address, outfile=input_address.replace('.fasta','.aln'))
    #stdout, stderr = cline()
    #tree = Phylo.read(input_address.replace('.fasta','.dnd'), "newick")

    # Windows:
    clustalw_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=input_address)
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    sys.setrecursionlimit(4000)
    tree = Phylo.read(input_address.replace('.fasta', '.dnd'), "newick")

    branches = [x for x in tree.clade.clades if x is not None]
    #print(dir(tree.clade))
    os.remove('files/treeRatio.txt')
    save_to_file(tree_DFS(tree.clade))
    tree.rooted = True
    matplotlib.rc('font', size=6)
    # matplotlib.rc('red' )
    fig = plt.figure(figsize=(10, 20), dpi=100)
    # tree.clade[0, 0,0,0,0,0].color = "blue"


    axes = fig.add_subplot(1, 1, 1)
    Phylo.draw(tree, axes=axes, do_show=False)
    plt.savefig('files/canada.png', dpi=100)
    plt.show()


draw_tree('files/test.fasta')
