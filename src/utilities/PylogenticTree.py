import os
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo
import logging

logger = logging.getLogger(__name__)


def draw_tree(input_address, ):
    clustalw_exe = r"C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=input_address)
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    tree = Phylo.read(input_address.replace('.fasta','.dnd'), "newick")
    # Phylo.draw_ascii(tree)

    # print phylogenetic tree
    tree.rooted = True
    Phylo.draw(tree)


#draw_tree("../../input/Test.fasta")
