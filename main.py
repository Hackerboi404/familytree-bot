import asyncio
from pyrogram import Client, idle
from config import Config
from database.db import init_db
from handlers import start, family, addrelations
from live import keep_alive

# Initialize the app
app = Client("familytreebot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

print("🌳 Starting FamilyTree Bot...")

# Start Flask Server for Keep-Alive
keep_alive()

# Initialize Database
init_db()

# Register Handlers
addrelations.register_handlers(app)

# Start Bot
print("Bot is running in Polling Mode...")
app.run()
idle()
