import mysql
from mysql.connector import Error
import requests
import calendar
import time

from cryptogroupsbot.loginByTelethon import client

token = '890843151:AAE43ZXhsgy08CeWgbhb5l5zRjI85-XMlug'
url = 'https://api.telegram.org/bot{}/'.format(token)


def crontab():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='crypto_db',
                                             user='root',
                                             password='190493')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

        master = 0
        start = False
        new_last = None
        last_msg = None
        cursor = connection.cursor()
        sql_query = "select `entity` from `user`"
        cursor.execute(sql_query)
        record = cursor.fetchall()
        # For para user
        for row in record:
            sql_query = "select `start` from `user` where `entity` = " + str(row[0])
            cursor.execute(sql_query)
            record = cursor.fetchall()
            for row2 in record:
                start = row2[0]

            if start:
                print("Starting")
                sql_query = "select `last_forward` from `user` where `entity` = " + str(row[0])
                cursor.execute(sql_query)
                record = cursor.fetchall()
                for row2 in record:
                    last_msg = row2[0]

                sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(row[0]) + " and type = 1"
                cursor.execute(sql_query)
                record2 = cursor.fetchall()
                # For para channel master
                for row2 in record2:
                    master = row2[0]

                sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(row[0]) + " and type = 2"
                cursor.execute(sql_query)
                record2 = cursor.fetchall()
                # For para channel source
                for row2 in record2:

                    # Check si hay filtro

                    sql_query = "SELECT text FROM crypto_db.filter where id_user = " + str(row[0])
                    cursor.execute(sql_query)
                    record3 = cursor.fetchall()

                    if len(record3) > 0:
                        # for para mensajes dentro del canal source con filtro

                        for row3 in record3:
                            print("1: " + str(row3[0]))
                            for message in client.iter_messages(row2[0], search=row3[0]):
                                if message.text:
                                    date_time = str(message.date)
                                    pattern = '%Y-%m-%d %H:%M:%S+00:00'
                                    epoch = int(time.mktime(time.strptime(date_time, pattern)))
                                    if epoch > last_msg:
                                        # print(message.sender_id, ':', message.text, " date: ", message.date)
                                        entity = client.get_entity(message.sender_id)
                                        final_msg = ("Message: \"" + message.text + "\"\nSender: " + entity.first_name + " " +
                                              entity.last_name + "\nDate: " + str(message.date))
                                        client.send_message(entity=master, message=final_msg)
                                        if new_last:
                                            if epoch > new_last:
                                                new_last = epoch
                                        else:
                                            new_last = epoch
                    else:
                        # for para mensajes dentro del canal source sin filtro
                        for message in client.iter_messages(row2[0]):
                            if message.text:
                                date_time = str(message.date)
                                pattern = '%Y-%m-%d %H:%M:%S+00:00'
                                epoch = int(time.mktime(time.strptime(date_time, pattern)))
                                if epoch > last_msg:
                                    # print(message.sender_id, ':', message.text, " date: ", message.date)
                                    entity = client.get_entity(message.sender_id)
                                    final_msg = ("Message: \"" + message.text + "\"\nSender: " + entity.first_name + " " +
                                          entity.last_name + "\nDate: " + str(message.date))
                                    client.send_message(entity=master, message=final_msg)
                                    if new_last:
                                        if epoch > new_last:
                                            new_last = epoch
                                    else:
                                        new_last = epoch
                                        print("new_last 2: " + str(new_last))

                if new_last is not None:
                    print("Updating: " + str(new_last))
                    sql_select_query = "UPDATE user SET last_forward = " + str(new_last) + " WHERE entity = " + str(
                        row[0])
                    result = cursor.execute(sql_select_query)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()


if __name__ == '__main__':
    crontab()
