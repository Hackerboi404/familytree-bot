import asyncio
from pyrogram import Client, filters
from database.db import get_family_tree
from utils.helpers import format_tree_text
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("familytree"))
async def show_tree_cmd(client, message):
    user_id = message.from_user.id
    loading_msg = await message.reply("🔄 Fetching your roots...")
    await asyncio.sleep(0.5)
    await loading_msg.delete()
    
    family_data = get_family_tree(user_id)
    tree_text = format_tree_text(family_data)
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="show_tree"),
            InlineKeyboardButton("❌ Close", callback_data="close_msg")
        ]
    ])
    
    await message.reply_text(tree_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^show_tree$"))
async def show_tree_cb(client, callback_query):
    user_id = callback_query.from_user.id
    family_data = get_family_tree(user_id)
    tree_text = format_tree_text(family_data)
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="show_tree"),
            InlineKeyboardButton("❌ Close", callback_data="close_msg")
        ]
    ])
    
    try:
        await callback_query.edit_message_text(tree_text, reply_markup=keyboard)
    except Exception:
        pass
