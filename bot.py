import os
import sqlite3
import logging
from telegram import Update, BotCommand, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging setup (Security & Error tracking-er jonno)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token
TOKEN = "8649527037:AAFPJRCau5uy2eAV5T4-UFpxx_LrFf3wFkg"

# --- STEP 1: DATABASE SETUP (SQLite) ---
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    # Users table to store balance & info
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_user(user_id, username):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)", (user_id, username, 0.0))
        conn.commit()
        balance = 0.0
    else:
        balance = row[0]
    conn.close()
    return balance

def update_balance(user_id, amount):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

# --- MENU BUTTON SETUP ---
async def post_init(application):
    commands = [
        BotCommand("start", "🔄 Restart Bot / Show Menu")
    ]
    await application.bot.set_my_commands(commands)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.username)

    welcome_text = (
        f"👋 **Welcome, {user.first_name}!**\n\n"
        "🚀 Amar ei Marketplace bot-e apnake shagotom. Nicher menu theke apnar proyojonio option select karun:"
    )
    
    keyboard = [
        ["🛒 Buy number", "💰 Deposit"],
        ["👤 Profile", "💸 Withdraw"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# --- BUTTON HANDLERS ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "👤 Profile":
        balance = get_user(user.id, user.username)
        profile_text = (
            f"👤 **User Profile:**\n\n"
            f"🆔 ID: `{user.id}`\n"
            f"👤 Name: {user.first_name}\n"
            f"💰 Balance: `${balance:.2f} USDT`"
        )
        await update.message.reply_text(profile_text, parse_mode="Markdown")

    elif text == "💰 Deposit":
        # --- STEP 2: PAYMENT GATEWAY (Inline Buttons for bKash/Crypto) ---
        keyboard = [
            [InlineKeyboardButton("bkash (Manual/Auto)", callback_data="pay_bkash")],
            [InlineKeyboardButton("Crypto (USDT/TRC20)", callback_data="pay_crypto")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("💳 Please select a payment method to deposit funds:", reply_markup=reply_markup)

    elif text == "🛒 Buy number":
        await update.message.reply_text("🛒 Current stock is empty. Please deposit first!")

    elif text == "💸 Withdraw":
        await update.message.reply_text("💸 Apnar balance-e porjapto fund nei.")

# --- PAYMENT CALLBACK HANDLER ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pay_bkash":
        await query.edit_message_text("📲 bKash Merchant/Personal No: `01XXXXXXXXX`\nSend money kore Transaction ID (TrxID) admin-ke pathan.")
    elif query.data == "pay_crypto":
        await query.edit_message_text("🪙 USDT (TRC20) Wallet Address:\n`TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`\nSend kore hash pathan.")

# --- ERROR HANDLER (STEP 3: SECURITY) ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main():
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Error logging
    application.add_error_handler(error_handler)

    print("Bot is running smoothly...")
    application.run_polling()

if __name__ == "__main__":
    main()