from telethon import TelegramClient, sync

api_id = 755960
api_hash = '86384f08e2c765d6f619e2e647e5d648'

client = TelegramClient('session_name', api_id, api_hash).start()

