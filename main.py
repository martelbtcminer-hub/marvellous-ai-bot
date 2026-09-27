import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = 8148318952:AAHIVB8eyXke9UKeXCfj3PBC86BZOlDiwcE
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"balance": 3.0, "last_claim": 0, "total_withdraw": 0.0, "referrals": 0}
    return users[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id!= update.effective_user.id and referrer_id in users:
                users[referrer_id]["balance"] += 0.50
                users[referrer_id]["referrals"] += 1
        except: pass

    text = f"""
╔═══════════════════╗
   🚀 *MARVELLOUS AI*
   AI Grid Trading Bot
╚═══════════════════╝

👋 Welcome, {update.effective_user.first_name}!

┌─ *YOUR PORTFOLIO*
│ 💰 Balance: `{user['balance']:.4f} USDT`
│ 📊 Daily Yield: `2.7%`
│ ✅ Status: `Active`
└───────────────────

🎁 *New User Bonus Activated*
You received 3.00 USDT free for trading.

⏰ Claim profit every 24 hours and grow your portfolio.

▬▬▬▬▬▬▬▬
"""
    keyboard = [
        [InlineKeyboardButton("💸 CLAIM PROFIT", callback_data="claim")],
        [
            InlineKeyboardButton("💼 Portfolio", callback_data="balance"),
            InlineKeyboardButton("👥 Team", callback_data="ref")
        ],
        [InlineKeyboardButton("💳 WITHDRAW TO TRUST WALLET", callback_data="withdraw")],
        [InlineKeyboardButton("📈 How It Works", callback_data="how")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = get_user(query.from_user.id)
    now = time.time()

    if query.data == "claim":
        if now - user["last_claim"] < 86400:
            h = int((86400 - (now - user["last_claim"])) / 3600)
            m = int(((86400 - (now - user["last_claim"])) % 3600) / 60)
            await query.edit_message_text(f"⏳ *Profit already claimed*\n\nNext claim in: {h}h {m}m
