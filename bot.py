import os
from telegram import Update, BotCommand, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# আপনার নতুন বট টোকেন সরাসরি এখানে বসানো হলো
TOKEN = "8649527037:AAFPJRCau5uy2eAV5T4-UFpxx_LrFf3wFkg"

# চ্যাট বক্সের কোণায় Menu বাটন সেট করার জন্য
async def post_init(application):
    commands = [
        BotCommand("start", "🔄 Restart Bot / Show Menu")
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Welcome to My-First-Test-Bot!**\n\n"
        "🚀 Please select an option from the menu below:"
    )
    
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    # Application তৈরি
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Handler যুক্ত করা
    application.add_handler(CommandHandler("start", start))

    # Polling চালু
    application.run_polling()

if __name__ == "__main__":
    main()