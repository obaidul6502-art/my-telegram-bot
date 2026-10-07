import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN", "8649527037:AAFtL9CpErLfbGT8J3xxo831CJjIEOxWMTM")
# Render-এর নিজস্ব External URL
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "https://my-telegram-bot-a2t1.onrender.com")

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

def main():
    port = int(os.environ.get("PORT", 10000))
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    # Native Webhook Server for Render
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{RENDER_EXTERNAL_URL}/{TOKEN}"
    )

if __name__ == '__main__':
    main()