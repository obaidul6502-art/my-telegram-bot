import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN", "8649527037:AAFtL9CpErLfbGT8J3xxo831CJjIEOxWMTM")

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
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is starting polling on Koyeb...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()