import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Railway-এর এনভায়রনমেন্ট থেকে টোকেন নেওয়া
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! বট সফলভাবে চালু হয়েছে।")

def main():
    # নতুন ভার্সনের নিয়ম অনুযায়ী Application তৈরি
    application = ApplicationBuilder().token(TOKEN).build()

    # /start কমান্ড হ্যান্ডলার যোগ করা
    application.add_handler(CommandHandler("start", start))

    # পোলিং শুরু করা
    application.run_polling()

if __name__ == "__main__":
    main()