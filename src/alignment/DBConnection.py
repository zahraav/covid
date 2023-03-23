"""import mysql.connector

myDb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="19_1_2021_seq_tech_metadata_canada_world"
)
database = "world"


def query_execute(query):
    my_cursor = myDb.cursor()
    print(query)

    my_cursor.execute(query)
    result = my_cursor.fetchone()
    myDb.commit()

    if result is None:
        return
    return result[0]


def query_execute_all(query):
    my_cursor = myDb.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchone()

    return result


def readSeqTech(table, accession_id):
    # return query_execute("SELECT Sequencing_technology FROM "+table+" WHERE Accession_ID='"+accession_id+"'")
    query = "SELECT Sequencing_technology FROM " + table + " WHERE Accession_ID='" + accession_id + "'"
    result = query_execute(query)
    return result


def readMetadata(accessionID, tableName):
    return query_execute("SELECT * FROM " + tableName + " WHERE gisaid_epi_isl= `" + accessionID + "`")


def addColumnToTable(tableName, columnName):
    return query_execute("ALTER TABLE " + tableName + " ADD " + columnName + " VARCHAR(100) NOT NULL")


def updateTable(tableName, accessionIdColumnName, accession_id, columnName, value):
    return query_execute(
        "UPDATE " + tableName + " SET " + columnName + " = '" + value +
        "' WHERE " + accessionIdColumnName + " = '" + accession_id + "' ")


def makeTable(tableName, firstLine, row):
    return query_execute("INSERT INTO " + tableName + "(" + firstLine + ") VALUES('" + row + ");")
"""