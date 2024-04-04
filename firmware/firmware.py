from telethon.sync import TelegramClient, events, Button
import os
from telethon.tl.types import MessageEntityUrl


api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'

bot_token = '6480106506:AAHn3_n5snw85MH_lpOQSM55RPalSZ0uuTQ'
#bot_token='6834882551:AAFJ_IBfUhXbkye4RslYCkWz0OJx1zEhrho'
firmware_directory = '.'

# Create a Telethon client
client = TelegramClient(None, api_id, api_hash).start(bot_token=bot_token)
admins_file_path = 'admin/admin.txt'

# Load admin user IDs from the file
with open(admins_file_path, 'r') as admins_file:
    admin_user_ids = admins_file.read().splitlines()

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    global add_link
    global add_file

    user = await event.get_chat()
#    await event.reply(f"Hello, {user.first_name}! I'm your bot. Here are some .txt files in the current directory:")

    # Get a list of .txt files in the current directory
    txt_files = sorted([os.path.splitext(file)[0] for file in os.listdir() if file.endswith('.txt')])

    if txt_files:
        # Create inline buttons for each .txt file, arranging them in pairs
        buttons = []
        for i in range(0, len(txt_files), 3):
            row_buttons = []
            for j in range(3):
                index = i + j
                if index < len(txt_files):
                    row_buttons.append(Button.inline(txt_files[index], data=txt_files[index]))
            buttons.append(row_buttons)
        buttons.append([Button.inline("❌", data="delete_message")])
        await event.respond(f"👋 Hello! I'm your firmware Provider bot. Here are some things you can do: \n\n\n\n"
                        "📱 Select your device to get firmware and custom ROMs.\n\nTo request firmware:@nub_coder_s"
                        "❓ Use /help to learn more about how to use this bot.", buttons=buttons)
    else:
        await event.reply("No .txt files found in the current directory.")

@client.on(events.CallbackQuery)
async def callback(event):
    selected_file = event.data.decode('utf-8')
    print(selected_file)
    if selected_file == 'back':
        await event.delete()
        # User clicked the back button, go back to start event
        await start(event)
        return
    if selected_file =="delete_message":
       await event.delete()
       return

    # Read the selected file and extract URLs with the format "V971: www.example.com"
    if 2==2:
        with open(selected_file + '.txt', 'r') as file:
            url_buttons = []
            urls = []
            for line in file:
                parts = line.strip().split(': ')
                if len(parts) == 2 and parts[1].startswith('http'):
                    urls.append((parts[0], parts[1]))

            # Create inline URL buttons, arranging them in pairs
            for i in range(0, len(urls), 2):
                row_buttons = []
                for j in range(2):
                    index = i + j
                    if index < len(urls):
                        row_buttons.append(Button.url(urls[index][0], urls[index][1]))
                url_buttons.append(row_buttons)

        # Add a back button to return to the start event
        url_buttons.append([Button.inline("Back", data="back")],)

        if url_buttons:
            #await event.edit(f"#CUSTOM-ROM1:\n\n***XOS 10 ReWorked***\n\n\n\nBy SOUROV KHAN N∆HID\n\nFlashing Guide :[Click Here](https://t.ly/23YsM)  \n\nReview : [Click Here](https://t.ly/rR7HS) \n\n\n\nChangelog :\n\n⚙️ Based on The latest Designed XOS\n\n⚙️ Boot Animation from Kali\n\n⚙️ Spoofing\n\n⚙️ Added Patches and Updates from Android 11,12 and 12L\n\n⚙️ All Bloatwares Removed\n\n⚙️ Added Voice Changer\n\n⚙️ Only Play Store and Pay Service PreLoaded\n\n⚙️ Stock Infinix Camera as default\n\n\n\nJoin :\n\nFollow @SourovKhanNahidYT (for Updates)\n\nReport Bugs on @SourovKhanNahid2\n\n\n\n\n\n#CUSTOM-ROM-2:\n\ndotOS | v5.2.1  | PORT | Android11By: Eko Rudianto\n\n\n\n🔹Port By: you n me\n\n🔹 How to Install: [click here](https://t.me/Infinix_Note11s/31552)\n\nNotes:\n\n• Boot will take upto 5-6 minutes\n\nBugs :\n\nScreenLock\n\nOTG (fix by magisk module)\n\nCheck other n fix together\n\n\n\nCredit:\n\n@InfinixHot10S@InfinixHot10\#dotOS\n\n#NOTE11s\n\n",buttons=url_buttons,link_preview=False)
        #else:
            await event.edit(f"Here are the some available firmware for your {selected_file}:\n\n⚠️Don't flash or use firmware from other devices, otherwise your phone might get bricked.\n\nPlease join:@nub_coder_s\nSome file are short linked so don't creare trouble",link_preview=False, buttons=url_buttons)

    else:
        await event.answer("Selected file not found.")

# Your existing code...

@client.on(events.NewMessage(pattern='/del'))
async def delete_file(event):
    if str(event.sender_id) not in admin_user_ids:
        return

    try:
        # Get the filename from the command
        command = event.message.text.split(' ')
        if len(command) >= 2:
            file_identifier = command[1]

            # Check if the identifier starts with 'V'
            if file_identifier.startswith('V'):
                # Iterate through all .txt files
                for filename in os.listdir():
                    if filename.endswith('.txt'):
                        file_path = os.path.join(os.getcwd(), filename)
                        # Read the file and check for lines starting with the identifier
                        with open(file_path, 'r') as file:
                            lines = file.readlines()
                        with open(file_path, 'w') as file:
                            for line in lines:
                                if not line.startswith(file_identifier):
                                    file.write(line)

                await event.reply(f"All lines starting with '{file_identifier}' have been deleted from the files.")
            else:
                file_path = f"{file_identifier}.txt"

                # Check if the file exists
                if os.path.exists(file_path):
                    # Delete the file
                    os.remove(file_path)
                    await event.reply(f"File '{file_identifier}' has been deleted.")
                else:
                    await event.reply(f"File '{file_identifier}' not found.")
        else:
            await event.reply("Please provide the filename in the format: /del {filename}")
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")





@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    help_message = """
    **Welcome to the Infinix Firmware Bot!**

This bot is designed to provide firmware and custom ROMs for various Infinix devices.

**How to Use:**
1. Start by using the /start command.
2. You will see a list of available device or model.
3. Select a device by clicking on its name WARNING: use your ow device firmware or custom rom.
4. The bot will then provide you with download links or information related to that device.

**Contact the Developer:**
If you have any questions, suggestions, or to request firmware, feel free to contact the developer:
- Bot managed by: @nub_coder_s

Thank you for using the Infinix Firmware Bot!
    """
    await event.reply(help_message, parse_mode='markdown')

@client.on(events.NewMessage(incoming=True))
async def handle_links(event):
    if str(event.sender_id) not in admin_user_ids:
        return
    if event.message.text:
        # Check if any of the allowed URLs are present in the message text
        allowed_urls = [
            "https://link-center.net/756279",
            "https://link-target.net/756279",
            "https://direct-link.net/756279",
            "https://link-hub.net/756279"
        ]
        for allowed_url in allowed_urls:
            if allowed_url in event.message.text:
                ulink = event.message.text.replace(allowed_url, "")
                model_version = ulink.split("/")[-1].split("-")
                if len(model_version) >= 2:
                    model = model_version[-2].upper()
                    version = model_version[-1].upper()
                    file_name = f"{model}.txt"
                    if os.path.exists(file_name):
                        with open(file_name, 'r') as file:
                            if version in file.read():
                                await event.reply("File already present.")
                            else:
                                with open(file_name, 'a') as file:
                                    file.write(f"{version} : {event.message.text}\n")
                                await event.reply(f"New device file created for {model} with version {version}.")
                    else:
                        with open(file_name, 'w') as file:
                            file.write(f"{version} : {event.message.text}\n")
                        await event.reply(f"New device file created for {model} with version {version}.")

                    # Send the model file to the user
                    await event.respond(file=file_name, message=f"Here is the firmware file for {model}.")

                else:
                    await event.reply("Invalid link format.")
                return


@client.on(events.NewMessage(pattern='/majdur'))
async def add_admin(event):
    # Check if the sender is an admin
    if str(event.sender_id) in admin_user_ids:
        try:
            # Get the user ID from the command
            command = event.message.text.split(' ')
            if len(command) >= 2:
                user_id = command[1]

                # Append the user ID to admin.txt
                with open(admins_file_path, 'a') as admins_file:
                    admins_file.write(f"{user_id}\n")
                
                await event.reply(f"User ID {user_id} has been added to the admin list.")
            else:
                await event.reply("Please provide the user ID in the format: /majdur {user_id}")
        except Exception as e:
            await event.reply(f"An error occurred: {str(e)}")
    else:
        await event.reply("You are not authorized to use this command.")

client.run_until_disconnected()
