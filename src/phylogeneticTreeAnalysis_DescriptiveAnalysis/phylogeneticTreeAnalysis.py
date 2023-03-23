import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import configparser

from Bio import Phylo
from io import StringIO
from datetime import datetime

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()

color = {}
collection_date_dictionary = {}  # {cluster: [count,min,max],..}


def print_collection_data_dictionary_to_file(date_dictionary):
    """
    This program Method print the Collection Data dictionary into date_file.
    :param date_dictionary:
    :return:
    """

    # Address of file containing the Date information( minDate, maxDate, count of variants)
    date_file = config['outputAddresses'].get('DateFile')

    with open(date_file, '+a') as dateFile:
        for mmd in date_dictionary:
            dateFile.write(str(mmd))  # clusterNum
            dateFile.write('  : ')
            dateFile.write(str(date_dictionary[mmd][1]))  # minDate
            dateFile.write(', ')
            dateFile.write(str(date_dictionary[mmd][2]))  # maxDAte
            dateFile.write(', ')
            dateFile.write(str(date_dictionary[mmd][0]))  # count
            dateFile.write('\n')


def print_clusters_to_file(cluster_dictionary):
    """
    This method prints every cluster to different files.
    :param cluster_dictionary:  different clusters data are stored in this dictionary
    :return:
    """

    output_file = config['outputAddresses'].get('country')

    with open(output_file, '+a') as outfile:
        for cl in cluster_dictionary:
            outfile.write(cl)
            outfile.write('  : ')
            outfile.write(str(cluster_dictionary[cl]))
            outfile.write('\n')


def print_country_dictionary(input_dictionary, output_filename):
    """
    This method prints dictionary containing info from different countries in clusters in  output files
    :param input_dictionary:
    :param output_filename:
    :return:
    """
    with open(output_filename, 'w') as cFile:
        for cc in input_dictionary:
            cFile.write(str(cc))
            cFile.write(': ')

            cFile.write(str(collection_date_dictionary[cc][0]))
            cFile.write(str(input_dictionary[cc]))
            cFile.write('\n')


def draw_pie_chart(country_count_list, my_labels, cluster):
    """
    This method gets a country lists and label for the pie chart.
    Then draw pieChart for different countries in the clusters.
    :param country_count_list: List of different countries and the number of variants in that country in a cluster
    :param my_labels: labels for the pieCart sample
    # my_labels = ["Apples", "Bananas", "Cherries", "Dates", "haha"]
    :param cluster: cluster number
    :return:
    """
    pie_charts_folder = config['outputAddresses'].get('pieChartsFolder')

    y = np.array(country_count_list)  # [35, 25, 25, 15, 5]
    plt.pie(y, labels=my_labels, startangle=90, textprops={"fontsize": 6})
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left", prop={'size': 6})

    # plt.show()
    # saving the pie chart in the pieChartFolder.
    plt.title("Cluster #"+str(cluster+1))
    plt.savefig(pie_charts_folder + "pieChart_" + str(cluster+1) + '.png')
    plt.close()


def make_plots(countries_dictionary):
    """
    This method iterate on Dictionary and plot send clusters' data to drawPieChart method one by one.
    :param countries_dictionary:
    :return:
    """
    for cluster in countries_dictionary:
        value_list = []

        sorted_footballers_by_goals = sorted(countries_dictionary[cluster].items(), key=lambda x: x[1])
        converted_dict = dict(sorted_footballers_by_goals)
        #print(converted_dict)
        for it in converted_dict.values():
            value_list.append(str(it))

        draw_pie_chart(value_list, converted_dict.keys(), cluster)


def analyze_tree(dfs_tree_dictionary, csv_dictionary):
    """
    this Method fill collection_date_dictionary , keys are clusters and the values are minimum Date and
    Maximum Date for every cluster
    :param dfs_tree_dictionary:
    :param csv_dictionary:
    :return:
    """

    for leaf in dfs_tree_dictionary:  # from Tree [leaf, cluster]
        if csv_dictionary.keys().__contains__(leaf):
            min_date = datetime.now()
            max_date = datetime.strptime("2019-01-01", "%Y-%m-%d")

            if collection_date_dictionary != {} and \
                    collection_date_dictionary.keys().__contains__(dfs_tree_dictionary[leaf]):
                # {cluster: [minDate , MaxDate]}
                min_date = collection_date_dictionary[dfs_tree_dictionary[leaf]][1]
                max_date = collection_date_dictionary[dfs_tree_dictionary[leaf]][2]

            else:
                collection_date_dictionary[dfs_tree_dictionary[leaf]] = [0, min_date, max_date]

            date_dt3 = datetime.strptime(csv_dictionary[leaf][1], '%Y-%m-%d')

            if min_date > date_dt3:  # min > collection date[leaf]
                collection_date_dictionary[dfs_tree_dictionary[leaf]][1] = date_dt3
            if max_date < date_dt3:  # max < collection date[leaf]
                collection_date_dictionary[dfs_tree_dictionary[leaf]][2] = date_dt3

            collection_date_dictionary[dfs_tree_dictionary[leaf]][0] = \
                collection_date_dictionary[dfs_tree_dictionary[leaf]][0] + 1


def return_csv_list(input_csv):
    """
    read CSV Metadata file and return a dictionary base on file
    if the date format is correct add the data to dictionary.
    because some data don't have year and or just mention the year, and don't have month and day, therefore
    I ignore these data.
    :param input_csv: CSV input file
    :return a dictionary {AccessionId:[info , collectionDate]}
    """
    years = ['2019', '2020', '2021', '2022']
    csv_dict = {}  # {accession_id:[info, collectionDate]}
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row[2]) == 10:
                if row[2][0:4] in years:
                    csv_dict[row[0]] = [row[1], row[2]]
    return csv_dict


def dfs(v, cut_length, colour):
    """
    :param v: Branch of graph( it can be terminal or non-terminal)
    :param cut_length: Threshold for cutting graph and make some sub-branches
    :param colour: A number to colour different sub-branches. every sub-branch has a different number
    :return:
    """
    if v.is_terminal():
        color[v.name] = colour
    else:
        for node in v:
            if node.branch_length < cut_length:
                dfs(node, cut_length, colour)
            else:
                colour += 1
                dfs(node, cut_length, colour)


def save_to_file(cluster, collection_date, country, accession_id):
    time_chart_folder = config['outputAddresses'].get('timeChartCluster')  # for countries

    with open((time_chart_folder + '_' + str(cluster) + '.txt'), '+a') as dateFile:
        dateFile.write(country)
        dateFile.write('\t')
        dateFile.write(accession_id)
        dateFile.write('\t')
        dateFile.write(collection_date)
        dateFile.write('\n')


def list_of_countries(cluster_id, csv_info):
    """
    :param cluster_id:
    :param csv_info:
    :return:
    """
    # accession_id - country -collection_date

    country_dictionary = {}

    for node in cluster_id:
        if csv_info.get(node) is not None:  # csv_file contains that node
            country = csv_info.__getitem__(node)[0].split('/')[1]
            collection_date = csv_info[node][1]

            save_to_file(cluster_id[node], collection_date, country, node)

            if country_dictionary.__contains__(cluster_id[node]):  # the country already exist on the dictionary
                if country_dictionary[cluster_id[node]].keys().__contains__(country):
                    count = country_dictionary[cluster_id[node]][country]
                    country_dictionary[cluster_id[node]][country] = count + 1
                else:
                    country_dictionary[cluster_id[node]][country] = 1

            else:
                country_dictionary[cluster_id[node]] = {country: 1}

    return country_dictionary


def get_content_of_file(input_file):
    """
    This method read the input file and return the data in the file.
    :param input_file: Input file
    :return: String contains all the data in the file
    """
    output = ''
    with open(input_file) as infile:
        for line in infile:
            if line.__contains__('>'):
                output += line
            else:
                output += line.strip()
    return output


def mutation_analysis(global_tree, metadata_file):
    """
    This method gets a phylogeneticTree and metadata File related to phylogenetic Tree.
    Phylogenetic Tree is on the newick format. ( the Data that are being used in this pipeline
    was provided from GisAid.)
    :param global_tree: Phylogenetic tree in Newick format
    :param metadata_file: metadata related to the phylogenetic tree
    :return:
    """

    if not os.path.isdir('files/output/PhylogeneticTreeDescriptiveAnalysis'):
        os.mkdir('files/output/PhylogeneticTreeDescriptiveAnalysis')
        os.mkdir('files/output/PhylogeneticTreeDescriptiveAnalysis/pieCharts')
        os.mkdir('files/output/PhylogeneticTreeDescriptiveAnalysis/timeCharts')

    tree_data = get_content_of_file(global_tree)
    csv_info = return_csv_list(metadata_file)

    # tree_data = "(EPI_ISL_406801:0,((EPI_ISL_1712380:0.000133812)0.10:20,EPI_ISL_578194:22,EPI_ISL_2035877:3):0);"

    tree = Phylo.read(StringIO(tree_data), "newick")

    len_for_count = 1e-4
    for cld in tree.clade:
        dfs(cld, len_for_count, 0)

    print_clusters_to_file(color)
    # print(color)  # id : clusterNum
    analyze_tree(color, csv_info)
    print_collection_data_dictionary_to_file(collection_date_dictionary)
    # print(collection_date_dictionary)  # cluster: count, minDate, MaxDate
    country_dictionary = list_of_countries(color, csv_info)

    pie_chart_data = config['outputAddresses'].get('country')  # for countries

    print_country_dictionary(country_dictionary, pie_chart_data)  # cluster: {countriesName: count,...} , ....
    make_plots(country_dictionary)


# variant -country - collectionDate


globalTree = config['inputAddresses'].get('globalTree')
metadataFile = config['inputAddresses'].get('metadata')

mutation_analysis(globalTree, metadataFile)
