from telethon.tl.functions.messages import ImportChatInviteRequest
import requests
import json
from time import sleep

from telethon.tl.types import PeerChat

from cryptogroupsbot.loginByTelethon import client
import mysql.connector
from mysql.connector import Error

token = '890843151:AAE43ZXhsgy08CeWgbhb5l5zRjI85-XMlug'
url = 'https://api.telegram.org/bot{}/'.format(token)


def addMasterChannel(chat_id, update_id, cursor, user_id, connection):
    print("in")
    message = 'Write the invitational link from the channel where you want to read all the messages:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Master Channel':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    id_channel = 0

    if "https://t.me/joinchat/" in text:

        text_proc = text.rpartition('https://t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id_channel = client.get_entity(text).id

    elif "t.me/joinchat/" in text:

        text_proc = text.rpartition('t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id_channel = client.get_entity("https://" + text).id

    else:

        try:
            updates = client(ImportChatInviteRequest(text))
        except Exception as e:
            print(e)
            pass

            id_channel = client.get_entity("https://t.me/joinchat/" + text).id

    sql_insert_query = "INSERT IGNORE INTO `channel` (`entity`) VALUES (" + str(id_channel) + ")"
    result = cursor.execute(sql_insert_query)

    sql_insert_query = "INSERT IGNORE INTO `channel_user` (`id_user`, `id_channel` ,`type`) VALUES (" +\
                       str(user_id) + ", " + str(id_channel) + ", 1 )"
    print(sql_insert_query)
    result = cursor.execute(sql_insert_query)
    connection.commit()
    print("Record inserted successfully into python_users table")
    connection.commit()
    message = "Added!"
    send_message(chat_id, message)


def addSourceChannel(chat_id, update_id, cursor, user_id, connection):
    print("in")
    message = 'Write the invitational link from the channel where you want to get messages:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Master Channel':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    id_channel = 0

    if "https://t.me/joinchat/" in text:

        text_proc = text.rpartition('https://t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id_channel = client.get_entity(text).id

    elif "t.me/joinchat/" in text:

        text_proc = text.rpartition('t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id_channel = client.get_entity("https://" + text).id

    else:

        try:
            updates = client(ImportChatInviteRequest(text))
        except Exception as e:
            print(e)
            pass

        id_channel = client.get_entity("https://t.me/joinchat/" + text).id

    sql_insert_query = "INSERT IGNORE INTO `channel` (`entity`) VALUES (" + str(id_channel) + ")"
    cursor = connection.cursor()
    result = cursor.execute(sql_insert_query)

    sql_insert_query = "INSERT IGNORE INTO `channel_user` (`id_user`, `id_channel` ,`type`) VALUES (" + \
                       str(user_id) + ", " + str(id_channel) + ", 2 )"
    print(sql_insert_query)
    result = cursor.execute(sql_insert_query)
    connection.commit()
    print("Record inserted successfully into python_users table")
    connection.commit()
    message = "Added!"
    send_message(chat_id, message)


def enable_disable(chat_id, connection, cursor, user_id):

    sql_select_query = "UPDATE user SET start = !start WHERE entity = " + str(user_id)
    result = cursor.execute(sql_select_query)

    sql_select_query = "select start from user WHERE entity = " + str(user_id)
    print(sql_select_query)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        if row[0] == 0:
            message = "Turned off!"
        else:
            message = "Turned on!"

    send_message(chat_id, message)
    connection.commit()


def addFilter(chat_id, update_id, connection, cursor, user_id):
    print("in")
    message = 'Write the text you want to filter:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Filter':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    sql_insert_query = "INSERT IGNORE INTO `filter` (`id_user`, `text`) VALUES (" + str(user_id) + \
                       ", '" + text + "')"
    result = cursor.execute(sql_insert_query)
    print(result)
    connection.commit()

    message = "Added!"
    send_message(chat_id, message)


def deleteFilter(chat_id, update_id, connection, cursor, user_id):
    message = 'Filters:'
    send_message(chat_id, message)

    sql_query = "select `text` from `filter` where `id_user` = " + str(user_id)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        for item in row:
            print("Row: " + item)
            send_message(chat_id, item)

    message = 'Which one you want to delete:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Which one you want to delete:':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    sql_query = "DELETE FROM `filter` WHERE `text` = '" + text + "' and id_user = " + str(user_id)

    result = cursor.execute(sql_query)

    connection.commit()

    message = "Deleted!"
    send_message(chat_id, message)


def viewChannel(chat_id, connection, cursor, user_id):
    message = '-----Master Channels-----'
    send_message(chat_id, message)
    sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(user_id) + " and `type` = 1"
    print(sql_query)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        entity = client.get_entity(row[0])
        msg = entity.title
        send_message(chat_id, msg)
    message = '-----Source Channels-----'
    send_message(chat_id, message)
    sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(user_id) + " and `type` = 2"
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        entity = client.get_entity(row[0])
        msg = entity.title
        send_message(chat_id, msg)


def get_updates(offset=None):
    while True:
        try:
            URL = url + 'getUpdates'
            if offset:
                URL += '?offset={}'.format(offset)

            res = requests.get(URL)
            while (res.status_code != 200 or len(res.json()['result']) == 0):
                sleep(1)
                res = requests.get(URL)
            print(res.url)
            return res.json()

        except:
            pass;


def get_last(data):
    results = data['result']
    count = len(results)
    last = count - 1
    last_update = results[last]
    return last_update


def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id = last_update['message']['chat']['id']
    update_id = last_update['update_id']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id, text, update_id


def send_message(chat_id, text, reply_markup=None):
    print(chat_id)
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)
    while res.status_code != 200:
        res = requests.get(URL)
    print(res.status_code)


def reply_markup_maker(data):
    keyboard = []
    for i in range(0, len(data), 2):
        key = []
        key.append(data[i].title())
        try:
            key.append(data[i + 1].title())
        except:
            pass
        keyboard.append(key)

    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def welcome_note(chat_id, commands):
    text = "Welcome to CryptoBot"
    send_message(chat_id, text)
    text = 'Select an Option'
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id, text, reply_markup)


def delete_channel(connection, cursor, user_id):
    chat_id, text, update_id = get_last_id_text(get_updates())
    text = 'Select the channel you want to delete:'

    channels = []
    channels_name = {}

    sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(user_id)
    cursor.execute(sql_query)
    record = cursor.fetchall()

    for row in record:
        entity = client.get_entity(row[0])
        channels.append(entity.title)
        channels_name[entity.title.lower()] = row[0]

    keyboard = []
    for i in range(0, len(channels), 2):
        key = []
        key.append(channels[i].title())
        try:
            key.append(channels[i + 1].title())
        except:
            pass
        keyboard.append(key)

    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    send_message(chat_id, text, json.dumps(reply_markup))

    while text.lower() == 'select the channel you want to delete:':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
    x = channels_name.get(text.lower())

    sql_query = "DELETE FROM `crypto_db`.`channel_user` WHERE `id_channel` = " + str(x) + " and id_user = " +\
                str(user_id)
    cursor.execute(sql_query)

    connection.commit()


def start(chat_id):
    message = 'Wanna Start'
    reply_markup = reply_markup_maker(['Start'])
    send_message(chat_id, message, reply_markup)

    chat_id, text, update_id = get_last_id_text(get_updates())
    while (text.lower() != 'start'):
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    return chat_id, text, update_id


def end(chat_id, text, update_id):
    message = 'Do you wanna end?'
    reply_markup = reply_markup_maker(['Yes', 'No'])
    send_message(chat_id, message, reply_markup)

    new_text = text
    while (text == new_text):
        chat_id, new_text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(1)

    if new_text == 'Yes':
        return 'y'
    else:
        return 'n'


def menu(chat_id, text, update_id, cursor, user_id, connection):
    commands = ['Add Master Channel', 'Add Source Channel', 'View Channels', 'Delete Source/Master', 'Add Filter',
                'Remove Filter', 'Start/Stop']
    welcome_note(chat_id, commands)

    while text.lower() == 'start':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
        print("waiting")
    print(text)
    while text not in commands:
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
        print("waiting 2")

    if text == 'Add Master Channel':
        addMasterChannel(chat_id, update_id, cursor, user_id, connection)
    elif text == 'Add Source Channel':
        addSourceChannel(chat_id, update_id, cursor, user_id, connection)
    elif text == 'Add Filter':
        addFilter(chat_id, update_id, connection, cursor, user_id)
    elif text == 'Remove Filter':
        deleteFilter(chat_id, update_id, connection, cursor, user_id)
    elif text == 'View Channels':
        viewChannel(chat_id, connection, cursor, user_id)
    elif text == 'Delete Source/Master':
        delete_channel(connection, cursor, user_id)
    elif text == 'Start/Stop':
        enable_disable(chat_id, connection, cursor, user_id)



def main():

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

        text = ''
        chat_id, text, update_id = get_last_id_text(get_updates())
        chat_id, text, update_id = start(chat_id)
        print('Started')

        while text.lower() != 'y':
            sleep(1)
            text = 'start'

            user_id = client.get_entity(text).id
            cursor = connection.cursor()

            sql_insert_query = "INSERT IGNORE INTO `user` (`entity`, `last_forward`) VALUES (" + str(user_id) + \
                               ", (select UNIX_TIMESTAMP()))"
            print(sql_insert_query)
            result = cursor.execute(sql_insert_query)
            connection.commit()

            menu(chat_id, text, update_id, cursor, user_id, connection)
            text = 'y'
            chat_id, text, update_id = get_last_id_text(get_updates())
            text = end(chat_id, text, update_id)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    main()
