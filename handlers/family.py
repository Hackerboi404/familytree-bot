from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db import get_family_tree


# Family tree command
async def family_tree(client, message):

    user_id = message.from_user.id

    # Get family data
    data = get_family_tree(user_id)

    if not data:
        await message.reply_text(
            "🌳 Your family tree is empty.\n\n"
            "Reply to users with commands like:\n"
            "`/adddad`, `/addmom`, `/addwife`"
        )
        return

    # Build text
    text = "╔═══ 🌳 YOUR FAMILY TREE 🌳 ═══╗\n\n"

    relations = {
        "dad": "👨 Dad",
        "mom": "👩 Mom",
        "grandfather": "👴 Grandfather",
        "grandmother": "👵 Grandmother",
        "uncle": "🧔 Uncle",
        "aunty": "👩 Aunty",
        "bro": "🧑 Brother",
        "sis": "👧 Sister",
        "wife": "💍 Wife",
        "gf": "❤️ Girlfriend",
        "crush": "😍 Crush",
        "friend": "🤝 Friend",
        "enemy": "😈 Enemy",
        "son": "👦 Son",
        "daughter": "👧 Daughter",
        "motherinlaw": "👵 Mother In Law",
        "fatherinlaw": "👴 Father In Law",
        "saali": "🙈 Saali",
        "ziza": "😎 Ziza"
    }

    for key, title in relations.items():

        if key in data:

            username = data[key]["username"]

            text += f"{title}\n"
            text += f"└── @{username}\n\n"

    text += "━━━━━━━━━━━━━━━\n👑 FamilyTree Bot"

    # Buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="refresh_tree"
                ),

                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close_tree"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=keyboard
    )


# Close callback
async def close_tree(client, callback_query):

    await callback_query.message.delete()


# Register handlers
def register_handlers(app):

    app.add_handler(
        MessageHandler(
            family_tree,
            filters.command("familytree")
        ),
        group=0
    )
