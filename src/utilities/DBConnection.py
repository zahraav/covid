import mysql.connector
from matplotlib import collections

#DatabaseConfig = collections.namedtuple('DatabaseConfig', ['userName', 'passWord'])

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="seq_tech_metadata"
)


def query_execute(query):
    my_cursor = mydb.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchone()
    # my_result = my_cursor.fetchall()
    # TODO change for select *
    return result[0]


def select_query(table_name, column, where_filter, filter_value):
    return query_execute(
        "SELECT " + str(column) + " FROM `" + str(table_name) + "` WHERE `" + str(where_filter) + "` = '" + str(
            filter_value) + "' ")


def get_technology(table_name, where_item, where_item_value):
    return str(select_query(table_name, " Sequencing_technology ", where_item, where_item_value))


def get_assembly_method(table_name, where_item, where_item_value):
    return str(select_query(table_name, " Assembly_method ", where_item, where_item_value))


get_assembly_method("north_america", "Accession_ID", "EPI_ISL_413557")
