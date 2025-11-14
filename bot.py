import os
import uuid
import sqlite3
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = "8257100937:AAE1-LBPKy1holr9xVpcAA0gB6LHQqwgO4U"

# Database setup
def init_db():
    conn = sqlite3.connect('images.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            session_id TEXT PRIMARY KEY,
            image_data BLOB
        )
    ''')
    conn.commit()
    conn.close()

init_db()
user_sessions = {}

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🤖 Image Sharing Bot\n\nSend /getlink then share an image!"
    await update.message.reply_text(text)

async def getlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session_id = str(uuid.uuid4())[:8]
    user_sessions[user_id] = session_id
    await update.message.reply_text(f"Session: {session_id}\nNow send image!")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("Use /getlink first!")
        return
    
    session_id = user_sessions[user_id]
    try:
        photo_file = await update.message.photo[-1].get_file()
        image_data = await photo_file.download_as_bytearray()
        
        conn = sqlite3.connect('images.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO images (session_id, image_data) VALUES (?, ?)',
                      (session_id, bytes(image_data)))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ Image saved!\nSession: {session_id}")
        del user_sessions[user_id]
    except Exception as e:
        await update.message.reply_text("Error!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /getlink then image")

def main():
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getlink", getlink))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
