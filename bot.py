import os
from telegram import Update, BotCommand, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# বট চালু হওয়ার পর মেনু বাটন সেট করার ফাংশন
async def post_init(application):
    commands = [
        BotCommand("start", "বট পুনরায় শুরু করুন")
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 আমাদের বটে আপনাকে স্বাগতম!"
    
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

def main():
    # post_init যুক্ত করে Application তৈরি
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()