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
        
        # Cooldown check
        if not check_cooldown(user_id):
            return

        # Get replied user
        replied_user = message.reply_to_message.from_user
        
        target_id = replied_user.id
        first_name = replied_user.first_name or "Unknown"
        username = replied_user.username or ""
        
        relation_key = COMMAND_MAP[command]
        
        # Save to DB
        add_relation(user_id, relation_key, target_id, first_name, username)
        
        # Feedback
        await message.reply(f"✅ Successfully saved as **{relation_key.replace('_', ' ').title()}**!", quote=True)
        
    return handler

# Register all handlers dynamically
def register_handlers(app):
    for cmd, key in COMMAND_MAP.items():
        # Apply the is_reply decorator manually by wrapping the function
        # Or simply check inside handler. Here we check inside handler logic via the wrapper
        # To use our decorator cleanly:
        
        raw_handler = create_add_handler(cmd)
        
        # We need to wrap it with is_reply
        # Since decorators return functions, we assign the wrapped function
        wrapped_handler = is_reply(raw_handler)
        
        app.add_handler(wrapped_handler, filters.command(cmd))
