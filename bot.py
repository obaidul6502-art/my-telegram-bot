import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "8649527037:AAFtL9CpErLfbGT8J3xxo831CJjIEOxWMTM")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "https://my-telegram-bot-a2t1.onrender.com")

# 1. Flask App (gunicorn eta kei খুঁজছে)
app = Flask(__name__)

# 2. Telegram Application
bot_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Profile", callback_data='profile')],
        [InlineKeyboardButton("🛒 Buy Number", callback_data='buy')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Bot! Choose an option below:", reply_markup=reply_markup)

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

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_click))

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# Set Webhook loop
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

async def setup_webhook():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(f"{RENDER_URL}/{TOKEN}")

loop.run_until_complete(setup_webhook())