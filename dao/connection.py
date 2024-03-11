import mysql.connector
import connect
dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.Connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, port=connect.dbport,\
    auth_plugin='mysql_native_password',\
    autocommit=True)
    dbconn = connection.cursor()
    return dbconn