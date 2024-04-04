from FastTelethonhelper import fast_download

import time
import cryptg
from telethon.sync import TelegramClient, events

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6501391531:AAGXvUFE1153Y_EtJp00Xz1uA3stbnS6LUo'

# Initialize the TelegramClient
client = TelegramClient(None, api_id, api_hash).start(bot_token=bot_token)

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def main(event):
    if event.media or event.document:
        type_of = "downloading\nProgress:"
        msg = None
        timer = Timer()
        async def progress_bar(current, total):
            progress_message = "{} {}%".format(type_of, current * 100 / total)
            await msg.edit(progress_message)


        msg = await event.respond("Downloading file...")
        await client.download_media(event.media, file='./', progress_callback=progress_bar,chunk_size=524288)
        await msg.edit("Download completed.")

        #msg = await event.reply("Downloading started")
client.run_until_disconnected()
