
import shutil
import os
import time

from telethon import events, utils
from telethon.sync import TelegramClient
from telethon.tl import types

from FastTelethon import download_file, upload_file

# Updated API credentials and bot token
api_id = 22877673
api_hash = 'fd368cc0762560833a22445063ce2c96'
token = '5663058726:AAHpNOtXeXvFRfetn_R8-Ji5o3fddw_GdGM'
client = TelegramClient("bot", api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hello! Send me any file to be renamed")

    user_directory = "/home/u201853/rename"
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    try:
        shutil.rmtree(user_path)
        print("Directory and all its contents deleted successfully in directory - {user_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



@client.on(events.NewMessage(pattern='/clear'))
async def clear(event):
    if event.sender_id==6476862483:
# Get the list of items in the current directory
        items = os.listdir()

# Iterate through the items
        for item in items:
    # Check if the item is a directory
            if os.path.isdir(item):
        # Delete the directory and its contents
                os.system(f'rm -rf {item}')
        await event.respond(f"all directories deleted inside /home/u201853/Magisk-flasher")


client.start(bot_token=token)

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

# Store user state to track when to download
user_state = {}

@client.on(events.NewMessage(func=lambda e: e.document))
async def filename(event):
    user_id = event.sender_id
    user_state[user_id] = {"filename_requested": True, "document": event.document}

    # Ask the user for a suitable file name
    await event.reply("Please enter a suitable file name for the upload:")

@client.on(events.NewMessage(func=lambda e: e.text))
async def download(event):
    user_id = event.sender_id
    if user_id not in user_state or not user_state[user_id].get("filename_requested"):
        return  # Don't proceed if filename wasn't requested

    type_of = ""
    msg = None
    timer = Timer()
    type_of = "download"
    user_dir = f"/home/u201853/{user_id}"

    # Create the user directory if it doesn't exist
    os.makedirs(user_dir, exist_ok=True)

    async def progress_bar(current, total):
        if timer.can_send():
            await msg.edit("{} {}%".format(type_of, current * 100 / total))

    # Generate a unique filename based on the provided name and the document's extension
    file_name = os.path.join(user_dir, event.text)

    msg = await event.reply("downloading started")
    with open(file_name, "wb") as out:
        await download_file(event.client, user_state[user_id]["document"], out, progress_callback=progress_bar)
    await msg.edit("Finished downloading")

    # After downloading, upload the file with the provided name
    type_of = "upload"
    msg = await event.reply("uploading started")
    with open(file_name, "rb") as out:
        res = await upload_file(client, out, progress_callback=progress_bar)
        attributes, mime_type = utils.get_attributes(file_name)
        media = types.InputMediaUploadedDocument(
            file=res,
            mime_type=mime_type,
            attributes=attributes,
            force_file=False
        )
        await msg.edit("Finished uploading")
        await event.reply(file=media)

    # Delete the downloaded file
    os.remove(file_name)

    # Reset user state
    user_state.pop(user_id)

client.run_until_disconnected()
