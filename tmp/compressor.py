import asyncio
import subprocess
import shutil
import os
import time

from telethon import events, Button, utils
from telethon.sync import TelegramClient
from telethon.tl import types
from FastTelethon import download_file, upload_file

# Updated API credentials and bot
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
token = '6436886481:AAGRLX1WGWsvPyMQ5XDUSKuBCFVx7c-0tDE'
admin = 6476862483 # Replace with the actual admin user ID
client = TelegramClient(None, api_id, api_hash)

# Define the common button layout
# Define the common button layout
# Define the common button layout
help_button = Button.inline("❓ Help", b"help")  # Define the "Help" button

clear_buttons = [Button.inline("🏠 Home", b"home")]

common_buttons = [
    [
        Button.inline("🗂️ List My Files", b"my_files"),
        Button.inline("❌ Clear My Files", b"clear"),
    ],
    [
        Button.inline("🏠 Home", b"home"),
        Button.inline("🗜️📑 Compress files", b"fzip"),
    ],
    [help_button],  # Add the "Help" button
]

home_buttons = [
    [
        Button.inline("🗂️ List My Files", b"my_files"),
        Button.inline("❌ Clear My Files", b"clear"),
    ],
    [help_button],  # Add the "Help" button
]

back_buttons = [Button.inline("🏠 Home", b"home"), help_button]  # Add the "Help" button

file_buttons = [
    [
        Button.inline("❌ Clear My Files", b"clear"),
        Button.inline("🏠 Home", b"home"),
    ],
    [
        Button.inline("📑 Compress files", b"fzip"),
        help_button,  # Add the "Help" button
    ],
]

# ...

@client.on(events.CallbackQuery(data=b'help'))
async def callback_help(event):
    await event.delete()
    await help_handler(event)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
            "Hello! Send me any files and I will compress them to a zip",
            buttons=home_buttons
        )

@client.on(events.CallbackQuery(data=b'my_files'))
async def callback_my_files(event):
    await list_files(event)

@client.on(events.CallbackQuery(data=b'clear'))
async def callback_clear(event):
    await clear(event)

@client.on(events.CallbackQuery(data=b'home'))
async def callback_home(event):
    await event.delete()
    await start(event)

@client.on(events.CallbackQuery(data=b'fzip'))
async def callback_fzip(event):
    await create_zip(event)

@client.on(events.NewMessage(pattern='/my_files'))
async def list_files(event):
    user_id = str(event.sender_id)
    user_dir = f"/home/u201853/tmp/{user_id}"

    if os.path.exists(user_dir):
        files = os.listdir(user_dir)
        if files:
            total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in files)
            total_size2 = round((total_size / (1024 * 1024)), 3)
            remaining_storage = (3 * 1024 * 1024 * 1024) - total_size  # 4GB in bytes

            file_list = "\n".join([f"{i+1}. {file} - {os.path.getsize(os.path.join(user_dir, file)) / (1024 * 1024):.2f} MB" for i, file in enumerate(files)])
            response_message = f"List of files in your directory:\n\n{file_list}\n\nTotal storage used: {total_size2} MB\nRemaining Storage: {remaining_storage / (1024 * 1024 * 1024):.2f} GB"
            await event.edit(response_message, buttons=file_buttons)

        else:
            await event.edit("Your directory is empty, send me any file", buttons=file_buttons)
    else:
        await event.edit("Your directory doesn't exist, send me any file to create your directory", buttons=file_buttons)


@client.on(events.NewMessage(pattern='/clear'))
async def clear(event):
    user_directory = "/home/u201853/tmp"
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    if os.path.exists(user_path):
        shutil.rmtree(user_path,ignore_errors=True)  # Recursively remove the entire directory
        os.makedirs(user_path, exist_ok=True)  # Recreate the directory
        await event.edit(f"All files and directories in your directory have been removed.", buttons=back_buttons)
    else:
        await event.edit(f"Your directory does not exist.", buttons=back_buttons)


@client.on(events.NewMessage(pattern='/clean'))
async def clean(event):
    if event.sender_id == 6476862483:
        user_path = "/home/u201853/tmp"  # Specify the correct directory path
        if os.path.exists(user_path):
            items = os.listdir(user_path)
            for item in items:
                item_path = os.path.join(user_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            await event.edit(f"All directories and files inside {user_path} deleted successfully.", buttons=clear_buttons)
        else:
            await event.edit(f"The specified directory {user_path} does not exist.", buttons=clear_buttons)

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

import queue  # Import the queue module

# Create a queue to manage the download queue
download_queue = queue.Queue()

# Define a flag to indicate if a download process is ongoing
download_in_progress = False

@client.on(events.NewMessage)
async def main(event):
    if event.media or event.document:
        await download(event)
async def download(event):
    global download_in_progress  # Use a global flag to track download process

    if event.document.size > 1000000000:  # 1GB in bytes
        await event.reply("Please send a file smaller than 1GB.",buttons=common_buttons)
        return

    user_id = event.sender_id
    user_dir = f"/home/u201853/tmp/{user_id}"
    #user_path = os.path.join(user_directory, user_id)
    os.makedirs(user_dir, exist_ok=True)
    # Calculate the remaining storage space
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 3 * 1024 * 1024 * 1024 - total_size  # 3GB in bytes

    if event.document.size <= remaining_storage:
        type_of = "downloading\nProgress:"
        msg = None
        timer = Timer()
        #msg = await event.reply("Downloading started")

        async def progress_bar(current, total):
            if timer.can_send():
                progress_message = "{} {}%".format(type_of, current * 100 / total)
                await msg.edit(progress_message)

        os.makedirs(user_dir, exist_ok=True)
        os.chdir(user_dir)

        if not download_in_progress:
            #msg = await event.reply("Downloading started")
            download_in_progress = True  # Set the flag to indicate download process is ongoing
            fi=event.file.name
            if fi is None:
                await event.respond("!Error happened, may be this is bacause file dont have any extension")
                return
            extension = os.path.splitext(fi)[1]  # Get
            video_extensions = ['.mp4', '.avi', '.wmv', '.mov', '.mkv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp']
            if extension.lower() in video_extensions:
                await event.respond("Can't download the file, currently we do not support video file")
                return
            with open(fi, "wb") as out:
                msg = await event.reply("Downloading started")
                await download_file(event.client, event.document, out, progress_callback=progress_bar)

            download_in_progress = False  # Reset the flag after download is complete
            await msg.edit("Finished downloading", buttons=common_buttons)
            # Check if there are more files in the queue
            if not download_queue.empty():
                next_file = download_queue.get()
                await msg.delete()
                await download(next_file)
        else:
            # If download is already in progress, add the file to the queue
            download_queue.put(event)

            #await msg.edit("Finished downloading", buttons=common_buttons)
    else:
        await event.reply("Not enough storage space to download this file.",buttons=common_buttons)




import zipfile
import re


# Updated API credentials and bot




@client.on(events.NewMessage(pattern='/fzip'))
async def create_zip(event):
    user_id = str(event.sender_id)
    user_dir = f"/home/u201853/tmp/{user_id}"

    if not os.path.exists(user_dir):
        await event.reply("Your directory doesn't exist.", buttons=back_buttons)
        return

    zip_dir = os.path.join(user_dir, 'zip')
    os.makedirs(zip_dir, exist_ok=True)

    # Create a unique zip file name (you can use timestamp or any other method)
    zip_filename = os.path.join(zip_dir, f'{user_id}_files.zip')

    # List all files in the user's directory and add them to the zip archive
    files = os.listdir(user_dir)

    if not files:
        await event.edit("No files to compress.", buttons=back_buttons)
        return

    # Compress files into a zip archive
    await event.edit("Compressing files to zip please wait")
    try:
        # Use the 'zip' command via subprocess to create the zip file
        subprocess.run(['zip', '-r', zip_filename, user_dir])

        # Check if the zip file was created successfully
        if os.path.exists(zip_filename):

            # Check the size of the zip file
            file_size = os.path.getsize(zip_filename)
            await event.edit('compression completed now uploading file')
            transfer_url = "https://transfer.sh"

# Use subprocess to run the curl command
            try:
                output = subprocess.check_output(
        ["curl", "--upload-file", zip_filename, transfer_url],universal_newlines=True)
                links = re.findall(r'https://transfer.sh/.*', output)
                for link in links:
                    if link and (link.startswith("http://") or link.startswith("https://")):
                        sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                        try:
                            await event.edit(f" Not able to upload files more than 500MB here\n So I provided this download link: {sanitized_link}",buttons=Button.url("download file",sanitized_link))
                        except Exception as e:
                            print(f"Error sending link: {link}, Error: {e}")
            except subprocess.CalledProcessError as e:
                print(e)
            if os.path.exists(user_dir):
                shutil.rmtree(user_dir, ignore_errors=True)  # Rec$                    os.makedirs(user_dir, exist_ok=True)
#                await start(event)
    except Exception as e:
        await event.edit(f"An error occurred: {str(e)}", buttons=back_buttons)



client.run_until_disconnected()

