import sys
import logging
import os
import matplotlib.pyplot as plt
from Bio import Phylo
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO

from utilities.write import saveToFile

logger = logging.getLogger(__name__)


def fastaToPhylipConvertor(address):
    """
    This Method reads a fasta file from the given address and converts the fasta file to the phylip
    :param address:
    :return:
    """
    phyAddress = address.replace('fasta', 'phy')
    with open(address) as handle:
        records = AlignIO.parse(handle, "fasta")
        with open(phyAddress, "w") as output_handle:
            AlignIO.write(records, output_handle, "phylip")
            # The name should be ten characters in length
            # name is lines with > in the fasta file


def addToBeginning(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + "\n" + content)


def makeNewFastaFile(address):
    """
    This method makes a new fasta file, and if the sequencing technology in the file is Nanopore
    it adds _ at the end of the header, and if it is Illumina, it is nothing at the end of the
    header in the phy file.
    :param address: address of the new file
    :return:
    """
    phyAddress = address.replace('/', '/phy_')
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
            saveToFile(temp, phyAddress)


def treeDFS(DFSBranch, clusters_name):
    """
    This method used for specifying color for branches and calculating Ratio, and also clusters data.
    :param DFSBranch:
    :param clusters_name:
    :return:
    """
    # (red,blue)
    if DFSBranch.is_terminal() is True:
        # print(branch.name)
        if '_' in DFSBranch.name:  # or 'Nanopore' in branch.name:
            DFSBranch._set_color('red')
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return 1, 0
        else:  # 'Illumina' in branch.name:
            DFSBranch._set_color('blue')
            # branch.name = (branch.name.rsplit('|')[1].rsplit('_')[2])
            return 0, 1

    (r_, b_) = (0, 0)
    for i in DFSBranch:
        (r, b) = treeDFS(i, clusters_name)
        print(clusters_name)
        if i.name in clusters_name:
            ratio = r / (b + r)
            i.name = '* (' + str(ratio) + ')'
            ratio_file_address = '../files/Ratio.txt'
            saveToFile(('* Nanopore:' + str(r) + '   Illumina:' + str(b) + '  Ratio: ' + str(ratio)),
                       ratio_file_address)
        else:
            i.name = ''

        r_ = r_ + r
        b_ = b_ + b

    if r_ + b_ == r_ and b_ == 0:
        DFSBranch.color = 'red'
    elif r_ + b_ == r_ and r_ == 0:
        DFSBranch.color = 'blue'

    return r_, b_


def drawPhylogeneticTree(input_address):
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

    makeNewFastaFile(input_address)
    fastaToPhylipConvertor(newFastaAddress)

    calculator = DistanceCalculator('identity')
    aln = AlignIO.read(open(newPhyAddress), 'phylip')
    dm = calculator.get_distance(aln)

    constructor = DistanceTreeConstructor()
    upgmaTree = constructor.upgma(dm)

    clusters = [upgmaTree.clade]

    numberOfClusters = 5
    distanceThreshold = .001

    for nc in range(numberOfClusters - 1):
        current_max = 0
        index_max = 0
        for i in range(len(clusters)):
            clade_name = clusters[i].name
            if (clade_name.startswith('Inner')) and int(clade_name.strip('Inner')) > current_max:
                current_max = int(clade_name.strip('Inner'))
                index_max = i

        if clusters[index_max].clades[0].branch_length + constructor._height_of(clusters[index_max].clades[0])\
                > distanceThreshold:
            break
        for i in clusters[index_max].clades:
            clusters.append(i)

        del clusters[index_max]

    cluster_names = set([c.name for c in clusters])

    ratio_file_address = '../files/output/phylogeneticTree/Ratio.txt'
    os.remove(ratio_file_address)

    treeDFS(upgmaTree.clade, cluster_names)

    if 'Inner' in upgmaTree.clade.name:
        upgmaTree.clade.name = ''

    Phylo.draw(upgmaTree.clade, do_show=False)
    plt.savefig('files/output/phylogeneticTree/upgmaTree.jpeg', dpi=100, format="jpeg")

    treeDFS(tree.clade, set())
    Phylo.draw(tree, do_show=False)
    plt.savefig('files/output/phylogeneticTree/phyloTree.jpeg', dpi=100, format="jpeg")
    plt.show()
    plt.close()

# draw_tree('files/output_test_22.fasta')
