# 📸 Telegram Image Sharing Bot

A simple Telegram bot that allows users to share images via unique public links with session IDs.

## 🚀 Features

- ✅ Generate unique session IDs for image sharing
- ✅ Store images temporarily in database
- ✅ Public access via unique URLs
- ✅ Simple and easy to use
- ✅ Free hosting on Render.com

## 🤖 How to Use

1. **Start the bot**: Send `/start` to [@YourBotUsername](https://t.me/YourBotUsername)
2. **Create session**: Send `/getlink` to generate a unique sharing session
3. **Share image**: Send any image to the bot
4. **Get link**: Receive a public link to share with anyone
5. **View image**: Anyone with the link can view the shared image

## 🛠️ Setup & Deployment

### Prerequisites
- Python 3.11+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/telegram-image-bot.git
cd telegram-image-bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py