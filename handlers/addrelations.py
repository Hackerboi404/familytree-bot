import asyncio
from pyrogram import Client, filters
from database.db import add_relation
from utils.decorators import is_reply
from utils.cooldown import check_cooldown

# Map commands to DB keys
COMMAND_MAP = {
    "adddad": "dad",
    "addmom": "mom",
    "addgrandfather": "grandfather",
    "addgrandmother": "grandmother",
    "adduncle": "uncle",
    "addaunty": "aunty",
    "addbro": "bro",
    "addsis": "sis",
    "addwife": "wife",
    "addgf": "gf",
    "addcrush": "crush",
    "addson": "son",
    "adddaughter": "daughter",
    "addmotherinlaw": "motherinlaw",
    "addfatherinlaw": "fatherinlaw",
    "addsaali": "saali",
    "addziza": "ziza",
    "addfriend": "friend",
    "addenemy": "enemy",
}

def create_add_handler(command):
    async def handler(client, message):
        user_id = message.from_user.id
        
        # Cooldown check (2 seconds)
        if not check_cooldown(user_id):
            return

        # Ensure we are replying to a user
        if not message.reply_to_message:
            await message.reply("⚠️ Please reply to a user's message to use this command.")
            return

        replied_user = message.reply_to_message.from_user
        
        # Prevent adding bots or deleted accounts
        if replied_user.is_bot or replied_user.is_deleted:
            await message.reply("⚠️ You cannot add bots or deleted accounts.")
            return

        target_id = replied_user.id
        first_name = replied_user.first_name or "Unknown"
        username = replied_user.username or ""
        
        relation_key = COMMAND_MAP[command]
        
        # Save to DB
        add_relation(user_id, relation_key, target_id, first_name, username)
        
        # Feedback
        await message.reply(f"✅ Successfully saved as **{relation_key.replace('_', ' ').title()}**!", quote=True)
        
    return handler

def register_handlers(app):
    for cmd, key in COMMAND_MAP.items():
        # Create the handler logic
        handler_func = create_add_handler(cmd)
        
        # Register with specific group=1 to avoid sorting errors
        app.add_handler(handler_func, filters.command(cmd), group=1)
