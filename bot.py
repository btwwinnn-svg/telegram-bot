from telegram import *
from telegram.ext import *
import random

TOKEN = "8713921344:AAHJd9RpKL_grLus46Pp9EPK2EuNtb0TZh8"

CHANNEL_LINK = "https://t.me/KWGPREDICTION_NUMBER"
CHANNEL_USERNAME = "@KWGPREDICTION_NUMBER"
ADMIN_LINK = "https://t.me/Boss_nikhill"
REGISTER_LINK = "https://kwgbet7.com/#/register?invitationCode=391E893774"

ADMIN_ID = 7512470737

users = set()

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.message.chat_id)

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Check Joined", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "⚠️ Pehle channel join karo fir aage badho",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# CHECK JOIN
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:

            keyboard = [
                ["🔮 Get Prediction"],
                ["🎮 Register Link", "📢 Prediction Channel"],
                ["👤 Admin"]
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.callback_query.message.reply_text(
                "✅ Ab niche se option select karo",
                reply_markup=reply_markup
            )
        else:
            await update.callback_query.answer("❌ Pehle join karo", show_alert=True)

    except:
        await update.callback_query.answer("❌ Error", show_alert=True)

# BUTTON HANDLE
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔮 Get Prediction":
        await update.message.reply_text("📩 3 digit period number bhejo")

    elif text == "🎮 Register Link":
        await update.message.reply_text(f"🎮 Register ➤ {REGISTER_LINK}")

    elif text == "📢 Prediction Channel":
        await update.message.reply_text(f"📢 Join ➤ {CHANNEL_LINK}")

    elif text == "👤 Admin":
        await update.message.reply_text(f"👤 Admin ➤ {ADMIN_LINK}")

    else:
        await prediction(update, context)

# PREDICTION
async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if len(text) == 3 and text.isdigit():
        last_digit = int(text[-1])

        # smart random logic
        if random.choice([True, False]):
            number = last_digit
        else:
            number = (last_digit + random.randint(1, 3)) % 9

        size = "SMALL" if number <= 4 else "BIG"

        tag = random.choice(["💎 SAFE", "⚡ RISKY", "🔥 STRONG"])

        message = f"""
✨ NIKHIL PREDICTION ✨

━━━━━━━━━━━━━━━
📊 PERIOD ➤ {text}

🎯 PREDICTION ➤ {size}
🔢 NUMBER ➤ {number}
━━━━━━━━━━━━━━━

{tag}
📢 JOIN ➤ {CHANNEL_LINK}

⚡ Next ke liye period bhejo
        """

        await update.message.reply_text(message)

    else:
        await update.message.reply_text("❌ Sirf 3 digit number bhejo")

# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    for user in users:
        try:
            await context.bot.send_message(user, msg)
        except:
            pass

    await update.message.reply_text("✅ Broadcast done")

# MAIN
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

print("✅ BOT RUNNING...")
app.run_polling()
