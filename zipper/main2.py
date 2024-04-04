from FastTelethonhelper import fast_download
import cryptg
import requests
import datetime
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
group_user_ids = {}
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
nofile_buttons = [
    [
        Button.inline("❌ Clear My Files", b"clear"),
        Button.inline("🏠 Home", b"home"),
    ],
[        help_button,  # Add the "Help" button
    ],
]

# ...
# ...

@client.on(events.CallbackQuery(data=b'help'))
async def callback_help(event):
    await event.delete()
    await help_handler(event)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/start'))
async def start(event):
    await event.respond(
            "Hello! Send me any files and I will compress them to a zip",
            buttons=home_buttons)

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

# Define a dictionary to store user states
user_states = {}

# ...

@client.on(events.CallbackQuery(data=b'fzip'))
async def callback_fzip(event):
    user_id = event.sender_id
    user_states[user_id] = "waiting_for_rename"  # Set the user's state to "waiting_for_rename"
    try:
        await event.edit("Please give me a suitable name for the compressed file.\n\nNote: name should contain extension also")
    except:
        await event.respond("Please give me a suitable name for the compressed file.\n\nNote: name should contain extension also")
# ...

@client.on(events.NewMessage(func=lambda e: e.text and e.is_private))
async def handle_message(event):
    user_id = event.sender_id
    user_state = user_states.get(user_id)

    if user_state == "waiting_for_rename":
        user_states[user_id] = "ready"  # Reset the user's state
        global file_name
        file_name = event.text
        await create_zip(event)  # Call the create_zip function to proceed with compression
    else:
        # Handle other messages or commands here
        pass


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/my_files'))
async def list_files(event):
    user = await event.get_sender()
    user_id = user.id
    group = await client.get_entity("@nub_coder_s")

    global group_user_ids

    # Fetch all user IDs in the group and store them in the dictionary
    async for member in client.iter_participants(group):
        group_user_ids[member.id] = True

    # Check if the user is in the group by looking up their ID in the dictionary
    if user_id not in group_user_ids:
        button = Button.url("Join", "https://t.me/nub_coder_s")
        await event.respond("You need to join @nub_coder_s in order to use this bot.\n\nClick below to Join!", buttons=button)
        return
    group_user_ids.clear()
    
    user_id = str(event.sender_id)
    user_dir = f"/home/u201853/compressor/{user_id}"

    if os.path.exists(user_dir):
        files = os.listdir(user_dir)
        if files:
            total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in files)
            total_size2 = round((total_size / (1024 * 1024)), 3)
            remaining_storage = (4.5 * 1024 * 1024 * 1024) - total_size  # 4GB in bytes

            file_list = "\n".join([f"{i+1}. {file} - {os.path.getsize(os.path.join(user_dir, file)) / (1024 * 1024):.2f} MB" for i, file in enumerate(files)])
            response_message = f"List of files in your directory:\n\n{file_list}\n\nTotal storage used: {total_size2} MB\nRemaining Storage: {remaining_storage / (1024 * 1024 * 1024):.2f} GB"
            try:
                await event.edit(response_message, buttons=file_buttons)
            except:
                await event.respond(response_message, buttons=file_buttons)
        else:
            try:
                await event.edit("Your directory is empty, send me any file", buttons=nofile_buttons)
            except:
                await event.respond("Your directory is empty, send me any file", buttons=nofile_buttons)
    else:
        try:
            await event.edit("Your directory doesn't exist, send me any file to create your directory", buttons=nofile_buttons)

        except:
            await event.respond("Your directory doesn't exist, send me any file to create your directory", buttons=nofile_buttons)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/clear'))
async def clear(event):
    user_directory = "/home/u201853/compressor"
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    if os.path.exists(user_path):
        shutil.rmtree(user_path,ignore_errors=True)  # Recursively remove the entire directory
        os.makedirs(user_path, exist_ok=True)  # Recreate the directory
        try:
            await event.edit(f"All files and directories in your directory have been removed.", buttons=back_buttons)
        except:
             await event.respond(f"All files and directories in your directory have been removed.", buttons=back_buttons)
    else:
        try:
            await event.edit(f"Your directory does not exist.", buttons=back_buttons)
        except:
            await event.respond(f"Your directory does not exist.", buttons=back_buttons)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/clean'))
async def clean(event):
    if event.sender_id == 6476862483:
        user_path = "/home/u201853/compressor"  # Specify the correct directory path
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

# Store user state to track when to downlo
import queue  # Import the queue module
dd=0
# Create a queue to manage the download queue
download_queue = queue.Queue()
user1=None
user2=None
user3=None
user4=None
user5=None
download_progress = {}

# Define a flag to indicate if a download process is ongoing
download_in_progress = False
user_ids = {}
link_download_queue = queue.Queue()
link_downloading = False  # Flag to track if a link download is in progress
# ... (previous code remains the same)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def main(event):
    if event.raw_text.startswith("http"):
        await link_download(event)
    elif event.media or event.document:
        await download(event)

async def download(event):
    global download_in_progress
    global user_ids
    global dd

    # Check if the user has previously initiated a download
    user_id = event.sender_id
    if user_id in download_progress:
        # Resume the interrupted download
        await resume_download(event, download_progress[user_id])
    else:
        # Start a new download
        await start_download(event)

async def start_download(event):
    # Initialize download parameters and progress tracking
    user_id = event.sender_id
    download_progress[user_id] = {'current_bytes': 0}
    global download_in_progress
    global user_ids
    global dd
    # Rest of your download logic here
    size = 0
    if event.document:
        if event.document.size > 2000000000:
            await event.reply("Please send a file smaller than 2GB.\n/my_files to show your files", buttons=common_buttons)
            return

    user_dir = f"/home/u201853/compressor/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 4.5 * 1024 * 1024 * 1024 - total_size

    if event.document:
        docs = event.document
        size = event.document.size
    if event.photo:
        docs = event.media
        size = 100
    if size <= remaining_storage:
        type_of = "downloading\nProgress:"
        msg = None
        timer = Timer()

        async def progress_bar(current, total):
            if timer.can_send():
                progress_message = "{} {}%".format(type_of, current * 100 / total)
                try:
                    await msg.edit(progress_message)
                except Exception as e:
                    print(e)

        os.makedirs(user_dir, exist_ok=True)
        os.chdir(user_dir)

        if not download_in_progress and not link_downloading:
            user_ids[user_id] = True
            time.sleep(2)
            download_in_progress = True
            fi = event.file.name

            if fi is None and event.photo:
                msg = await event.reply("Downloading file please wait")
                await client.download_media(event.media, file=user_dir)
            if fi is not None:
                extension = os.path.splitext(fi)[1]
                fi_encoded = fi.encode('utf-8')
                with open(fi_encoded, "wb") as out:
                    msg = await event.reply("Downloading started")
                    await download_file(event.client, docs, out, progress_callback=progress_bar)
            download_in_progress = False
            await msg.edit("Finished downloading\n/my_files to see your files")

            if not download_queue.empty():
                next_file = download_queue.get()
                await download(next_file)
                user_ids.clear()
                dd = dd - 1
        else:
            dd += 1
            que = f'I have added your file in queue to download\n\nCurrent position: {dd}'
            if user_id not in user_ids:
                user_ids[user_id] = True
            await event.reply(que)

            download_queue.put(event)

    else:
        await event.reply("Not enough storage space to download this file.", buttons=common_buttons)

async def resume_download(event, progress):
    user_id = event.sender_id
    current_bytes = progress['current_bytes']

    # Resume the download from the last saved position
    # You can use the 'current_bytes' to specify the start position in the file

    # Rest of your download logic here
    size = 0
    if event.document:
        if event.document.size > 2000000000:
            await event.reply("Please send a file smaller than 2GB.\n/my_files to show your files", buttons=common_buttons)
            return

    user_dir = f"/home/u201853/compressor/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 4.5 * 1024 * 1024 * 1024 - total_size

    if event.document:
        docs = event.document
        size = event.document.size
    if event.photo:
        docs = event.media
        size = 100
    if size <= remaining_storage:
        type_of = "downloading\nProgress:"
        msg = None
        timer = Timer()

        async def progress_bar(current, total):
            if timer.can_send():
                progress_message = "{} {}%".format(type_of, current * 100 / total)
                try:
                    await msg.edit(progress_message)
                except Exception as e:
                    print(e)

        os.makedirs(user_dir, exist_ok=True)
        os.chdir(user_dir)

        if not download_in_progress and not link_downloading:
            user_ids[user_id] = True
            time.sleep(2)
            download_in_progress = True
            fi = event.file.name

            if fi is None and event.photo:
                msg = await event.reply("Downloading file please wait")
                await client.download_media(event.media, file=user_dir)
            if fi is not None:
                extension = os.path.splitext(fi)[1]
                fi_encoded = fi.encode('utf-8')
                with open(fi_encoded, "wb") as out:
                    msg = await event.reply("Downloading started")
                    await download_file(event.client, docs, out, progress_callback=progress_bar)
            download_in_progress = False
            await msg.edit("Finished downloading\n/my_files to see your files")

            if not download_queue.empty():
                next_file = download_queue.get()
                await download(next_file)
                user_ids.clear()
                dd = dd - 1
        else:
            dd += 1
            que = f'I have added your file in queue to download\n\nCurrent position: {dd}'
            if user_id not in user_ids:
                user_ids[user_id] = True
            await event.reply(que)

            download_queue.put(event)

    else:
        await event.reply("Not enough storage space to download this file.", buttons=common_buttons)




import zipfile
import re

# Updated API credentials and bot

video_sent=False
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/fzip'))
async def fzip(event):
    await callback_fzip(event)
async def create_zip(event):
    user = await event.get_sender()
    user_iid = user.id
    group = await client.get_entity("@nub_coder_s")

    global group_user_ids
    global file_name
    if file_name.startswith("/") or file_name.startswith("http"):
        return
    # Fetch all user IDs in the group and store them in the dictionary
    async for member in client.iter_participants(group):
        group_user_ids[member.id] = True

    # Check if the user is in the group by looking up their ID in the dictionary
    if user_iid not in group_user_ids:
        button = Button.url("Join", "https://t.me/nub_coder_s")
        await event.respond("You need to join @nub_coder_s in order to use this bot.\n\nClick below to Join!", buttons=button)
        return
    group_user_ids.clear()
    user_id = str(event.sender_id)
    user_dir = f"/home/u201853/compressor/{user_id}"
    if not os.path.exists(user_dir):
        await event.reply("Your directory doesn't exist.", buttons=back_buttons)
        return

    # List all files in the user's directory and add them to the zip archive
    files = os.listdir(user_dir)

    if not files:
        try:
            await event.edit("No files to compress.", buttons=back_buttons)
        except:
            await event.respond("No files to compress.", buttons=back_buttons)
        return
    zip_dir = os.path.join(user_dir, 'zip')
    os.makedirs(zip_dir, exist_ok=True)

    if not file_name.endswith('.zip'):
        file_name=f'{file_name}.zip'

    # Create a unique zip file name (you can use timestamp or any other method)
    zip_filename= file_name
    video_extensions = ['.mp4', '.avi', '.wmv', '.mov', '.mkv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp']
    video_files = [file for file in files if os.path.splitext(file)[1].lower() in video_extensions]
    global video_sent
    if video_files:
        video_sent=True
    # Compress files into a zip archive
    try:
        await event.edit("Compressing files to zip please wait")
    except:
        await event.respond("Compressing files to zip please wait")
    try:
        # Use the 'zip' command via subprocess to create the zip file
        count = 0

        for filename in os.listdir(user_dir):
            if count % 8 == 0 and count != 0:
                time.sleep(2)  # Wait for 5 seconds

            subprocess.run(['zip', '-r', zip_filename, os.path.join(user_dir, filename)])
            count += 1

        # Check if the zip file was created successfully
        if os.path.exists(zip_filename):

            # Check the size of the zip file
            file_size = os.path.getsize(zip_filename)
            await event.respond('compression completed now uploading file')
            if file_size <= 500000000:  # 1000 MB in bytes
                type_of = "Uploading\nProgress:"
                msg = None
                timer = Timer()
        # File size is less than or equal to 1000 MB, upload as is
                async def progress_bar(current, total):
                    if timer.can_send():
                        progress_message = "{} {}%".format(type_of, current * 100 / total)
                        await msg.edit(progress_message)

                type_of = f"Uploading Compressed file\nProgress:"
                msg = await event.respond("uploading started")

                with open(zip_filename, "rb") as out:
                    res = await upload_file(client, out, progress_callback=progress_bar)
                    attributes, mime_type = utils.get_attributes(zip_filename)
                    media = types.InputMediaUploadedDocument(
                        file=res,
                        mime_type=mime_type,
                        attributes=attributes,
                        force_file=False
                    )

                    await msg.edit('Uploaded successfully\n\nPlease join @nub_coder_s', buttons=home_buttons)
                    await event.respond(file=media)
                    if os.path.exists(user_dir):
                        shutil.rmtree(user_dir, ignore_errors=True)  # Recursivel$
                        os.makedirs(user_dir, exist_ok=True)
            elif file_size <= 3000000000 and not video_sent:
                # File size is greater than 1000 MB, use the external script for upload
                key = "132485nxw6omzhbg9c4qd"
                script_url = "https://devuploads.com/upload.sh"
                script_name = "upload.sh"

                # Download the script
                subprocess.run(["curl", "-s", "-o", script_name, script_url])

                if os.path.exists(zip_filename):
                    command = f"bash {script_name} -f {zip_filename} -k {key}"
                    output = subprocess.check_output(command, shell=True, text=True)

                    # Use regular expression to find and print the links
                    links = re.findall(r'https://devuploads\.com/.*', output)
                    for link in links:
                        if link and (link.startswith("http://") or link.startswith("https://")):
                            sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
        # Remove non-alphanumeric characters from the link                                                      sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                            jink=sanitized_link.replace("0m","")
                            try:
                                await event.edit(f" Not able to upload files more than 500MB here\n So I provided this download ",buttons=Button.url("download file",jink))
                            except Exception as e:
                                print(f"Error sending link: {link}, Error: {e}")
                        else:
                            print(f"Invalid link: {link}")                     # ... (previous code remains the same)
                    if os.path.exists(user_dir):
                        shutil.rmtree(user_dir, ignore_errors=True)  # Rec$
                        os.makedirs(user_dir, exist_ok=True)
                        await start(event)
            elif file_size <= 3000000000 and video_sent:
                video_sent = False
                file_size = os.path.getsize(zip_filename)

                if file_size > 5000000000:  # 5000 MB
                    await event.reply("File size is too large to upload here. Please use an alternative method.", buttons=back_buttons)
                    return

                await event.respond('Compression completed. Uploading file...')

                transfer_url = "https://transfer.sh"
                try:
        # Use subprocess to run the curl command to upload the zip file
                    output = subprocess.check_output(["curl", "--upload-file", zip_filename, transfer_url], universal_newlines=True)
                    print(output)
                    links = re.findall(r'https://transfer.sh/.*', output)
                    print(links)
                    for link in links:
                        if link and (link.startswith("http://") or link.startswith("https://")):
                            #sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                            #print(sanitized_link)
                            try:
                                await event.respond(f"Not able to upload files more than 500MB here\n So I provided this download link:", buttons=Button.url("Download File",link))
                            except Exception as e:
                                print(f"Error sending link: {link}, Error: {e}")
                except subprocess.CalledProcessError as e:
                    print(e)
                    await start(event)
    # Clean up the user directory
                if os.path.exists(user_dir):
                    shutil.rmtree(user_dir, ignore_errors=True)
        os.makedirs(user_dir, exist_ok=True)

    except Exception as e:
        await event.edit(f"An error occurred: {str(e)}", buttons=back_buttons)
        print(e)


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/help'))
async def help_handler(event):
    user_id = str(event.sender_id)
    user_dir = f"/home/u201853/compressor/{user_id}"

    # Provide information about the bot
    help_message = (
        "🤖 **File Compression Bot Help** 🤖\n\n"
        "This bot allows you to compress files into zip archives and manage your files.\n\n"
        "📋 **Available Commands:**\n"
        "/start - Start the bot\n"
        "/my_files - List your files\n"
        "/clear - Clear your files\n"
        "/fzip - Compress files into a zip archive\n"
        "/help - Show this help message\n\n"
        "🚧 **Limitations:**\n"
        "- Maximum file size for compression: 1GB\n"
        "- Maximum storage per user: 3GB\n\n"
        "📞 **Support:**\n"
        "If you need assistance or have any questions, please contact the bot admin.\n"
        f"Admin : @nub_coder_s\n\n"
        "Enjoy using the bot! 🚀"
    )

    # Send the help message with the common buttons
    await event.respond(help_message, buttons=common_buttons)


edit=0
# ... (previous code remains the same)
async def update_progress(event, message, link):
    while True:
        await asyncio.sleep(3)  # Update progress every 5 seconds
        
async def link_download(event):
    global link_downloading
    global dd
    global user2
    global edit
    link=event.raw_text

    link = event.raw_text
    user_id = event.sender_id
    user_dir = f"/home/u201853/compressor/{user_id}"
    download_directory = user_dir

    max_file_size_bytes = 4 * 1024 * 1024 * 1024  # 4 GB in bytes
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 4.5 * 1024 * 1024 * 1024 - total_size  # 3GB in bytes
    os.makedirs(user_dir, exist_ok=True)
    if not link_downloading and not download_in_progress:
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
                    
                    for line in process.stdout:
                        line = line.strip()
                    
                        if line and line.endswith("s") and edit % 8 ==0:
                            await message.edit(line)
                        edit+=1
                    process.wait()  # Wait for the process to finish
                    progress_task.cancel()
                    if process.returncode == 0:
                        await message.edit("File downloaded successfully")
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
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
    else:
        dd+=1
        que=f'I have added your file in queue to download\n\nCurrent position: {dd}'
        if user_id not in user_ids:
            user_ids[user_id] = True
            user2=await event.reply(que)
      
        link_download_queue.put(event)

# ... (previous code remains the same)

client.run_until_disconnected()


