import os
import uuid
import sqlite3
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Your bot token - directly in code
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
    text = """
📸 **Image Sharing Bot**

Welcome! Here's how it works:

1. Send /getlink to create a sharing session
2. Send me any image
3. Get a public link to share
4. Anyone can view the image with the link

Ready? Send /getlink to start!
"""
    await update.message.reply_text(text)

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session_id = str(uuid.uuid4())[:8]
    user_sessions[user_id] = session_id
    
    # For now, we'll just return the session ID
    # Once deployed, we'll update this with the real URL
    message = f"""
🆕 **Sharing Session Created!**

🔑 Session ID: `{session_id}`
🔗 Public URL: Will be available after deployment

📤 Now send me an image!
"""
    await update.message.reply_text(message)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await update.message.reply_text("❌ Please use /getlink first to create a session!")
        return
    
    session_id = user_sessions[user_id]
    
    try:
        # Get the photo
        photo_file = await update.message.photo[-1].get_file()
        image_data = await photo_file.download_as_bytearray()
        
        # Save to database
        conn = sqlite3.connect('images.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM images WHERE session_id = ?', (session_id,))
        cursor.execute('INSERT INTO images (session_id, image_data) VALUES (?, ?)',
                      (session_id, bytes(image_data)))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ **Image Saved!**\n\nSession ID: `{session_id}`\n\nWe'll add the web URL after deployment!")
        
        # Clear session
        del user_sessions[user_id]
        
    except Exception as e:
        await update.message.reply_text("❌ Error processing image. Please try again.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Send /getlink to create a sharing session, then send me an image!")

def main():
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getlink", get_link))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start POLLING (no webhook needed!)
    print("🤖 Bot starting with POLLING...")
    application.run_polling()

if __name__ == "__main__":
    main()