import telebot
import smtplib
import random
from email.message import EmailMessage
from flask import Flask
from threading import Thread

# ফ্লাস্ক অ্যাপ (রেলওয়ে সার্ভার চালু রাখার জন্য)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# কনফিগারেশন
BOT_TOKEN = "8560427479:AAGKs3EaWdY5GfNZcdA2c1Fjt7Q63-biaoY"
SENDER_EMAIL = "ariyanxd02@gmail.com"
SENDER_PASSWORD = "iubadniiwcpucytc"

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! ওটিপি পেতে আপনার ইমেইল অ্যাড্রেসটি লিখুন।")

@bot.message_handler(func=lambda message: "@" in message.text)
def handle_email(message):
    email = message.text.strip()
    otp = str(random.randint(100000, 999999))
    try:
        msg = EmailMessage()
        msg['Subject'] = f"OTP: {otp}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg.set_content(f"আপনার কোডটি হলো: {otp}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        
        user_data[message.chat.id] = otp
        bot.reply_to(message, "ওটিপি পাঠানো হয়েছে। কোডটি দিন।")
    except Exception as e:
        bot.reply_to(message, f"ভুল হয়েছে: {e}")

@bot.message_handler(func=lambda message: message.text.isdigit())
def verify_otp(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id] == message.text.strip():
        bot.reply_to(message, "✅ ভেরিফিকেশন সফল!")
        del user_data[chat_id]
    else:
        bot.reply_to(message, "❌ ভুল ওটিপি!")

if __name__ == "__main__":
    # ওয়েব সার্ভার আলাদা থ্রেডে চালানো হচ্ছে
    t = Thread(target=run)
    t.start()
    print("Bot is running...")
    bot.infinity_polling()
                     
