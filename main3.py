from telethon.sync import TelegramClient, events, Button
import re

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6501391531:AAGXvUFE1153Y_EtJp00Xz1uA3stbnS6LUo'

initial_sender_id = None  # Global variable to store initial sender ID

client = TelegramClient(None, api_id, api_hash).start(bot_token=bot_token)

async def get_full_name(username_or_id):
    try:
        entity = await client.get_entity(username_or_id)
        full_name = entity.first_name + " " + entity.last_name if entity.last_name else entity.first_name
        return full_name
    except Exception as e:
        return None

@client.on(events.InlineQuery)
async def handler(event):
    global initial_sender_id  # Use the global variable
    builder = event.builder
    results = []

    initial_sender_id = event.sender_id  # Store the initial sender ID

    user = await event.client.get_entity(initial_sender_id)  # Get the entity using the initial sender ID
    full_name = user.first_name + " " + user.last_name if user.last_name else user.first_name
    input_text = event.text.strip()

    input_text_parts = input_text.split()
    secret_message = f"whisper message from {full_name}"

    if input_text_parts:
        last_word = input_text_parts[-1]
        mentioned_full_name = None

        if re.match(r'^@\w+', last_word):  # Check for username starting with '@'
            mentioned_full_name = await get_full_name(last_word[1:])
        if re.match(r'^\d{9,12}$', last_word):  # Check for numeric user ID with 9-12 digits
            mentioned_full_name = last_word

        if mentioned_full_name:
            secret_message += f" to {mentioned_full_name}"

            results.append(builder.article(
                title=f"send whisper message to {mentioned_full_name}",
                description=f"💌💌Only {mentioned_full_name} can see this message",
                text=secret_message,
                buttons=[Button.inline("Show Secret", data=f"show_secret_{' '.join(input_text_parts)}")]
            ))
        else:
            results.append(
                builder.article(title='Write recipients username or userid',
                description=f'see the format\n@Fuck_u_in_whisper_bot whisper message eusername or userid of recipients',
                text=f'usage : @fuck_u_in_whisper your message to be sent in whisper username or userid',))
    else:
        results.append(
                builder.article(
                    title='Write recipients username or userid',
                    description=f'See the format\n@Fuck_u_in_whisper_bot whisper message username or userid of recipients',
                    text=f'Usage : @fuck_u_in_whisper your message to be sent in whisper username or userid',
                )
            )

    await event.answer(results)

@client.on(events.CallbackQuery)
async def callback_handler(event):
    print("Callback query received.")
    input_text = event.data.decode().split('_', 2)[2]
    user = await event.client.get_entity(event.sender_id)

    if str(user.username) in input_text or str(event.sender_id) in input_text or event.sender_id == initial_sender_id:

        input_text_parts = input_text.split()
        secret_message = f"Secret Message: {' '.join(input_text_parts[:-1])}"  # Remove the last word
    else:
        secret_message = "jyada idhr udhr ungli mat chala be"

    print("Initial sender ID:", initial_sender_id)  # Print the initial sender ID
    print("Sending answer:", secret_message.encode('utf-8', 'replace'))
    await event.answer(secret_message, alert=True)

print("Bot is running...")
#client.run(bot_token=bot_token)
client.run_until_disconnected()

