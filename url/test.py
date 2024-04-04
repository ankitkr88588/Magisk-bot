from mediafiredl import MediafireDL as MF

from urllib.parse import urlparse
import re
import queue
import requests
import datetime
from datetime import datetime as tatetime
import asyncio
import subprocess
import shutil
import os
import time

from telethon import events, Button, utils
from telethon.sync import TelegramClient
from telethon.tl import types
from FastTelethon import download_file, upload_file
dd=0




# Updated API credentials and bot
api_id =21251185
api_hash ='3adfb76fc9dd4da95d2ec4c06c315df8'
token = '5864808613:AAFQsl83aO-IxPky0LkBozBSmGN4BFmCs_M'
admin = 6476862483 # Replace with the actual admin user ID
time.sleep(2)
client = TelegramClient(None, api_id, api_hash).start(bot_token=token)

dd=0
links = {
    'Monday': 'https://direct-link.net/756279/verify',
    'Tuesday': 'https://link-hub.net/756279/verify1',
    'Wednesday': 'https://link-hub.net/756279/verify2',
    'Thursday': 'https://link-hub.net/756279/verify3',
    'Friday': 'https://direct-link.net/756279/verify4',
    'Saturday': 'https://direct-link.net/756279/verify5',
    'Sunday': 'https://direct-link.net/756279/verify6'
}
uuser_ids={}
days_of_week = {
    'Monday': '/start verifycodeis27373636384747',
    'Tuesday': '/start verifycodeis273733764778',
    'Wednesday': '/start verifycodeis273736327364637',
    'Thursday': '/start verifycodeis27373636737473',
    'Friday': '/start verifycodeis2737363373748484',
    'Saturday': '/start verifycodeis27373636e626353747',
    'Sunday': '/start verifycodeis27373636365449'
}
link_download_queue = queue.Queue()
group_user_ids = {}
class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

@client.on(events.CallbackQuery(data=b'bhad'))
async def callback_queue(event):
    global dd
    await event.answer(f"your current position:{dd}",alert=True)



@client.on(events.NewMessage(pattern='/start'))
async def lstart(event):
    if event.raw_text=="/start":
        return
    print(event.raw_text)
    user_id = event.sender_id
    current_time = time.time()
    today = tatetime.today()
    Today = today.strftime("%A")
    print(days_of_week[Today])

    # Check if the user's message contains the special start link
    if days_of_week[Today] == event.raw_text:
            # Add the new user ID with an expiration time of 1 day (86400 seconds)
        uuser_ids[user_id] = current_time + 86400

            # Send a welcome message to the new user
        await event.respond("Welcome to the bot! You are verified for one day",buttons=home_buttons)

            # User already exists, check if their expiration time has passed
    if days_of_week[Today] != event.raw_text:
        await event.respond("Wrong link, please try again")

edit=0
user_ids={}
link_downloading= False
@client.on(events.NewMessage)
async def main(event):
    if event.raw_text.startswith("htt"):
        parsed_url = urlparse(event.raw_text)
        domain = parsed_url.netloc
        if domain.endswith('mediafire.com'):
            await mediafire_ddl(event)
        else:
            await link_download(event)

async def mediafire_ddl(event):
    try:
        url = event.raw_text
        user_id = event.sender_id
        user_dir = f"/home/u201853/url/{user_id}"
        file_name = MF.GetName(url)
        
        message = await event.reply("Downloading {user_dir}\n please wait")
        file_result = MF.Download(url,user_dir)
        await message.edit("file Downloaded")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
# Usage example:
async def update_progress(event, message, link):
    while True:
        await asyncio.sleep(3) 

async def link_download(event):
    global link_downloading
    global dd
    global user2
    global edit
    link=event.raw_text
    global zipping_in_progress
    link = event.raw_text
    user_id = event.sender_id
    user_dir = f"/home/u201853/url/{user_id}"
    download_directory = user_dir
    os.makedirs(user_dir, exist_ok=True)
    try:
        shutil.rmtree(user_dir)
    except Exception as e:
        print(e)
    os.makedirs(user_dir, exist_ok=True)
    max_file_size_bytes = 7.9* 1024 * 1024 * 1024  # 4 GB in bytes
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 54.9* 1024 * 1024 * 1024 - total_size  # 3GB in bytes
    if not link_downloading:
        try:
        # Send a HEAD request to fetch only headers and check file size
            response = requests.head(link)
            if "content-length" in response.headers:
                content_length = int(response.headers["content-length"])

                if content_length <= remaining_storage:
                    link_downloading = True
                    message = await event.reply(f"File size: {content_length} bytes\nStarting download")
                    progress_task = asyncio.create_task(update_progress(event, message, link))

                    command = ["wget", link, "--progress=bar:force", "-P", download_directory]

                    process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                    last_progress_update_time = time.time()

# Inside your for loop where you process the lines from the subprocess
                    for line in process.stdout:
                        line = line.strip()
                        if total_size > remaining_storage:
                            await message.edit("File size exceeds 2GB. Aborting download.")
                            process.terminate()
                            try:
                                shutil.rmtree(user_dir)
                            except Exception as e:
                                print(e)
                            link_downloading = False
                        else:
                            if line and line.endswith("s") and edit % 8 == 0:
                                try:
                                    await message.edit(line)
                                except Exception as e:
                                    print(e)
   
                            edit += 1

                    process.wait()  # Wait for the process to finish
                    progress_task.cancel()
                    if process.returncode == 0:
                        await message.edit("File downloaded successfully\n/my_files to check all your files")
                        for root, _, files in os.walk(user_dir):
                            for filename in files:
                                if not filename:
                                     await message.edit("Something went wrong\nMay be provided file is password protected")
                                file_path = os.path.join(root, filename)
                                timer = Timer()
                                async def progress_bar(current, total,start_time=time.time()):
                                    if timer.can_send():
                                        progress_percent = current * 100 / total
                                        progress_message = f"Downloading: {progress_percent:.2f}%\n"

        # Calculate speed in MB/s
                                        elapsed_time = time.time() - start_time
                                        speed = current / (elapsed_time * 1024 * 1024)
                                        progress_message += f"Speed: {speed:.2f} MB/s\n"

        # Calculate estimated time left to complete
                                        time_left = (total - current) / (speed * 1024 * 1024)
                                        progress_message += f"Time left: {time_left:.2f} seconds"

                                        progress_bar_length = int(progress_percent / 2)
                                        progress_bar_text = "█" * progress_bar_length + "░" * (50 - progress_bar_length)
        
                                        progress_message += f"\n[{progress_bar_text}]"

                # Create a message with HTML formatting for better appearance
                                        message_text = f"<b>{type_of}</b>\n{progress_message}"

                                        try:
                                            await message.edit(message_text, parse_mode='html')
                                        except Exception as e:
                                            print(e)
                                type_of = f"Uploading {filename}\nProgress:"
                                with open(file_path, "rb") as out:
                                    try:
                                        res = await upload_file(client, out, progress_callback=progress_bar)
                                        attributes, mime_type = utils.get_attributes(file_path)
                                        media = types.InputMediaUploadedDocument(
                    file=res,
                    mime_type=mime_type,
                    attributes=attributes,
                    force_file=False
                )
                                        await event.reply(file=media)
                                        await message.edit("Uploading completed")
                                    except Exception as e:
                                        await message.edit(e)
                                link_downloading = False
                                #try:
                                 #   shutil.rmtree(user_dir)
#                                except Exception as e:
 #                                   print(e)
                    else:
                        await event.reply("Download failed. Please check the URL.")
                        link_downloading = False

                    if not link_download_queue.empty():
                        next_link = link_download_queue.get()
                        user_ids.clear()
                        dd=dd-1
                        await link_download(next_link)
   
                else:
                    await event.reply("File size exceeds available storage. Aborting download.")
            else:
                await event.reply("Content length not found in headers. Cannot determine file size.")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
    else:
        dd+=1
        que=f'I have added your file in queue to download\n\nCurrent position: {dd}'
        if user_id not in user_ids:
            user_ids[user_id] = True
            user2=await event.reply(que,buttons=Button.inline("check your queue",b"bhad"))
      
        link_download_queue.put(event)

client.run_until_disconnected()
