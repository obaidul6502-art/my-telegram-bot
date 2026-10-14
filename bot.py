import os
from telegram import Update, BotCommand, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token variable
TOKEN = os.environ.get("8649527037:AAFPJRCau5uy2eAV5T4-UFpxx_LrFf3wFkg")

# Chat box-er pashiyo Menu button set korar jonno
async def post_init(application):
    commands = [
        BotCommand("start", "🔄 Restart Bot / Show Menu")
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Welcome Message
    welcome_text = (
        "👋 **Welcome to My-First-Test-Bot!**\n\n"
        "🚀 Please select an option from the menu below:"
    )
    
    # Keyboard Buttons
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return

    # Application Build
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))

    # Run polling
    application.run_polling()

if __name__ == "__main__":
    main()