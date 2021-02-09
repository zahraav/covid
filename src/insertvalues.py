

def run_queries(file_name):
    count = 0
    with open(file_name, 'r') as file:
        for line in file:
            count = count + 1
            try:
                if count > 1442929:
                    print(line)

            except:
                pass


run_queries('newoutputascii2.sql')


