from threading import Thread
from pyrogram import Client

from config import Config
from database.db import init_db
from handlers import start, family, addrelations
from live import keep_alive


print("🌳 Starting FamilyTree Bot...")


# Start Flask keep alive server
Thread(target=keep_alive).start()


# Initialize database
init_db()


# Create bot client
app = Client(
    "familytreebot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


# Register handlers
start.register_handlers(app)
family.register_handlers(app)
addrelations.register_handlers(app)


print("✅ Bot is running in Polling Mode...")


# Run bot
app.run()
