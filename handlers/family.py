from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db import get_family_tree


# Build tree text
def build_family_text(data):

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

            first_name = data[key]["first_name"]
            target_id = data[key]["target_id"]

            # Proper clickable mention
            mention = f"[{first_name}](tg://user?id={target_id})"

            text += f"{title}\n"
            text += f"└── {mention}\n\n"

    text += "━━━━━━━━━━━━━━━\n👑 FamilyTree Bot"

    return text


# /familytree command
async def family_tree(client, message):

    user_id = message.from_user.id

    data = get_family_tree(user_id)

    if not data:

        await message.reply_text(
            "🌳 Your family tree is empty.\n\n"
            "Reply to users with commands like:\n"
            "`/adddad`, `/addmom`, `/addwife`"
        )
        return

    text = build_family_text(data)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data=f"refresh_{user_id}"
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
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# Refresh button
async def refresh_tree(client, callback_query):

    user_id = callback_query.from_user.id

    data = get_family_tree(user_id)

    if not data:

        await callback_query.answer(
            "Tree is empty.",
            show_alert=True
        )
        return

    text = build_family_text(data)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data=f"refresh_{user_id}"
                ),

                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close_tree"
                )
            ]
        ]
    )

    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    await callback_query.answer("✅ Refreshed")


# Close button
async def close_tree(client, callback_query):

    await callback_query.message.delete()


# Register handlers
def register_handlers(app):

    # /familytree command
    app.add_handler(
        MessageHandler(
            family_tree,
            filters.command("familytree")
        ),
        group=0
    )

    # Refresh callback
    app.add_handler(
        CallbackQueryHandler(
            refresh_tree,
            filters.regex("^refresh_")
        ),
        group=0
    )

    # Close callback
    app.add_handler(
        CallbackQueryHandler(
            close_tree,
            filters.regex("^close_tree$")
        ),
        group=0
    )
