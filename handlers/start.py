from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start(client, message):
    welcome_text = """
🌳 **Welcome to FamilyTree Bot** 👑

Build your own Telegram Family Empire ❤️

**Reply to any user using commands like:**
`/adddad` | `/addmom` | `/addwife`
`/addbro` | `/addsis` | `/addfriend`

Then use `/familytree` to view your complete relationship tree.
    """
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌳 Open Family Tree", callback_data="show_tree"),
            InlineKeyboardButton("📖 Help", callback_data="help_cmd")
        ],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^close_msg$"))
async def close_msg(client, callback_query):
    await callback_query.message.delete()
