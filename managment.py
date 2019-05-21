from pprint import pprint
from telethon.tl.functions.messages import ImportChatInviteRequest
import requests
import json
from time import sleep

from telethon.tl.types import PeerChannel

from cryptogroupsbot.loginByTelethon import client
from cryptogroupsbot.tele_news import *
from cryptogroupsbot.tele_saavn import *
from cryptogroupsbot.tele_temp import temp
from cryptogroupsbot.tele_cricket import *
import mysql.connector
from mysql.connector import Error

token = '890843151:AAE43ZXhsgy08CeWgbhb5l5zRjI85-XMlug'
url = 'https://api.telegram.org/bot{}/'.format(token)


def addMasterChannel(chat_id, update_id, connection):
    print("in")
    message = 'Write the invitational link from the channel where you want to read all the messages:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Master Channel':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    if "https://t.me/joinchat/" in text:

        text_proc = text.rpartition('https://t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity(text).id

    elif "t.me/joinchat/" in text:

        text_proc = text.rpartition('t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity("https://" + text).id

    else:

        try:
            updates = client(ImportChatInviteRequest(text))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity("https://t.me/joinchat/" + text).id

    sql_insert_query = "INSERT IGNORE INTO `channel` (`entity`) VALUES (" + str(id) + ")"
    cursor = connection.cursor()
    result = cursor.execute(sql_insert_query)
    sql_insert_query = "INSERT IGNORE INTO `user` (`entity`) VALUES (" + str(client.get_me().id) + ")"
    result = cursor.execute(sql_insert_query)

    sql_select_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]

    sql_select_query = "select id from `channel` where `entity` = " + str(id)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        id_channel = row[0]

    sql_insert_query = "INSERT IGNORE INTO `channel_user` (`id_user`, `id_channel` ,`type`) VALUES (" \
                       + str(id_user) + ", " + str(id_channel) + ", 1 )"

    result = cursor.execute(sql_insert_query)
    connection.commit()
    print("Record inserted successfully into python_users table")

    message = "Added!"
    send_message(chat_id, message)


def addSourceChannel(chat_id, update_id, connection):
    print("in")
    message = 'Write the invitational link from the channel where you want to get messages:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Master Channel':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    if "https://t.me/joinchat/" in text:

        text_proc = text.rpartition('https://t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity(text).id

    elif "t.me/joinchat/" in text:

        text_proc = text.rpartition('t.me/joinchat/')
        try:
            updates = client(ImportChatInviteRequest(text_proc[2]))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity("https://" + text).id

    else:

        try:
            updates = client(ImportChatInviteRequest(text))
        except Exception as e:
            print(e)
            pass

        id = client.get_entity("https://t.me/joinchat/" + text).id
        print(client.get_entity("https://t.me/joinchat/" + text))
    sql_insert_query = "INSERT IGNORE INTO `channel` (`entity`) VALUES (" + str(id) + ")"
    cursor = connection.cursor()
    result = cursor.execute(sql_insert_query)
    sql_insert_query = "INSERT IGNORE INTO `user` (`entity`) VALUES (" + str(client.get_me().id) + ")"
    result = cursor.execute(sql_insert_query)

    sql_select_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]

    sql_select_query = "select id from `channel` where `entity` = " + str(id)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        id_channel = row[0]

    sql_insert_query = "INSERT IGNORE INTO `channel_user` (`id_user`, `id_channel` ,`type`) VALUES (" \
                       + str(id_user) + ", " + str(id_channel) + ", 2 )"

    result = cursor.execute(sql_insert_query)
    connection.commit()
    print("Record inserted successfully into python_users table")

    message = "Added!"
    send_message(chat_id, message)


def addFilter(chat_id, update_id, connection):
    print("in")
    message = 'Write the text you want to filter:'
    send_message(chat_id, message)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Add Filter':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    cursor = connection.cursor()

    sql_select_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]
    sql_insert_query = "INSERT IGNORE INTO `filter` (`id_user`, `text`) VALUES (" + str(id_user) + \
                       ", '" + text + "')"
    result = cursor.execute(sql_insert_query)
    print(result)
    connection.commit()

    message = "Added!"
    send_message(chat_id, message)


def deleteFilter(chat_id, update_id, connection):
    print("inn")
    message = 'Filters:'
    send_message(chat_id, message)

    cursor = connection.cursor()

    sql_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    print(sql_query)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]

    sql_query = "select `text` from `filter` where `id_user` = " + str(id_user)
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

    sql_query = "DELETE FROM `filter` WHERE `text` = '" + text + "' and id_user = " + str(id_user)

    result = cursor.execute(sql_query)

    connection.commit()

    message = "Deleted!"
    send_message(chat_id, message)


def viewChannel(chat_id, update_id, connection):
    print("in")
    entity = client.get_input_entity(PeerChannel(395315655))
    print(entity)
    message = 'Channels:'
    send_message(chat_id, message)
    cursor = connection.cursor()

    sql_query = "select `id` from `user` where `entity` = " + str(client.get_me().id)
    print(sql_query)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        id_user = row[0]

    sql_query = "select `id_channel` from `channel_user` where `id_user` = " + str(id_user)
    cursor.execute(sql_query)
    record = cursor.fetchall()
    for row in record:
        for item in row:
            sql_query = "select `entity` from `channel` where `id` = " + str(item)
            cursor.execute(sql_query)
            record2 = cursor.fetchall()
            for row2 in record2:
                for item2 in row2:
                    print("Row: " + str(item2))
                    entity = client.get_entity(item2)
                    print(entity)
                    send_message(chat_id, item2)

    connection.commit()


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


def menu(chat_id, text, update_id, connection):
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
        addMasterChannel(chat_id, update_id, connection)
    elif text == 'Add Source Channel':
        addSourceChannel(chat_id, update_id, connection)
    elif text == 'Add Filter':
        addFilter(chat_id, update_id, connection)
    elif text == 'Remove Filter':
        deleteFilter(chat_id, update_id, connection)
    elif text == 'View Channels':
        viewChannel(chat_id, update_id, connection)


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
        dialogs = client.get_dialogs()
        print(dialogs)
        # client.forward_messages(354659824, dialogs, 354659824)
        # for message in client.iter_messages(354659824, search="asd"): -----Filter-----
        for message in client.iter_messages(354659824, search="asd"):
            print(message.sender_id, ':', message.text)

        while text.lower() != 'y':
            sleep(1)
            text = 'start'
            menu(chat_id, text, update_id, connection)
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
