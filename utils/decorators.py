from pyrogram import Client, filters
from pyrogram.types import Message

def is_reply(func):
    """Decorator to check if command is a reply."""
    async def wrapper(client: Client, message: Message):
        if not message.reply_to_message:
            await message.reply("⚠️ Please reply to a user's message to use this command.")
            return
        await func(client, message)
    return wrapper
