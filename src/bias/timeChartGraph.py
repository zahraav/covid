import configparser
import matplotlib.pyplot as plt
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


def timeChartGraph(inFile):
    """
    This method makes the time chart for from the Fasta file
    :param inFile: main fasta file for making the time chart
    :return:
    """
    graphGenome = config['outputAddresses'].get('graphGenome')

    makeTimeChartGraph(inFile, graphGenome)


def getCountry(line):
    """
    This method returns the country for a line in the
    """
    return line.split('|')[0].split('/')[1].strip()


def getDateOf(line):
    """
    This method returns the country for a line in the
    """
    return line.split('|')[2].strip()


def makeTimeChartGraph(inFastaFile, timeChart):
    """
    This method make the Time Chart for Graph that shows the time of starting the variant and the country
    it initiated and then also shows the time and the countries it moves around the world
    :param inFastaFile: Fasta file containing the sequence technology
    :param timeChart:
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

    for (country, dates) in countries.items():
        dates = [datetime(int(dd.split('-')[0]), int(dd.split('-')[1]), int(dd.split('-')[2]), 0) for dd in dates]
        dates = sorted(dates)
        plt.plot(dates, [x + 1 for x in range(len(dates))], label=str(country))

    plt.legend(loc='best')

    plt.gcf().autofmt_xdate()

    plt.savefig(timeChart)
    plt.close()
