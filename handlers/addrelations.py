from pyrogram import filters
from pyrogram.handlers import MessageHandler

from database.db import add_relation
from utils.cooldown import check_cooldown


# Relationship command mapping
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

        # Ignore invalid users
        if not message.from_user:
            return

        user_id = message.from_user.id

        # Cooldown check
        if not check_cooldown(user_id):
            await message.reply_text(
                "⏳ Please wait before using another command."
            )
            return

        # Must reply to user
        if not message.reply_to_message:
            await message.reply_text(
                "⚠️ Reply to someone's message first."
            )
            return

        replied_user = message.reply_to_message.from_user

        # Invalid user
        if not replied_user:
            await message.reply_text(
                "⚠️ Invalid user."
            )
            return

        # Prevent bots
        if replied_user.is_bot:
            await message.reply_text(
                "🤖 Bots cannot be added."
            )
            return

        # Prevent self add
        if replied_user.id == user_id:
            await message.reply_text(
                "😂 You can't add yourself."
            )
            return

        # User data
        target_id = replied_user.id
        first_name = replied_user.first_name or "Unknown"
        username = replied_user.username or "NoUsername"

        relation_key = COMMAND_MAP[command]

        # Save relation
        add_relation(
            user_id=user_id,
            relation=relation_key,
            target_id=target_id,
            first_name=first_name,
            username=username
        )

        # Success message
        await message.reply_text(
            f"✅ Successfully added "
            f"**{first_name}** as your "
            f"**{relation_key.replace('_', ' ').title()}** ❤️",
            quote=True
        )

    return handler


def register_handlers(app):

    for cmd in COMMAND_MAP.keys():

        # Create function
        handler_func = create_add_handler(cmd)

        # Proper command filter
        command_filter = filters.command(
            cmd,
            prefixes=["/"]
        )

        # Create MessageHandler
        message_handler = MessageHandler(
            handler_func,
            command_filter
        )

        # Register handler
        app.add_handler(
            message_handler,
            group=1
        )
