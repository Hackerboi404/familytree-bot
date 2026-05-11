from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Start command
async def start_cmd(client, message):

    welcome_text = """
🌳 **Welcome to FamilyTree Bot** 👑

Build your own Telegram Family Empire ❤️

━━━━━━━━━━━━━━━

👨 Dad
👩 Mom
💍 Wife
❤️ Girlfriend
🧑 Brothers
👧 Sisters
🤝 Friends
😈 Enemies

━━━━━━━━━━━━━━━

Reply to any user using commands like:

`/adddad`
`/addmom`
`/addwife`
`/addfriend`

Then use:

`/familytree`

to view your complete relationship tree 🌳
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🌳 Open Family Tree",
                    callback_data="show_tree"
                ),

                InlineKeyboardButton(
                    "📖 Help",
                    callback_data="help_cmd"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close_msg"
                )
            ]
        ]
    )

    await message.reply_text(
        welcome_text,
        reply_markup=keyboard
    )


# Close button
async def close_msg(client, callback_query):

    await callback_query.message.delete()


# Register handlers
def register_handlers(app):

    app.add_handler(
        MessageHandler(
            start_cmd,
            filters.command("start")
        ),
        group=0
    )

    app.add_handler(
        CallbackQueryHandler(
            close_msg,
            filters.regex("^close_msg$")
        ),
        group=0
    )
