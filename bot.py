import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dummy Flask App to keep Render service active
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# Bot Token
TOKEN = os.getenv("BOT_TOKEN", "8649527037:AAFtL9CpErLfbGT8J3xxo831CJjIEOxWMTM")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Profile", callback_data='profile')],
        [InlineKeyboardButton("🛒 Buy Number", callback_data='buy')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the Bot! Choose an option below:",
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'profile':
        user = query.from_user
        msg = f"👤 **Profile Info:**\nName: {user.full_name}\nID: `{user.id}`"
        await query.edit_message_text(text=msg, parse_mode="Markdown")
    elif query.data == 'buy':
        await query.edit_message_text(text="🛒 Buy Number service is currently under maintenance.")
    elif query.data == 'help':
        await query.edit_message_text(text="ℹ️ Send /start to reload the main menu.")

def main():
    # Start Keep-Alive Web Server
    keep_alive()

    # Telegram Bot Application
    bot_app = Application.builder().token(TOKEN).build()
    
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(button_click))

    print("Bot with Keep-Alive Web Server is running...")
    bot_app.run_polling()

if __name__ == '__main__':
    main()