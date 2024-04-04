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
import sys  # Import the sys module at the beginning of your code


# Directory path
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
token = '6239906461:AAFrz8NvMpG5o9oXGIx_XDEl34ulTK18wtY'
admin = 6476862483 # Replace with the actual admin user ID
time.sleep(2)
client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage(pattern='^!skip$'))
async def skip_handler(event):
    global dd
    user_id = event.sender_id
    global link_downloading
    global download_in_progress
    global zipping_in_progress

    # Check if the user is an admin by comparing their user ID with the ones in admin.txt
    admin_file = "/etc/secrets/admin.txt"
    if os.path.exists(admin_file):
        with open(admin_file, "r") as file:
            admin_ids = [int(line.strip()) for line in file.readlines()]
            if user_id in admin_ids:
                await event.respond("Admin command received. Skipping the task...")
                await timeout(event)




async def timeout(event):
    global dd
    global max_retry
    max_retry=0
    user_id = event.sender_id
    global zipping_in_progress
    global link_downloading
    global download_in_progress
    zipping_in_progress=False
    link_downloading = False
    download_in_progress = False
    if not download_queue.empty():

                 next_file = download_queue.get()
                 dd=dd-1
                 user_ids.clear()
                 await download(next_file)
    elif not link_download_queue.empty():
                 next_link = link_download_queue.get()
                 dd=dd-1
                 user_ids.clear()
                 await link_download(next_link)
def read_chat_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            chat_ids = file.readlines()
            chat_ids = [chat_id.strip() for chat_id in chat_ids]
            return chat_ids
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# Path to your user.txt file
file_path = 'user.txt'

@client.on(events.NewMessage(pattern='/loud'))
async def loud_message(event):
    user_id = event.sender_id

    # Check if the user is an admin by comparing their user ID with the ones in admin.t$
    admin_file = "/etc/secrets/admin.txt"
    if os.path.exists(admin_file):
        with open(admin_file, "r") as file:
            admin_ids = [int(line.strip()) for line in file.readlines()]
            if user_id not in admin_ids:
             return
    chat_ids = read_chat_ids_from_file(file_path)
    if event.is_reply:
        try:
            reply_message = await event.get_reply_message()
            # Check if the replied message is text or media
            if reply_message:
                # If it's text, forward the text message
                # If it's media, forward the media message
                for chat_id in chat_ids:
                    try:
                        await client.forward_messages(int(chat_id), reply_message)
                    except Exception as e:
                        print(f"Failed to forward message: {e}")
        except Exception as e:
            print(f"Failed to forward message: {e}")
@client.on(events.NewMessage(pattern='^!reboot$'))
async def reboot_handler(event):
    user_id = event.sender_id

    # Check if the user is an admin by comparing their user ID with the ones in admin.txt
    admin_file = "/etc/secrets/admin.txt"
    if os.path.exists(admin_file):
        with open(admin_file, "r") as file:
            admin_ids = [int(line.strip()) for line in file.readlines()]
            if user_id in admin_ids:
                await event.respond("Admin command received. Stopping the bot...")
                sys.exit(0)  # Raise a system exit exception to stop the entire code
            else:
                await event.respond("You are not authorized to use this command.")
    else:
        await event.respond("Admin file not found. Please contact the bot admin.")

links = {
    'Monday_phase1': 'https://xpshort.com/reverify',
    'Monday_phase2': 'https://xpshort.com/reverify1',
    'Monday_phase3': 'https://xpshort.com/reverify2',
    'Monday_phase4': 'https://xpshort.com/reverify3',
    'Tuesday_phase1': 'https://xpshort.com/reverify4',
    'Tuesday_phase2': 'https://xpshort.com/reverify5',
    'Tuesday_phase3': 'https://xpshort.com/reverify6',
    'Tuesday_phase4': 'https://xpshort.com/reverify7',
    'Wednesday_phase1': 'https://xpshort.com/reverify8',
    'Wednesday_phase2': 'https://xpshort.com/reverify9',
    'Wednesday_phase3': 'https://xpshort.com/reverify10',
    'Wednesday_phase4': 'https://xpshort.com/reverify11',
    'Thursday_phase1': 'https://xpshort.com/reverify12',
    'Thursday_phase2': 'https://xpshort.com/reverify13',
    'Thursday_phase3': 'https://xpshort.com/reverify14',
    'Thursday_phase4': 'https://xpshort.com/reverify15',
    'Friday_phase1': 'https://xpshort.com/reverify16',
    'Friday_phase2': 'https://xpshort.com/reverify17',
    'Friday_phase3': 'https://xpshort.com/reverify18',
    'Friday_phase4': 'https://xpshort.com/reverify19',
    'Saturday_phase1': 'https://xpshort.com/reverify20',
    'Saturday_phase2': 'https://xpshort.com/reverify21',
    'Saturday_phase3': 'https://xpshort.com/reverify22',
    'Saturday_phase4': 'https://xpshort.com/reverify23',
    'Sunday_phase1': 'https://xpshort.com/reverify24',
    'Sunday_phase2': 'https://xpshort.com/reverify25',
    'Sunday_phase3': 'https://xpshort.com/reverify26',
    'Sunday_phase4': 'https://xpshort.com/reverify27',

}
uuser_ids={}
days_of_week = {
    'Monday_phase1': '/start verifycodeis27373636384747',
    'Monday_phase2': '/start verifycodeis273733764778',
    'Monday_phase3': '/start verifycodeis273736327364637',
    'Monday_phase4': '/start verifycodeis27373636737473',
    'Tuesday_phase1': '/start verifycodeis2737363373748484',
    'Tuesday_phase2': '/start verifycodeis27373636e626353747',
    'Tuesday_phase3': '/start verifycodeis27373636365449',
    'Tuesday_phase4': '/start verifycodeis27373755635449',
    'Wednesday_phase1': '/start verifycodeis2737363636758',
    'Wednesday_phase2': '/start verifycodeis27373666365449',
    'Wednesday_phase3': '/start verifycodeis27373636365744',
    'Wednesday_phase4': '/start verifycodeis27373636364487',
    'Thursday_phase1': '/start verifycodeis27373636365644',
    'Thursday_phase2': '/start verifycodeis27373636366744',
    'Thursday_phase3': '/start verifycodeis273736363534799',
    'Thursday_phase4': '/start verifycodeis2737363664897876',
    'Friday_phase1': '/start verifycodeis27373636364377',
    'Friday_phase2': '/start verifycodeis27373636354478',
    'Friday_phase3': '/start verifycodeis27373636329383',
    'Friday_phase4': '/start verifycodeis27373636365437373',
    'Saturday_phase1': '/start verifycodeis27373636362737363',
    'Saturday_phase2': '/start verifycodeis27373636286364',
    'Saturday_phase3': '/start verifycodeis27373636363874',
    'Saturday_phase4': '/start verifycodeis2737363373664',                                                                'Sunday_phase1': '/start verifycodeis273736327263648',
    'Sunday_phase2': '/start verifycodeis2737363639127644',
    'Sunday_phase3': '/start verifycodeis2737363827374',                                                                  'Sunday_phase4': '/start verifycodeis2737363443648',
}



group_user_ids = {}
# Define the common button layout
help_button = Button.inline("❓ Help", b"help")  # Define the "Help" button
mesaage=None
clear_buttons = [Button.inline("🏠 Home", b"home")]
cancel_download_button = Button.inline("❌ Cancel Download", b"cancel_download")
common_buttons = [
    [   Button.inline("🗂️ List My Files", b"my_files"),
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
        Button.inline("🏠 Home", b"home"),                                                                                ],
[        help_button,  # Add the "Help" button
    ],

]

@client.on(events.CallbackQuery(data=b'cancel_download'))
async def cancel_download(event):
    user_id = event.sender_id

    # Check if the user has an ongoing download                                                                           
    if user_id in user_ids:
        # Remove the user from the queue                                                                                      
        if not download_queue.empty():
            download_queue.queue.remove(event)                                                                                
# Reset the user's download status
        del user_ids[user_id]
        # Respond with a cancellation message
        await event.edit("Download canceled.")
    else:
        await event.edit("No ongoing download to cancel.")


async def link_send(event):

# Get the current date and time
# Define the phases for each day
    phases = ['phase1', 'phase2', 'phase3', 'phase4']
# Get the current day and time
    current_datetime = datetime.datetime.now()

# Calculate the current phase based on the time of day
    current_hour = current_datetime.hour
    phase_index = (current_hour // 6) % 4  # 6 hours per phase, modulo 4 to cycle through phases

# Get the name of the current day
    day_name = current_datetime.strftime('%A')

# Combine the day name and phase
    output = f'{day_name}_{phases[phase_index]}'
# Print the result
    await event.respond("you need to verify first in order to use the bot to avoid spam",buttons=[Button.url("Click to verify",links[output]),Button.url("how to verify","https://t.me/nub_coder_s_updates/3")])

@client.on(events.NewMessage(pattern='/start'))
async def lstart(event):
    if event.raw_text=="/start":
        return
    print(event.raw_text)
    user_id = event.sender_id
    current_time = time.time()
# Get the current day of the week
    phases = ['phase1', 'phase2', 'phase3', 'phase4']

# Get the current day and time
    current_datetime = datetime.datetime.now()

# Calculate the current phase based on the time of day
    current_hour = current_datetime.hour
    phase_index = (current_hour // 6) % 4  # 6 hours per phase, modulo 4 to cycle through phases

# Get the name of the current day
    day_name = current_datetime.strftime('%A')

# Combine the day name and phase                                                                                          
    output = f'{day_name}_{phases[phase_index]}'
    # Check if the user's message contains the special start link
    if days_of_week[output] == event.raw_text:
            # Add the new user ID with an expiration time of 1 day (86400 seconds)
        uuser_ids[user_id] = current_time +  14400

            # Send a welcome message to the new user
        await event.respond("Welcome back to the bot! You are verified for 4 hours",buttons=home_buttons)

            # User already exists, check if their expiration time has passed

    if  days_of_week[output] != event.raw_text:
        await event.respond("Wrong link, please try again")
        await link_send(event)
                # User exists and their access is still valid
# ...
active_user_id =None
# ...
@client.on(events.CallbackQuery(data=b'bhad'))
async def callback_queue(event):
    global dd
    global active_user_id
    user_id = event.sender_id

    # Check if the user is an admin by comparing their user ID with the ones in admin.t$
    admin_file = "/etc/secrets/admin.txt"
    if 2==2:
                user_task_counts = {}

    # Iterate through the events in the download queue and count tasks per user
                for download_event in download_queue.queue:
                    user_id = download_event.sender_id

                    if user_id in user_task_counts:
                        user_task_counts[user_id] += 1
                    else:
                        user_task_counts[user_id] = 1

    # Iterate through the events in the link download queue and update counts
                for link_event in link_download_queue.queue:
                    user_id = link_event.sender_id
                    if user_id in user_task_counts:
                        user_task_counts[user_id] += 1
                    else:
                        user_task_counts[user_id] = 1
                if active_user_id:
                    response_text = f"ACTIVE USER ⚡: {active_user_id}\n\n\n"
                else:
                    response_text = "No active downloads or uploads\n\n\n"

                response_text += "DOWNLOAD IN QUEUE:\n"
                for user_id, task_count in user_task_counts.items():
                    response_text += f"{user_id}:({task_count} tasks)\n\n\n"
                response_text += f"\nNEXT QUEUE IN: {time_left} seconds"
                try:
                    await event.answer(response_text, alert=True)
                except Exception as e:
                    await event.answer(f"your current queue {dd}", alert=True)

@client.on(events.CallbackQuery(data=b'help'))
async def callback_help(event):
    await event.delete()
    await help_handler(event)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/start'))
async def start(event):
    user_file_path = 'user.txt'  # Update with your file path
    user_exists = False
    user_chat_id=str(event.chat_id)
    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as user_file:
            user_ids = user_file.read().splitlines()
            if user_chat_id in user_ids:
                user_exists = True

    # If the user's chat_id is not present, append it to the file
    if not user_exists:
        with open(user_file_path, 'a+') as user_file:
            user_file.write(user_chat_id + '\n')
    await event.respond(
            "Hello! Send me any files or direct download link  and I will compress them to a zip",
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
    if user_id not in uuser_ids:
       return await link_send(event)
       #await event.respond("you need to verify first in order to use the bot to avoid spam",buttons=[Button.url("Click to verify",links[Today]),Button.url("how to verify","https://t.me/nub_coder_s_updates/3")])
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
        return await event.respond("You need to join @nub_coder_s in order to use this bot.\n\nClick below to Join!", buttons=button)
    group_user_ids.clear()


    user_id = str(event.sender_id)
    user_dir = user_id

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


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text.startswith('/del ')))
async def delete_file(event):
    user_id = str(event.sender_id)
    user_dir = user_id

    # Extract the file number from the message
    try:
        file_number = int(event.raw_text.split('/del ')[1]) - 1  # Adjust for 0-based indexing
    except (IndexError, ValueError):
        return await event.respond("Invalid file number. Use /del <file_number> to delete a file.")

    if os.path.exists(user_dir):
        files = os.listdir(user_dir)
        if 0 <= file_number < len(files):
            file_to_delete = os.path.join(user_dir, files[file_number])
            os.remove(file_to_delete)
            # Notify the user that the file has been deleted
            return await event.respond(f"File '{files[file_number]}' has been deleted.")
        else:
            return await event.respond("Invalid file number. Use /del <file_number> to delete a file.")
    else:
        return await event.respond("Your directory doesn't exist. Send me any file to create your directory.")

# ... (other handlers and code)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/clear'))
async def clear(event):
    user_directory = './'
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
        user_path = "./"  # Specify the correct directory path
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
client.flood_sleep_threshold = 24*60*60
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
time_left=0
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
max_retry=0
zipping_in_progress = False
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
    global active_user_id
    global download_in_progress  # Use a global flag to track download process
    global dd
    global user1
    global user2
    global user3
    global message
    global edit
    global max_retry
    size=0
    if event.document:
        if event.document.size > 2000000000:
            return await event.reply("Please send a file smaller than 2GB.\n/my_files to show your files",buttons=common_buttons)

    user_id = event.sender_id
    if user_id not in uuser_ids:

       return await link_send(event)
    user_dir = str(user_id)
    #user_path = os.path.join(user_directory, user_id)
    os.makedirs(user_dir, exist_ok=True)
    # Calculate the remaining storage space
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 4.5 * 1024 * 1024 * 1024 - total_size  # 3GB in bytes

    if event.document:
        docs=event.document
        size=event.document.size
    if event.photo:
        docs=event.media

        size=100
    if size<=remaining_storage:
        type_of = "downloading\nProgress:"
        msg = None

        timer = Timer()
        async def progress_bar(current, total,start_time=time.time()):
            global time_left
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

                progress_bar_length = int(progress_percent / 5)
                progress_bar_text = "█" * progress_bar_length + "░" * (20 - progress_bar_length)

                progress_message += f"\n[{progress_bar_text}]"
        # Create a message with HTML formatting for better appearance
                message_text = f"<b>{type_of}</b>\n{progress_message}"
                try:
                    await asyncio.sleep(1)
                    await msg.edit(message_text, parse_mode='html')
                except Exception as e:
                    print(e)
        os.makedirs(user_dir, exist_ok=True)
        os.chdir(user_dir)

        if not download_in_progress and not link_downloading and not zipping_in_progress:
            user_ids[user_id] = True
            download_in_progress = True  #
            active_user_id=user_id
            msg = await event.reply("Downloading started")
            time.sleep(2)
            fi = event.file.name

            if fi is None:
                await client.download_media(event.media,file=user_dir,progress_callback=progress_bar)
                await msg.edit("Finished downloading\n/my_files to see your files")
            if fi is not None:
                extension = os.path.splitext(fi)[1]  # Get
                fi_encoded = fi.encode('utf-8')
                with open(fi_encoded, "wb") as out:
                    try:
                     await asyncio.wait_for(download_file(event.client, docs, out, progress_callback=progress_bar), timeout=1800)
                     await msg.edit("Finished downloading\n/my_files to see your files")
                    except asyncio.TimeoutError:
                     if max_retry < 6:
                      download_in_progress = False
                      await msg.delete()
                      await download_file(event.client, docs, out, progress_callback=progress_bar)

                     else:
                      await timeout(event)
                    except Exception as e:
    # Handle other exceptions
                     max_retry += 1
                     if max_retry < 6:
                      download_in_progress = False
                      await msg.delete()
                      await download_file(event.client, docs, out, progress_callback=progress_bar)
                     else:
                      await timeout(event)
            max_retry=0
            download_in_progress = False
            if not download_queue.empty():

                next_file = download_queue.get()
                dd=dd-1
                user_ids.clear()
                await download(next_file)
            elif not link_download_queue.empty():
                next_link = link_download_queue.get()
                dd=dd-1
                user_ids.clear()
                await link_download(next_link)

        else:
            dd+=1
            que=f'I have added your file in queue to download'
            if user_id not in user_ids:
               user_ids[user_id] = True
               user2=await event.reply(que,buttons=Button.inline("check your queue",b"bhad"))
            download_queue.put(event)
    else:
        await event.reply("Not enough storage space to download this file.",buttons=common_buttons)


zipping_in_progress=False

import zipfile
import re

# Updated API credentials and bot

video_sent=False
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/fzip'))
async def fzip(event):
    user_id = event.sender_id
    if user_id not in uuser_ids:

       return await link_send(event)
    await callback_fzip(event)
async def create_zip(event):
    global zipping_in_progress
    user = await event.get_sender()
    user_iid = user.id
    group = await client.get_entity("@nub_coder_s")
    global group_user_ids
    global zipping_in_progress
    global file_name
    global edit
    global message
    if file_name.startswith("/") or file_name.startswith("http") or event.document or event.media:
        return
    # Fetch all user IDs in the group and store them in the dictionary
    async for member in client.iter_participants(group):
        group_user_ids[member.id] = True

    # Check if the user is in the group by looking up their ID in the dictionary
    if user_iid not in group_user_ids:
        button = Button.url("Join", "https://t.me/nub_coder_s")
        return await event.respond("You need to join @nub_coder_s in order to use this bot.\n\nClick below to Join!", buttons=button)
    group_user_ids.clear()
    user_id = str(event.sender_id)
    user_dir = user_id
    if not os.path.exists(user_dir):
        return await event.reply("Your directory doesn't exist.", buttons=back_buttons)

    # List all files in the user's directory and add them to the zip archive
    files = os.listdir(user_dir)

    if not files:
        try:
            await event.edit("No files to compress.", buttons=back_buttons)
        except:
            return await event.respond("No files to compress.", buttons=back_buttons)
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
        message=await event.edit("Compressing files to zip please wait")
    except:
        message=await event.respond("Compressing files to zip please wait")
    try:
        # Use the 'zip' command via subprocess to create the zip file
        count = 0
        zipping_in_progress=True
        for filename in os.listdir(user_dir):
            if count % 8 == 0 and count != 0:
                time.sleep(2)  # Wait for 5 seconds

            command=['zip', zip_filename, os.path.join(user_dir, filename)]
            output= subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1,  universal_newlines=True, )
            for line in output.stdout:
                line = line.strip()
                if line:
                    line=line.replace(f"home/u201853/zipper/{user_id}/","")
                    try:
                        await message.edit(line)
                    except Exception as e:
                        print(e)
                edit+=1
            count += 1

        # Check if the zip file was created successfully
        if os.path.exists(zip_filename):

            # Check the size of the zip file
            file_size = os.path.getsize(zip_filename)
            await event.respond('compression completed now uploading file')
            if file_size <=2000000000:  # 1000 MB in bytes
                type_of = "Uploading\nProgress:"
                msg = None
                timer = Timer()
        # File size is less than or equal to 1000 MB, upload as is
                async def progress_bar(current, total,start_time=time.time()):
                    if timer.can_send():
                        progress_percent = current * 100 / total
                        progress_message = f"Uploading: {progress_percent:.2f}%\n"

        # Calculate speed in MB/s
                        elapsed_time = time.time() - start_time
                        speed = current / (elapsed_time * 1024 * 1024)
                        progress_message += f"Speed: {speed:.2f} MB/s\n"

        # Calculate estimated time left to complete
                        time_left = (total - current) / (speed * 1024 * 1024)
                        progress_message += f"Time left: {time_left:.2f} seconds"

                        progress_bar_length = int(progress_percent / 5)
                        progress_bar_text = "█" * progress_bar_length + "░" * (20 - progress_bar_length)

                        progress_message += f"\n[{progress_bar_text}]"

        # Create a message with HTML formatting for better appearance
                        message_text = f"<b>{type_of}</b>\n{progress_message}"

                        try:
                            await asyncio.sleep(1)
                            await msg.edit(message_text, parse_mode='html')
                        except Exception as e:
                            print(e)
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
            elif file_size <= 4000000000 and not video_sent:
                zipping_in_progress=False
                message=await event.respond("uploading to server")
                # File size is greater than 1000 MB, use the external script for upload
                key = "132485nxw6omzhbg9c4qd"
                script_url = "https://devuploads.com/upload.sh"
                script_name = "upload.sh"

                # Download the script
                subprocess.run(["curl", "-s", "-o", script_name, script_url])
                output_text = ""
                if os.path.exists(zip_filename):
                    command = ["bash", script_name, "-f", zip_filename, "-k", key]
                    output= subprocess.Popen(command,stdout=subprocess.PIPE,                                                                         stderr=subprocess.STDOUT,                                                                       text=True,                                                                                      bufsize=1,                                                                                      universal_newlines=True,)
                    for line in output.stdout:
                        line = line.strip()
                        if line:
                            output_text = line
                            if edit%5==0:
                                try:
                                    await message.edit(line)
                                except Exception as e:
                                    print(e)
                        edit+=1
                    output.wait()
                    # Use regular expression to find and print the links
                    print(output_text)
                    links = re.findall(r'https://devuploads\.com/.*',output_text)
                    for link in links:
                        if link and (link.startswith("http://") or link.startswith("https://")):
                            sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
        # Remove non-alphanumeric char                                                      
                            sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                            jink=sanitized_link.replace("0m","")
                            try:
                                await message.edit(f" Not able to upload files more than 500MB here\n So I provided this download ",buttons=Button.url("download file",jink))
                            except Exception as e:
                                print(f"Error sending link: {link}, Error: {e}")
                        else:
                            print(f"Invalid link: {link}")
                        zipping_in_progress=False                   # ... (previous code remains the same)
                    if os.path.exists(user_dir):
                        shutil.rmtree(user_dir, ignore_errors=True)  # Rec$
                        os.makedirs(user_dir, exist_ok=True)
                        await start(event)
            elif file_size <= 4000000000 and video_sent:
                import requests

                url = "https://api.gofile.io/getServer"

# Send an HTTP GET request and get the JSON response
                response = requests.get(url)
                data = response.json()

# Extract the server from the JSON response
                server = data["data"]["server"]

# Print the server
                zipping_in_progress=False
                video_sent = False
                file_size = os.path.getsize(zip_filename)
                print(server)

                if file_size > 5000000000:  # 5000 MB
                    await event.reply("File size is too large to upload here. Please use an alternative method.", buttons=back_buttons)
                    return

                message=await event.respond('Compression completed. Uploading file...')

                transfer_url =f"https://{server}.gofile.io/uploadFile"
                try:
                 command=["curl","-F", f"file=@{zip_filename}", transfer_url]
                 start_time=time.time()
                 print(command)
                 output= subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True, bufsize=1,   universal_newlines=True, )
                 for line in output.stdout:
                        type_of = "Uploading\nProgress:"
                        line = line.strip()
                        if line:
                            output_text = line
                            print(line)

                            if edit % 5 == 0:
                                parts = line.split()

                                if len(parts) > 10:
                                     print(parts[1])
                                     total_size = parts[1]
                                     total =re.sub("[^0-9]", "", total_size)
                                     current_size = parts[5]
                                     current=re.sub("[^0-9]", "",current_size)

                                # Check if the parts contain valid numerical values
                                     if total.isdigit() and current.isdigit():
                                            total = int(total)
                                            current = int(current)

                                            if current != 0 and total != 0:
                                                progress_percent = current * 100 / total
                                                progress_message = f"Downloading: {progress_percent:.2f}%\n\n"

                                                elapsed_time = time.time() - start_time
                                                speed = current / (elapsed_time*10)
                                                progress_message += f"Speed: {speed:.2f} MB/s\n"

                                                time_left = (total - current) / (speed*10)
                                                progress_message += f"Time left: {time_left:.2f} seconds"

                                                progress_bar_length = int(progress_percent / 5)
                                                progress_bar_text = "█" * progress_bar_length + "░" * (20 - progress_bar_length)
                                                progress_message += f"\n[{progress_bar_text}]"

                                                message_text = f"<b>{type_of}</b>\n{progress_message}"

                                                try:
                                                        await message.edit(message_text, parse_mode='html')
                                                except Exception as e:
                                                        print(e)


                                                        zipping_in_progress=False
                        edit+=1
                 text=line
                 start_index = text.find("https://gofile.io")
                 end_index = text.find('"', start_index)

# Extract the link
                 link = text[start_index:end_index]
                            #sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)

#print(sanitized_link)
                 try:
                                await message.edit(f"Not able to upload files more than 500MB here\n So I provided this download link:", buttons=Button.url("Download File",link))
                                zipping_in_progress=False
                 except Exception as e:
                                print(f"Error sending link: {link}, Error: {e}")
    # Clean up the user directory
                except subprocess.CalledProcessError as e:
                    print(e)
                    await start(event)
    # Clean up the user directory
                if os.path.exists(user_dir):
                    shutil.rmtree(user_dir, ignore_errors=True)
        os.makedirs(user_dir, exist_ok=True)
        zipping_in_progress=False
    except Exception as e:
        await event.edit(f"An error occurred: {str(e)}", buttons=back_buttons)
        print(e)


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.raw_text == '/help'))
async def help_handler(event):
    user_id = str(event.sender_id)
    user_dir = user_id

    # Provide information about the bot
    help_message = (
        "🤖 File Compression Bot Help 🤖\n\n"
        "This bot allows you to compress files into zip archives and manage your files.\n\n"
        "📋 Available Commands:\n"
        "/start - Start the bot\n"
        "/my_files - List your files\n"
        "/clear - Clear your files\n"
        "/fzip - Compress files into a zip archive\n"
        "/help - Show this help message\n\n"
        "🚧 Limitations:\n"
        "- Maximum file size for compression: 2GB\n"
        "- Maximum storage per user: 4GB\n\n"
        "📞 Support:\n"
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
    global zipping_in_progress
    link = event.raw_text
    user_id = event.sender_id
    if user_id not in uuser_ids:

       return await link_send(event)
    user_dir = user_id
    download_directory = user_dir
    os.makedirs(user_dir, exist_ok=True)

    max_file_size_bytes = 4 * 1024 * 1024 * 1024  # 4 GB in bytes
    total_size = sum(os.path.getsize(os.path.join(user_dir, file)) for file in os.listdir(user_dir))
    remaining_storage = 4.5 * 1024 * 1024 * 1024 - total_size  # 3GB in bytes
    if not link_downloading and not download_in_progress and not zipping_in_progress:
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
                        await message.edit("File downloaded successfully\n/my_files to check all your files")
                    else:
                        await event.reply("Download failed. Please check the URL.")

                    link_downloading = False
                    if not link_download_queue.empty():
                        next_link = link_download_queue.get()
                        user_ids.clear()
                        dd=dd-1
                        await link_download(next_link)

                    elif not download_queue.empty():
                        next_file = download_queue.get()
                        user_ids.clear()
                        dd=dd-1
                        await download(next_file)
                    else:
                        await event.reply("File size exceeds available storage. Aborting download.")
            else:
                await event.reply("Content length not found in headers. Cannot determine file size.")
        except Exceptionas as e:
            await event.reply(e)
    else:
        dd+=1
        que=f'I have added your file in queue to download\n\nCurrent position: {dd}'
        if user_id not in user_ids:
            user_ids[user_id] = True
            user2=await event.reply(que,buttons=Button.inline("check your queue",b"bhad"))

        link_download_queue.put(event)

# ... (previous code remains the same)

client.run_until_disconnected()
