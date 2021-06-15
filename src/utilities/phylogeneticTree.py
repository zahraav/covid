# Linux:
# from Bio.Align.Applications import ClustalwCommandline

import sys
import logging
import os
import matplotlib.pyplot as plt
from Bio import Phylo
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO

logger = logging.getLogger(__name__)


def save_to_file(data, address):
    try:
        with open(address, 'a', encoding='utf-8') as f1:
            f1.write(str(data) + "\n")

    except MemoryError as e:
        logger.error(e)


def fastaToPhylipConvertor(address):
    phyaddress = address.replace('fasta', 'phy')
    with open(address) as handle:
        records = AlignIO.parse(handle, "fasta")
        with open(phyaddress, "w") as output_handle:
            AlignIO.write(records, output_handle, "phylip")
            # The name should be ten characters in length
            # name is lines with > in the fasta file


def add_to_begining(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + "\n" + content)


def make_new_fasta_file(address):
    phyaddress = address.replace('/', '/phy_')
    with open(address) as infile:
        for line in infile:
            if line.__contains__('>'):
                if line.__contains__('Nanopore'):
                    underscore = '_'
                else:
                    underscore = ''
                temp = '>' + line.rsplit('|')[1].rsplit('_')[2] + underscore
            else:
                temp = str(line.rstrip("\r\n"))
            save_to_file(temp, phyaddress)


def tree_DFS(branch, clusters_name):
    # (red,blue)
    if branch.is_terminal() is True:
        # print(branch.name)
        if '_' in branch.name:  # or 'Nanopore' in branch.name:
            branch._set_color('red')
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return (1, 0)
        else:  # 'Illumina' in branch.name:
            branch._set_color('blue')
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return (0, 1)

    (r_, b_) = (0, 0)
    for i in branch:
        ratio = 0
        (r, b) = tree_DFS(i, clusters_name)
        print(clusters_name)
        if i.name in clusters_name:
            ratio = r / (b + r)
            i.name = '* (' + str(ratio) + ')'
            ratio_file_address = '../files/Ratio.txt'
            save_to_file(('* Nanopore:' + str(r) + '   Illumina:' + str(b) + '  Ratio: ' + str(ratio)),
                         ratio_file_address)
        else:
            i.name = ''

        r_ = r_ + r
        b_ = b_ + b

    if r_ + b_ == r_ and b_ == 0:
        branch.color = 'red'
    elif r_ + b_ == r_ and r_ == 0:
        branch.color = 'blue'

    return r_, b_


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
    newPhyAddress = newFastaAddress.replace('.fasta', '.phy')
    os.remove(newFastaAddress)
    os.remove(newPhyAddress)
    # print(newFastaAddress)

    make_new_fasta_file(input_address)
    fastaToPhylipConvertor(newFastaAddress)

    calculator = DistanceCalculator('identity')
    aln = AlignIO.read(open(newPhyAddress), 'phylip')
    dm = calculator.get_distance(aln)

    constructor = DistanceTreeConstructor()
    upgmatree = constructor.upgma(dm)

    clusters = [upgmatree.clade]

    number_of_clusters = 5
    distance_threshold = .001

    for nc in range(number_of_clusters - 1):
        current_max = 0
        index_max = 0
        for i in range(len(clusters)):
            clade_name = clusters[i].name
            if (clade_name.startswith('Inner')) and int(clade_name.strip('Inner')) > current_max:
                current_max = int(clade_name.strip('Inner'))
                index_max = i

        if clusters[index_max].clades[0].branch_length + constructor._height_of(
                clusters[index_max].clades[0]) > distance_threshold:
            break
        for i in clusters[index_max].clades:
            clusters.append(i)

        del clusters[index_max]

    cluster_names = set([c.name for c in clusters])

    ratio_file_address = '../files/Ratio.txt'
    os.remove(ratio_file_address)

    tree_DFS(upgmatree.clade, cluster_names)

    if 'Inner' in upgmatree.clade.name:
        upgmatree.clade.name = ''

    Phylo.draw(upgmatree.clade, do_show=False)
    plt.savefig('files/upgmatree.png', dpi=100, format="png")

    tree_DFS(tree.clade,set())
    Phylo.draw(tree, do_show=False)
    plt.savefig('files/phylotree.png', dpi=100, format="png")
    plt.show()
    plt.close()


#draw_tree('files/output_test_22.fasta')
