

def run_queries(file_name):
    count = 0
    with open(file_name, 'r') as file:
        for line in file:
            count = count + 1
            try:
                if count > 282240:
                    print(line)

            except:
                pass


run_queries('outputascii.sql')


