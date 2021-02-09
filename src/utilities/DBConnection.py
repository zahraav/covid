import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="world"
)


def query_execute(query):
    #print('query:',query)

    my_cursor = mydb.cursor()
    #print(query)

    my_cursor.execute(query)
    result = my_cursor.fetchone()
  #  mydb.commit()

    if result is None:
        return
    return result[0]
    #return 'a'


def query_execute_all(query):
    my_cursor = mydb.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchone()

    return result

    #return 'a'


def query():
    return query_execute(
        "SELECT * FROM " + '' + "`canada` WHERE Sequencing_technology in ('Illumina' ,'Nanopore') and  GROUP BY Sequencing_technology")


def select_query(table_name, column, where_filter, filter_value):
    return query_execute(
        "SELECT " + str(column) + " FROM `" + str(table_name) + "` WHERE `" + str(where_filter) + "` = '" + str(
            filter_value) + "' ")


def count_query(table_name, column, where_filter, filter_value):
    return query_execute(
        "SELECT " + str(column) + " FROM `" + str(table_name) + "` WHERE `" + str(where_filter) + "` = '" + str(
            filter_value) + "' ")


def get_technology(table_name, where_item, where_item_value):
    return str(select_query(table_name, " Sequencing_technology ", where_item, where_item_value))


def get_assembly_method(table_name, where_item, where_item_value):
    return str(select_query(table_name, " Assembly_method ", where_item, where_item_value))


def get_ratio_Nano_to_Illu():
    seq_tech = query_execute_all(
        "SELECT Sequencing_technology, COUNT(*) FROM" + " `canada` WHERE Sequencing_technology in ('Nanopore','Illumina') GROUP BY Sequencing_technology");
    return seq_tech[1][1] / seq_tech[0][1]


# get_assembly_method("north_america", "Accession_ID", "EPI_ISL_413557")

def readSeqTech(table, accessionId):
    query="SELECT Sequencing_technology FROM "+table+" WHERE Accession_ID='"+accessionId+"'"
    result=query_execute(query)
    #print(result)
    return result

def readMetadata(accessionID, tableName):
    return query_execute("SELECT * FROM " + tableName + " WHERE gisaid_epi_isl= `" + accessionID + "`")


def addColumnToTable(tableName, columnName):
    return query_execute("ALTER TABLE " + tableName + " ADD " + columnName + " VARCHAR(100) NOT NULL")

def makeTable(tableName,firstLine,row):
    return query_execute("INSERT INTO "+tableName+"("+firstLine+") VALUES('"+row+");")





def createTable(tableName):
    return query_execute(
        "CREATE TABLE '"+tableName+"' Virus_name VARCHAR(100), Accession_ID VARCHAR(100),Collection_date VARCHAR("
                                   "100), Location VARCHAR(100),Host VARCHAR(100), Passage VARCHAR(100),  "
                                   "Specimen VARCHAR(100),Additional_host_information VARCHAR(100),"
                                   "Sequencing_technology VARCHAR(100),Assembly_method VARCHAR(100),Comment VARCHAR("
                                   "100),Comment_type VARCHAR(100),Lineage VARCHAR(100), Clade VARCHAR(100));")







