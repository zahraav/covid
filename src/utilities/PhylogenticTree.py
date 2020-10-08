# Linux:
# from Bio.Align.Applications import ClustalwCommandline

import sys
from Bio import Phylo
import logging
from Bio.Align.Applications import ClustalwCommandline
import os

logger = logging.getLogger(__name__)


def draw_tree(input_address):
    # Linux:
    """ cline = ClustalwCommandline("clustalw", infile=input_address, outfile=input_address.replace('.fasta','.aln'))
    stdout, stderr = cline()
    tree = Phylo.read(input_address.replace('.fasta','.dnd'), "newick")"""

    # Windows:
    clustalw_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=input_address)
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    sys.setrecursionlimit(4000)
    tree = Phylo.read(input_address.replace('.fasta', '.dnd'), "newick")

    # Print phylogenetic tree
    # Phylo.draw_ascii(tree)
    tree.rooted = True
    Phylo.draw(tree)
