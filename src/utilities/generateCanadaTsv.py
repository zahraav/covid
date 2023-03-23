import csv


def generateCanadaTsv(inputTsvAddress, outputAddress):
    with open(outputAddress, 'w', encoding='UTF8', newline='') as wf:
        writer = csv.writer(wf)
        with open(inputTsvAddress, encoding="utf8") as rf:
            csv_reader = csv.reader(rf)

            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:  # header
                    writer.writerow(line)
                else:
                    if line.__contains__("Canada"):
                        writer.writerow(line)
