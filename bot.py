import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Railway Environment থেকে BOT_TOKEN গ্রহণ
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # কাস্টম ওয়েলকাম মেসেজ
    welcome_text = (
        "👋 **আমাদের বটে আপনাকে স্বাগতম!**\n\n"
        "🚀 নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি নির্বাচন করুন:"
    )
    
    # মেনু বাটনসমূহ (কিবোর্ড Layout)
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    
    # বাটনগুলো রেসপনসিভভাবে দেখানোর জন্য
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # ইউজারকে মেসেজ ও বাটন পাঠানো
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN পাওয়া যায়নি! Railway Variables চেক করুন।")
        return

    # Application তৈরি
    application = ApplicationBuilder().token(TOKEN).build()

    # /start কমান্ডের হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler("start", start))

    # পোলিং রান করা
    application.run_polling()

if __name__ == "__main__":
    main()