from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import re

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6579487121:AAFNL4QiIkkbChz9MrcRf4yP6iEkdNcTS9A'

# Create a Telethon client
client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)

# Dictionary to store saved notes
saved_notes = {}

@client.on(events.NewMessage(pattern='/save (.+)'))
async def save_note(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id
        note_text = reply_message.text
        title = event.pattern_match.group(1).strip()
        saved_notes[title] = note_text
        await event.reply(f"Note with title '{title}' saved!")

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text.lower()

    # Generate results based on saved notes' titles
    results = []
    for title, note_text in saved_notes.items():
        if query in title.lower():
            results.append(
                builder.article(
                    title=title,
                    description=note_text,
                    text=note_text,
                )
            )
    
    await event.answer(results)

# Start the client
client.run_until_disconnected()

