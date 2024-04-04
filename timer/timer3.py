import time
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from telethon.tl.types import ChatAdminRights
# Your API credentials
api_id = 22877673
api_hash = 'fd368cc0762560833a22445063ce2c96'

# Your session name (can be any string)
session_name = 'timer3'

# Initialize the TelegramClient
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(outgoing=True))
async def handle_messages(event):
    #print(event.message.text)
    # Check if the message is a reply to a file and contains the "/ddit" command
    if event.is_reply and event.message.reply_to_msg_id and event.message.text in ["/sendc" , "/save","/clear"]:
        # Get the replied-to message
        replied_message = await event.get_reply_message()

        # Check if the replied-to message contains a file
        if replied_message.media:
            # Download the file
           hfile= await client.download_media(replied_message, file="/home/u201853/timer/tempo")

           await event.delete()
           if event.message.text=="/sendc":
               await client.send_file(event.chat_id, file=hfile)
           elif event.message.text=="/clear":
               subprocess.run(["python", "clear.py"])

           else:
               await client.send_file("me", file=hfile)

#@client.on(events.NewMessage(pattern='kid|Kid|@CTRL_PLUS_Z'))
#async def handle_messagesh(event):
 #   await event.reply('bhundi si skl ki\nSucchi')
async def get_call(event):
    geez = await event.client(getchat(event.chat_id))
    vcky = await event.client(getvc(geez.full_chat.call,limit=100))
    return vcky.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@client.on(events.NewMessage(outgoing=True, pattern="!vc1"))
async def start_voice_chat(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await event.edit(NO_ADMIN)
    try:
        await event.client(startvc(event.chat_id))
        await event.edit("Video chat started")
    except Exception as ex:
        await event.edit(f"`{str(ex)}`")


@client.on(events.NewMessage(outgoing=True, pattern="!vc0"))
async def stop_voice_chat(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await event.edit(NO_ADMIN)
    await event.client(stopvc(await get_call(event)))


    await event.edit("Video chat ended")

@client.on(events.NewMessage(outgoing=True, pattern="!vcin"))
async def invite_to_voice_chat(event):
    await event.edit("inviting all members")
    users = []
    z = 0
    async for x in event.client.iter_participants(event.chat_id):
        if not x.bot and not x.deleted:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:

            await event.client(invitetovc(call=await get_call(event), users=p))
            z += 6
    await event.edit(f"`Invited {z} users`")


CMD_HELP = {
    "calls": "�^}^x��^}^y��^}^y��^}^y��^}^y^v�^}^y��^}^y^y: `.startvc`\n"
    "�^f� : Start Group Call in a group.\n\n"
    "�^}^x��^}^y��^}^y��^}^y��^}^y^v�^}^y��^}^y^y: `.stopvc`\n"
    "�^f� : Stop Group Call in a group.\n\n"
    "�^}^x��^}^y��^}^y��^}^y��^}^y^v�^}^y��^}^y^y: `.vcinvite`\n"
    "�^f� : Invite all members of the group to a Group Call. (You must be joined)."
}
# Start the client
with client:
    # Run the client loop
    client.run_until_disconnected()
