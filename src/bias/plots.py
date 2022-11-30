import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd


def drawPlot(inputAddress, xBar, yBar, plotTitle, savingAddress):
    dt = pd.read_csv(inputAddress, index_col=0, encoding='latin')
    sns.barplot(data=dt, x=xBar, y=yBar).set(title=plotTitle)
    plt.savefig(savingAddress)
    plt.show()


def LetterCount():
    inputFile = "files/output/BarCharts/plot/LetterCount.csv"
    outputFile = inputFile.replace('.csv', 'Plot.jpeg')
    drawPlot(inputFile, "IUPAC codes", "Count", 'Number of each IUPAC codes found in all sequences', outputFile)


def LetterContinent():
    inputFile = "files/output/BarCharts/plot/LetterContinent.csv"
    outputFile = inputFile.replace('.csv', 'Plot.jpeg')
    drawPlot(inputFile, "Continent", "Count", ' Number of IUPAC codes found in Continents', outputFile)


def SequenceTechnologyCount():
    inputFile = "files/output/BarCharts/plot/SequenceTechnologyCount.csv"
    outputFile = inputFile.replace('.csv', 'Plot_2.jpeg')
    drawPlot(inputFile, "Sequencing Technology", "Count", 'Number of IUPAC codes for each sequencing technology',
             outputFile)


# LetterCount()
# LetterContinent()
SequenceTechnologyCount()
