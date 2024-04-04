from telethon.sync import TelegramClient, events
import subprocess
# Your API credentials
api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'

# Your session name (can be any string)
session_name = 'my_userbot'

# Initialize the TelegramClient
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(outgoing=True))
async def handle_messages(event):
    print(event.message.text)
    # Check if the message is a reply to a file and contains the "/ddit" command
    if event.is_reply and event.message.reply_to_msg_id and event.message.text in ["/sendc" , "/up","/clear"]:
        # Get the replied-to message
        replied_message = await event.get_reply_message()

        # Check if the replied-to message contains a file
        if replied_message.media:
            # Download the file
           hfile= await client.download_media(replied_message, file="/home/u201900/timer/tempo")

           await event.delete()
           if event.message.text=="/sendc":
               await client.send_file(event.chat_id, file=hfile)
           elif event.message.text=="/clear":
               subprocess.run(["python", "clear.py"])

           else:
               await client.send_file("me", file=hfile)
               await client.send_file("me", file='file.zip')
# Start the client
with client:
    # Run the client loop
    client.run_until_disconnected()
