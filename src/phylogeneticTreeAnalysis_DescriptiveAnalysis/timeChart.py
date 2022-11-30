import csv
from datetime import datetime

from matplotlib import pyplot as plt


def editTxtFileFormat(inputFile, clusterNumber):
    outputChart = inputFile.replace(".txt", ".jpeg")
    outputFile = inputFile.replace(".txt", "_ratio.csv")
    countries = {}
    MinTime = datetime.now()
    MaxTime = datetime(2018, 1, 1, 0)
    with open(inputFile) as inFile:
        for line in inFile:
            line = line.strip()
            x = line.rsplit("\t")
            country = x[0]
            date = x[2]
            if country in countries:
                countries[country].append(date)
            else:
                countries[country] = [date]
    count = 0
    dataCount = 0
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
            dataCount += 1
        # dates = [datetime(int(dd.split('-')[0]), int(dd.split('-')[1]), int(dd.split('-')[2]), 0) for dd in dates]

        sequenceDates = sorted(sequenceDates)
        for x in sequenceDates:
            if x <= MinTime:
                MinTime = x
            if x >= MaxTime:
                MaxTime = x
    header = ["min Time", "Max Time", "MaxTime-MinTime", "dataCount", "mutationPerDay"]
    with open(outputFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow([MinTime, MaxTime, (MaxTime - MinTime), dataCount, (MaxTime - MinTime) / dataCount])

    print(MinTime, "   ", MaxTime)


"""count += 1

        if count < 15:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))], label=str(country))
        else:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))])
    plt.xlabel('Time')
    plt.ylabel('Confirmed cases')
    plt.title('Cumulative worldwide confirmed Covid-19 cases in Cluster ' + str(clusterNumber))

    plt.legend(loc='best', fontsize='5')
    plt.gcf().autofmt_xdate()
    plt.savefig(outputChart)
    plt.close()
"""

for x in range(0, 63):
    editTxtFileFormat("files/output/PhylogeneticTree/TimeCharts/timeChart_" + str(x) + ".txt", x)

# editTxtFileFormat("files/output/PhylogeneticTree/TimeCharts/sample.txt",0,)
