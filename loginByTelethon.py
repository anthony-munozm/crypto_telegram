from telethon import TelegramClient, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 755960
api_hash = '86384f08e2c765d6f619e2e647e5d648'

client = TelegramClient('session_name', api_id, api_hash).start()

