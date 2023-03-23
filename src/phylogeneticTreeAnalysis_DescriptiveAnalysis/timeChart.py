import csv
from datetime import datetime

from matplotlib import pyplot as plt


def edit_txt_file_format(input_file, cluster_number):
    output_chart = input_file.replace(".txt", ".jpeg")
    output_file = input_file.replace(".txt", "_ratio.csv")
    countries = {}
    min_time = datetime.now()
    max_time = datetime(2018, 1, 1, 0)
    with open(input_file) as inFile:
        for line in inFile:
            line = line.strip()
            xx = line.rsplit("\t")
            country = xx[0]
            date = xx[2]
            if country in countries:
                countries[country].append(date)
            else:
                countries[country] = [date]
    count = 0
    data_count = 0
    for (country, dates) in countries.items():
        sequence_dates = []
        for dd in dates:
            xx = dd.split('-')
            if len(xx) >= 2:
                if int(xx[1]) == 0:
                    xx[1] = 1
                if len(xx) == 2:
                    sequence_dates.append(datetime(int(xx[0]), int(xx[1]), 1, 0))
                elif len(xx) == 3:
                    if int(xx[2]) == 0:
                        xx[2] = 1
                    sequence_dates.append(datetime(int(xx[0]), int(xx[1]), int(xx[2]), 0))
            data_count += 1
        # dates = [datetime(int(dd.split('-')[0]), int(dd.split('-')[1]), int(dd.split('-')[2]), 0) for dd in dates]

        sequence_dates = sorted(sequence_dates)
        for xx in sequence_dates:
            if xx <= min_time:
                min_time = xx
            if xx >= max_time:
                max_time = xx
    header = ["min Time", "Max Time", "max_time-min_time", "data_count", "mutationPerDay"]
    with open(output_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow([min_time, max_time, (max_time - min_time), data_count, (max_time - min_time) / data_count])

    print(min_time, "   ", max_time)


"""count += 1

        if count < 15:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))], label=str(country))
        else:
            plt.plot(sequenceDates, [x + 1 for x in range(len(sequenceDates))])
    plt.xlabel('Time')
    plt.ylabel('Confirmed cases')
    plt.title('Cumulative worldwide confirmed Covid-19 cases in Cluster ' + str(cluster_number))

    plt.legend(loc='best', fontsize='5')
    plt.gcf().autofmt_xdate()
    plt.savefig(outputChart)
    plt.close()
"""

for x in range(0, 63):
    edit_txt_file_format("files/output/PhylogeneticTree/TimeCharts/timeChart_" + str(x) + ".txt", x)

# editTxtFileFormat("files/output/PhylogeneticTree/TimeCharts/sample.txt",0,)
