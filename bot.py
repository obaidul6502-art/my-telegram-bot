import os
from telegram import Update, BotCommand, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Railway Environment থেকে BOT_TOKEN গ্রহণ
TOKEN = os.environ.get("BOT_TOKEN")

# বট চালু হওয়ার সাথে সাথে চ্যাট বক্সে Menu Button সেট করার ফাংশন
async def post_init(application):
    commands = [
        BotCommand("start", "🔄 বট পুনরায় চালু করুন / মেনু দেখুন")
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **আমাদের বটে আপনাকে স্বাগতম!**\n\n"
        "🚀 নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি নির্বাচন করুন:"
    )
    
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN পাওয়া যায়নি!")
        return

    # post_init যুক্ত করে Application তৈরি
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # /start কমান্ড হ্যান্ডলার যোগ করা
    application.add_handler(CommandHandler("start", start))

    # পোলিং চালু করা
    application.run_polling()

if __name__ == "__main__":
    main()