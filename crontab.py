import mysql
from mysql.connector import Error

from cryptogroupsbot.loginByTelethon import client

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='crypto_db',
                                         user='root',
                                         password='190493')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to - ", record)

    cursor = connection.cursor()
    sql_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    print(sql_query)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

