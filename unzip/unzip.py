
import py7zr
import asyncio
import subprocess
import shutil
import os
import time

from telethon import events, utils
from telethon.sync import TelegramClient
from telethon.tl import types

from FastTelethon import download_file, upload_file

# Updated API credentials and bot
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
token = '6664259125:AAE4Ro0Dsxz0hVuXdZf2kEYXmp1ZHjgwUhI'
admin = 6476862483 # Replace with the actual admin user ID
client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hello! Send me any compressed file to be uncompressed")
@client.on(events.NewMessage(pattern='/clear'))
async def clear(event):
    if event.sender_id ==6476862483:
        user_path = "/home/u201853/unzip"  # Specify the correct directory path
        if os.path.exists(user_path):
            items = os.listdir(user_path)
            for item in items:
                item_path = os.path.join(user_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            await event.respond(f"All directories and files inside {user_path} deleted successfully.")
        else:
            await event.respond(f"The specified directory {user_path} does not exist.")

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

@client.on(events.NewMessage(func=lambda e: e.document and e.is_private))
async def download(event):
    if event.document.size > 1000000000:  # 50MB in bytes
        await event.reply("Please send a file smaller than 1000MB.")
        return
    user_id = event.sender_id

    type_of = ""
    msg = None
    timer = Timer()
    type_of = "downloading\nProgress:"
    user_dir = f"/home/u201853/unzip/{user_id}"

    # Create the user directory if it doesn't exist
    os.makedirs(user_dir, exist_ok=True)
    original_working_directory = os.getcwd()
    os.chdir(user_dir)

    async def progress_bar(current, total):
        if timer.can_send():
            progress_message = "{} {}%".format(type_of, current * 100 / total)
            await msg.edit(progress_message)



    msg = await event.reply("downloading started")
    with open(event.file.name, "wb") as out:
        fill=await download_file(event.client,event.document, out, progress_callback=progress_bar)

    await msg.edit("Finished downloading")

    # Unzip the downloaded file
    file_path=event.file.name
    file_extension = os.path.splitext(file_path)[1].lower()

    #magiskboot = "./magiskboot"  # Replace with the actual path to the magiskboot tool

# Define magic bytes for supported compression methods
    compression_magic_bytes = {
    b'\x50\x4b\x03\x04': 'zip',      # ZIP
    b'\x1f\x8b\x08': 'gz',          # GZIP
    b'\x42\x5a\x68': 'bz2',         # BZIP2
    b'\xfd\x37\x7a\x58\x5a\x00': 'xz', # XZ
    b'\x52\x61\x72\x21': 'rar',     # RAR
    b'\x1f\x9d': 'tar.Z',           # Compressed TAR
    b'7z\xbc\xaf\x1c':'7z', # Add more magic bytes for other compression methods as needed
    }
    with open(file_path, 'rb') as f:
        file_signature = f.read(6)
        print(file_signature)

# Check if the magic bytes match any supported compression methods
    compression_method = None
    for magic_bytes, method in compression_magic_bytes.items():
        if file_signature.startswith(magic_bytes):
            compression_method = method
            break
    #subprocess.run(['cp','-r', 'magiskboot', {user_dir}])
    if compression_method == 'zip' or file_extension == '.zip':
        subprocess.run(['unzip', file_path, '-d', user_dir])
    elif compression_method == 'gz' or file_extension == '.gz':
        subprocess.run(['gzip', '-d', '-c', file_path], stdout=open(os.path.join(user_dir, os.path.basename(file_path)[:-3]), 'wb'))
    elif compression_method == 'bz2' or file_extension == '.bz2':
        subprocess.run(['bzip2', '-d', '-c', file_path], stdout=open(os.path.join(user_dir, os.path.basename(file_path)[:-4]), 'wb'))
    elif compression_method == 'xz' or file_extension == '.xz':
        subprocess.run(['xz', '-d', '-c', file_path], stdout=open(os.path.join(user_dir, os.path.basename(file_path)[:-3]), 'wb'))
    elif compression_method == 'rar' or file_extension == '.rar':
        subprocess.run(['unrar', 'x', file_path, user_dir])
    elif compression_method == 'tar.Z' or file_extension == '.tar.Z':
        subprocess.run(['tar', 'xzf', file_path, '-C', user_dir])
    elif compression_method == '7z' or file_extension == '.7z':
        subprocess.run(['7z', 'x', file_path, '-o' + user_dir])
    else:
        await event.reply("Unsupported compression method")
    os.remove(event.file.name)
    os.chdir(original_working_directory)
# Example usag


    # After unzipping, upload the files
    msg = await event.respond("uploading started")

    for root, _, files in os.walk(user_dir):
        for filename in files:
            if not filename:
                await msg.edit("Something went wrong\nMay be provided file is password protected")
            file_path = os.path.join(root, filename)
            type_of = f"uploading {filename}\nProgress:"
            with open(file_path, "rb") as out:
                res = await upload_file(client, out, progress_callback=progress_bar)
                attributes, mime_type = utils.get_attributes(file_path)
                media = types.InputMediaUploadedDocument(
                    file=res,
                    mime_type=mime_type,
                    attributes=attributes,
                    force_file=False
                )
                await event.reply(file=media)
    shutil.rmtree(user_dir)
    await msg.edit("Uploading completed")
#    await msg.edit("Finished uploading")
import os
import shutil
import subprocess
from telethon import events, types, utils
from telethon.sync import TelegramClient

# Your other code remains the same...

@client.on(events.NewMessage(pattern='/unzip'))
async def unzip(event):
    replied_message = await event.get_reply_message()

    if not replied_message:
        await event.respond("Please reply to a message containing the compressed file.")
        return

    if replied_message.file.name.endswith('.apk'):
        await event.reply("Don't try to uncompress an APK file.")
        return

    if not replied_message.document:
        await event.respond("The replied message does not contain a document.")
        return

    if replied_message.document.size > 1000000000:  # 1000MB in bytes
        await event.respond("Please send a file smaller than 1000MB.")
        return

    user_id = event.sender_id
    type_of = ""
    msg = None
    timer = Timer()
    type_of = "downloading\nProgress:"
    user_dir = f"/home/u201853/unzip/{user_id}"

    # Create the user directory if it doesn't exist
    os.makedirs(user_dir, exist_ok=True)
    original_working_directory = os.getcwd()
    os.chdir(user_dir)

    async def progress_bar(current, total):
        if timer.can_send():
            progress_message = "{} {}%".format(type_of, current * 100 / total)
            await msg.edit(progress_message)

    msg = await event.respond("Unzipping started")
    try:
        with open(replied_message.file.name, "wb") as out:
            await download_file(event.client, replied_message.document, out, progress_callback=progress_bar)

        await msg.edit("Finished downloading")

        # Unzip the downloaded file
        file_path = replied_message.file.name
        file_extension = os.path.splitext(file_path)[1].lower()

        compression_magic_bytes = {
            b'\x50\x4b\x03\x04': 'zip',
            b'\x1f\x8b\x08': 'gz',
            b'\x42\x5a\x68': 'bz2',
            b'\xfd\x37\x7a\x58\x5a\x00': 'xz',
            b'\x52\x61\x72\x21': 'rar',
            b'\x1f\x9d': 'tar.Z',
            b'7z\xbc\xaf\x1c': '7z',
        }

        with open(file_path, 'rb') as f:
            file_signature = f.read(6)

        compression_method = None
        for magic_bytes, method in compression_magic_bytes.items():
            if file_signature.startswith(magic_bytes):
                compression_method = method
                break

        if compression_method == 'zip' or file_extension == '.zip':
            subprocess.run(['unzip', file_path, '-d', user_dir])
        elif compression_method == 'gz' or file_extension == '.gz':
            subprocess.run(['gzip', '-d', '-c', file_path], stdout=open(os.path.join(user_dir, os.path.basename(file_path)[:-3]), 'wb'))
        # Add more elif conditions for other compression methods as needed

        else:
            await event.respond("Unsupported compression method")
    except Exception as e:
        await event.respond(f"Unable to uncompress the file: {str(e)}")

    os.remove(replied_message.file.name)
    os.chdir(original_working_directory)

    # After unzipping, upload the files
    msg = await event.respond("Uploading started")

    for root, _, files in os.walk(user_dir):
        for filename in files:
            if not filename:
                await msg.edit("Something went wrong\nMay be provided file is password protected")
            file_path = os.path.join(root, filename)
            type_of = f"Uploading {filename}\nProgress:"
            with open(file_path, "rb") as out:
                res = await upload_file(client, out, progress_callback=progress_bar)
                attributes, mime_type = utils.get_attributes(file_path)
                media = types.InputMediaUploadedDocument(
                    file=res,
                    mime_type=mime_type,
                    attributes=attributes,
                    force_file=False
                )
                await event.reply(file=media)
    shutil.rmtree(user_dir)
    await msg.edit("Uploading completed")

# Your other code r

@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    help_message = (
        "Welcome to the File Compression Bot!\n"
        "Here are the available commands:\n\n"
        "/start - Start the bot\n"
        "/unzip - Reply to any file to uncompress the filw\n"
        "/help - Show this help message\n"
    )

    await event.reply(help_message)


client.run_until_disconnected()
