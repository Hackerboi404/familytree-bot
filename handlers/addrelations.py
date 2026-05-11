from pyrogram import Client, filters, MessageHandler
from database.db import add_relation
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
    """Creates the callback function for a specific command."""
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
    """Registers all dynamic handlers to the app with a specific group."""
    for cmd, key in COMMAND_MAP.items():
        # 1. Get the logic function
        handler_func = create_add_handler(cmd)
        
        # 2. Create the Filter object
        command_filter = filters.command(cmd)
        
        # 3. Wrap in MessageHandler with group=1
        # This fixes the "got multiple values for argument 'group'" error
        message_handler = MessageHandler(handler_func, command_filter, group=1)
        
        # 4. Register the Handler object to the app
        app.add_handler(message_handler)
