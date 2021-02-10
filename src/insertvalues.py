

def run_queries(file_name,output_name):
    count = 0
    with open(file_name, 'r') as file:
        for line in file:
            count = count + 1
            if count > 8084:
                #print(line)
                writ_queries(output_name,line)
            else:
                pass


def writ_queries(file_name,line):
    with open(file_name, "a") as output_handle:
        output_handle.write(line)


file_name='files//ascii_output__2.txt'
run_queries(file_name,file_name.replace('2.txt','3.txt'))


