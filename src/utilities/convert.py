import re

from ReadAndWrite import saveData


def convertTsvToSQL(file_name, table_name):
    with open(file_name, 'r', encoding='utf-8') as tabular_file:
        attributes = None
        for line in tabular_file:
            values = line.split("\t")
            if attributes is None:
                attrList = [re.sub(r"\s+", '_', whitespace_attribues) \
                            for whitespace_attribues in values]
                attributes = ','.join(attrList)
                data = "CREATE TABLE {table} ({attribute_types});".format(table=table_name, attribute_types=",".join(
                    [attr + " VARCHAR(100)" for attr in attrList]))
                print(data)

                saveData(file_name.replace('.tsv', '_' + table_name + '.txt'), data)
            else:
                data = "INSERT INTO {table} ({attributes}) VALUES ({values});" \
                    .format(table=table_name, attributes=attributes, values=',' \
                            .join(['"' + v + '"' for v in values]))
                print(data)
                saveData(file_name.replace('.tsv', '_' + table_name + '.txt'), data)


convertTsvToSQL('files/file.tsv', 'myTable')
