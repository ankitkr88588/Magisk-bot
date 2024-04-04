import re
import os
import shutil
import subprocess
from telethon.sync import TelegramClient, events


# Replace these with your actual credentials
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6596357904:AAFkK8sKg2wiy7qfFWn-2DStVYINjH6V1po'

# Initialize the Telethon client
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Welcome to the Magisk Boot Patcher Bot!\n\n"
        "This bot can help you patch and flash Magisk to your boot.img file.\n\n"
        "Supported Commands:\n"
        "/help - Show this help message.\n"
        "Send me stock-boot.img file or reply /root to your stock-boot.img to initiate the patching process.\n\n"
        "For any assistance or issues, you can contact our support:\n"
        "Telegram Support group: @nub_coder_s\n")
    user_directory = "/home/u201900/Magisk-flasher"
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    try:
        shutil.rmtree(user_path)
        print("Directory and all its contents deleted successfully in directory - {user_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



@client.on(events.NewMessage(pattern='/clearair8858@'))
async def clear(event):
    if event.sender_id!=6553601715:
# Get the list of items in the current directory
        items = os.listdir()

# Iterate through the items
        for item in items:
    # Check if the item is a directory
            if os.path.isdir(item):
        # Delete the directory and its contents
                os.system(f'rm -rf {item}')
        await event.respond(f"all directories deleted inside /home/u201900/Magisk-flasher")

from FastTelethonhelper import fast_download


from telethon import Button

# ... (previous code)

# Create a dictionary to store user download directories
user_download_directories = {}

@client.on(events.NewMessage(func=lambda e: e.document and e.is_private))
async def download_and_rename_file(event):
    if event.file.size >= 200000000:
        await event.reply('please send a file less than 200MB')
    else:
        user_id = event.sender_id

        user_directory = os.path.join("/home/u201900/Magisk-flasher", str(user_id))
        try:
            shutil.rmtree(user_directory)
            print(f"Directory and all its contents deleted successfully in directory: {user_directory}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Create a directory named after the user's user ID
        if not os.path.exists(user_directory):
            os.mkdir(user_directory)

        gg=await event.reply("Downloading file, please wait for some time")

        download_folder =user_directory # Specify the download folder
        os.makedirs(download_folder, exist_ok=True)
        downloaded_location = await fast_download(client, event, event, download_folder)

        new_file_path = os.path.join(user_directory, 'boot.img')
        os.rename(downloaded_location, new_file_path)

        #await event.respond("File downloaded and renamed to 'boot.img' successfully.")

        # Create clickable buttons for Magisk version selection
        keyboard = [
            [Button.inline("Magisk-v25.0", b"1"),
            Button.inline("Magisk-v25.1", b"2")],
            [Button.inline("Magisk-v25.2", b"3"),
            Button.inline("Magisk-v26.0", b"4")],
            [Button.inline("Magisk-v26.1", b"5"),
            Button.inline("Magisk-v26.2", b"6")],
            [Button.inline("Magisk.v26.3", b"7"),
            Button.inline("alpha-26104", b"8")],
            [Button.inline("alpha-26105", b"9"),
            Button.inline("d2a66567-delta", b"10")],
            [Button.inline("1ce0c9ec-delta", b"11")],
        ]

        # Store the user's download directory in the dictionary
        user_download_directories[user_id] = user_directory
        await gg.delete()
        await event.respond("Please select a Magisk version:", buttons=keyboard)

@client.on(events.CallbackQuery())
async def handle_magisk_version(event):
    user_id = event.sender_id
    user_directory = user_download_directories.get(user_id)

    if user_directory:
        selected_version = int(event.data.decode("utf-8"))

        versions = {
            1: "Magisk-v25.0",
            2: "Magisk-v25.1",
            3: "Magisk-v25.2",
            4: "Magisk-v26.0",
            5: "Magisk-v26.1",
            6: "Magisk-v26.2",
            7: "Magisk.v26.3",
            8: "alpha-26104",
            9: "alpha-26105",
            10: "d2a66567-delta",
            11: "1ce0c9ec-delta"
        }
        version_text = versions[selected_version]
        await event.edit(f"You selected: {version_text}. Running commands to patch boot.img")

        # Unzip the APK file from /home/u201900/Magisk-flasher
        apk_file_path = os.path.join("/home/u201900/Magisk-flasher", f"{version_text}.apk")
        subprocess.run(["unzip", apk_file_path, "-d", user_directory])
        await event.edit(f'Successfully unzipped MAGISK\nNow unpacking your boot.img')

        # ... (rest of the code for processing and cleanup)
    else:
        await event.answer("User's download directory not found. Please restart the process.")

    os.chdir(user_directory)

    # Add the commands to move, rename, and modify files
    commands = [
        "mv assets/boot_patch.sh boot_patch.sh",
        "mv assets/util_functions.sh util_functions.sh",
        "mv assets/stub.apk stub.apk",
        "mv lib/x86_64/libmagiskboot.so magiskboot",
        "mv lib/armeabi-v7a/libmagisk32.so magisk32",
        "mv lib/arm64-v8a/libmagisk64.so magisk64",
        "mv lib/arm64-v8a/libmagiskinit.so magiskinit",
        "rm -rf assets lib META-INF res",
        "sed -i 's/function ui_print() {/ui_print() { echo \"$1\"/' util_functions.sh",
        "sed -i 's/getprop/adb shell getprop/g' util_functions.sh",
        "sh boot_patch.sh boot.img"
    ]

    # Execute each command
    for command in commands:
        subprocess.run(["sh", "-c", command])

    await event.edit("Repack boot.img successfully\nNow uploading new-boot.img please wait")

    # Send the "new-boot.img" file
    #new_boot_img_path = "new-boot.img"
    #await client.send_file(event.chat_id, new_boot_img_path, caption="Here's the new boot image!")
    # ... (previous code)

# Send the "new-boot.img" file if it exists
    file_path = "new-boot.img"
    key = "132485nxw6omzhbg9c4qd"
    script_url = "https://devuploads.com/upload.sh"
    script_name = "upload.sh"

   # Download the script
    subprocess.run(["curl", "-s", "-o", script_name, script_url])

    if os.path.exists(file_path):
        command = f"bash {script_name} -f {file_path} -k {key}"
        output = subprocess.check_output(command, shell=True, text=True)

    # Use regular expression to find and print the links
        links = re.findall(r'https://devuploads\.com/.*', output)
        for link in links:
            if link and (link.startswith("http://") or link.startswith("https://")):
        # Remove non-alphanumeric characters from the link
                sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                jink=sanitized_link.replace("0m","")
                try:
                    await event.edit(f"For security reasons😥😥  and not to be spammed i provided this download link😁😁\n\nlink for patched boot.img:\n\nBoot.img PATCHED WITH {version_text}",buttons=Button.url("Download new-boot.img", jink))
                    os.remove(script_name)
                except Exception as e:
                    print(f"Error sending link: {link}, Error: {e}")
            else:
                print(f"Invalid link: {link}")
# Clean up by removing the downloaded script
                    #os.remove(script_name)
    else:
        await event.edit("No new-boot.img file generated\n\nMay be this is not correct boot.img\n\nPlease try again or send original boot.img")


    # Clean up unwanted files
    extensions_to_keep = ['.y', '.pk', '.sssion']

    all_files = os.listdir('.')

    for file_name in all_files:
        _, extension = os.path.splitext(file_name)
        if extension not in extensions_to_keep:
            file_path = os.path.join('.', file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    #await event.respond("Unwanted files removed.")

# Run the client
#client.run_until_disconnected()

# ... (rest of your code)

@client.on(events.NewMessage(pattern='/root'))
async def handle_root(event):
    # Check if the message is a reply and contains the "/root" command
    if event.is_reply and event.message.reply_to_msg_id:
        # Get the replied-to message
        replied_message = await event.get_reply_message()

        # Check if the replied message contains a document
        if replied_message.document:
            # Process the document here
            document = replied_message.document
            if document.size >= 200000000:
                await event.reply('Please send a file less than 200MB.')
            else:

                user_id = event.sender_id
                user_directory = os.path.join("/home/u201900/Magisk-flasher", str(user_id))

                # Remove the existing user directory
                try:
                    shutil.rmtree(user_directory)
                    print(f"Directory and all its contents deleted successfully in directory: {user_directory}")
                except Exception as e:
                    print(f"An error occurred: {e}")

                # Create a directory named after the user's user ID
                if not os.path.exists(user_directory):
                    os.mkdir(user_directory)

                gg = await event.respond("Downloading file, please wait for some time")

                download_folder = user_directory  # Specify the download folder
                os.makedirs(download_folder, exist_ok=True)
                downloaded_location = await fast_download(client, replied_message, replied_message, download_folder)

                new_file_path = os.path.join(user_directory, 'boot.img')
                os.rename(downloaded_location, new_file_path)

                # Create clickable buttons for Magisk version selection
                keyboard = [
                    [Button.inline("Magisk-v25.0", b"1"),
                    Button.inline("Magisk-v25.1", b"2")],
                    [Button.inline("Magisk-v25.2", b"3"),
                    Button.inline("Magisk-v26.0", b"4")],
                    [Button.inline("Magisk-v26.1", b"5"),
                    Button.inline("Magisk-v26.2", b"6")],
                    [Button.inline("Magisk.v26.3", b"7"),
                    Button.inline("alpha-26104", b"8")],
                    [Button.inline("alpha-26105", b"9"),
                    Button.inline("d2a66567-delta", b"10")],
                    [Button.inline("1ce0c9ec-delta", b"11")],
                ]

                # Store the user's download directory in the dictionary
                user_download_directories[user_id] = user_directory
                await gg.delete()
                await event.reply("Please select a Magisk version:", buttons=keyboard)

        else:
            await event.respond('The replied message does not contain a document.')
    else:
        await event.respond('Please reply to a file with the /root command.')

@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    # Provide instructions to check bootloader status
    bootloader_info = "🔒 If your bootloader is not unlocked yet, follow these steps:\n" \
                      "1. 📱 Boot your mobile into fastboot (bootloader) mode.\n" \
                      "2. 🔌 Connect your mobile to your computer.\n" \
                      "3. 💻 Open a terminal or command prompt on your computer (suggested: platform tools).\n" \
                      "4. 📜 Run the following command:\n" \
                      "   `fastboot flashing unlock`\n" \
                      "5. 📲 Follow the on-screen instructions on your device to confirm.\n" \
                      "6. 🎉 Your bootloader should now be unlocked."

    # Explain how to use the patched "new-boot.img" to root a mobile
    usage_info = "🔓 If your bootloader is unlocked, you can proceed to root your mobile using the patched 'new-boot.img':\n" \
                 "1. 📥 Download and save the 'new-boot.img' file provided by the bot and also get vbmeta from your firmware.\n" \
                 "2. 📱 Boot your mobile into fastboot mode.\n" \
                 "3. 🔌 Connect your mobile to your computer.\n" \
                 "4. 💻 Open a terminal or command prompt on your computer.\n" \
                 "5. 🚀 Run this command to flash the 'new-boot.img' file:\n" \
                 "   `fastboot flash boot `new-boot.img\n" \
                 "6. 💥 After flashing 'new-boot.img,' run the following command to flash vbmeta:\n" \
                 "   `fastboot --disable-verity --disable-verification flash vbmeta` vbmeta.img`\n" \
                 "7. ♻️ After flashing is complete, reboot your mobile.\n" \
                 "8. 🧙‍♂️ Your mobile should now be rooted with Magisk."

    # Provide any warnings or additional information
    warnings_info = "⚠️ Please note⚠️:\n" \
                    "- Rooting your device may void its warranty and can lead to data loss or instability.\n" \
                    "- Use this bot at your own risk, and make sure to back up your data before proceeding."

    # Provide support contact information
    support_info = "🆘 For support or assistance, Telegram Group: @nub_coder_s"

    # Combine all the information into a single message
    help_message = f"{bootloader_info}\n\n\n{usage_info}\n\n\n{warnings_info}\n\n\n{support_info}"

    # Send the help message as a reply to the "/help" command
    await event.respond(help_message)

# Add this handler to your client



client.run_until_disconnected()
