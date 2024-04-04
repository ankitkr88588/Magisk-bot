from telethon.sync import TelegramClient,types

# Your Telegram API credentials
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6400640505:AAEkS-gVOM_-W1eL_qRtjS3X9ARjBu14S18'
# Your session name

# Create a TelegramClient instance
import asyncio
from telethon import TelegramClient, events

# Your Telegram API credentials

# Your session name

async def download_file(event):
    message = event.message
    if message.media and isinstance(message.media, types.Document):
        file_id = message.media.document.id
        await event.respond("start ho gya")
        await message.download_media(f'downloaded_file_{file_id}')
        await event.respond("ho gya")

# Create a TelegramClient instance
client = TelegramClient(None, api_id, api_hash)
client.start(bot_token =bot_token )
@client.on(events.NewMessage( incoming=True))
async def download_file(event):
    message = event.message
    if message.media or event.document:
        file_id = message.media.document.id
        await event.respond("start ho gya")
        await message.download_media(f'downloaded_file_{file_id}')
        await event.respond("ho gya")

# Connect to the Telegram server

# Start the event loop
client.run_until_disconnected()
