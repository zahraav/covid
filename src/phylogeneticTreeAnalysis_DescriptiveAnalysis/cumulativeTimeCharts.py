import matplotlib.pyplot as plt
import configparser
from datetime import datetime

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    """
    This method returns config from config file in config/config.
    Configs of project are there so for change the configuration of the project we just need to change
    the config file
    :return: configs of app
    """
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def getCountry(line):
    """
    This method returns the country for the line
    """
    return line.split('|')[0].split('/')[1].strip()


def getDateOf(line):
    """
    This method returns the Time for the line
    """
    return line.split('|')[2].strip()


def makeTimeChartGraph(inFastaFile, outFolder):
    """
    This method make the Time Chart for Graph that shows the time of starting the variant and the country
    it initiated and then also shows the time and the countries it moves around the world
    :param outFolder: Folder containing the outputs
    :param inFastaFile: Fasta file containing the sequence technology
    :return:
    """
    countries = {}
    with open(inFastaFile) as inFastaFile:
        for line in inFastaFile:
            if line.__contains__('>'):
                country = getCountry(line)
                date = getDateOf(line)
                if country in countries:
                    countries[country].append(date)
                else:
                    countries[country] = [date]
    count = 0
    for (country, dates) in countries.items():
        sequenceDates = []
        for dd in dates:
            x = dd.split('-')
            if len(x) >= 2:
                if int(x[1]) == 0:
                    x[1] = 1
                if len(x) == 2:
                    sequenceDates.append(datetime(int(x[0]), int(x[1]), 1, 0))
                elif len(x) == 3:
                    if int(x[2]) == 0:
                        x[2] = 1
                    sequenceDates.append(datetime(int(x[0]), int(x[1]), int(x[2]), 0))
        # dates = [datetime(int(dd.split('-')[0]), int(dd.split('-')[1]), int(dd.split('-')[2]), 0) for dd in dates]

        sequenceDates = sorted(sequenceDates)
        count += 1
        if count < 10:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))], label=str(country))
        else:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))])
    plt.xlabel('Time')
    plt.ylabel('Confirmed cases')
    plt.title('Cumulative worldwide confirmed Covid-19 cases')

    plt.legend(loc='best', fontsize='5')
    plt.gcf().autofmt_xdate()
    plt.savefig(outFolder+'timeChart.jpeg')
    plt.close()


def timeChart(inputFile):
    """
    This method makes the time chart for from the Fasta file
    :param inputFile: main fasta file for making the time chart
    :return:
    """
    outputChartFile = config['outputAddresses'].get('timeChart')
    outputFolder = 'files/output/PhylogeneticTreeDescriptiveAnalysis/'
    makeTimeChartGraph(inputFile, outputFolder)


inputAddress = 'files/input/msa_0206.fasta'
timeChart(inputAddress)
