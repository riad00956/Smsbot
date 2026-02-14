import telebot
import smtplib
import random
import os
from email.message import EmailMessage
from flask import Flask
from threading import Thread

# রেলওয়ে বা ক্লাউড সার্ভার সচল রাখার জন্য ছোট একটি ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # রেলওয়ে সাধারণত পরিবেশ চলক থেকে পোর্ট নেয়, না থাকলে ৮MD৮MD ব্যবহার করবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- কনফিগারেশন ---
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
        msg['Subject'] = f"আপনার ওটিপি কোড: {otp}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg.set_content(f"আপনার ভেরিফিকেশন কোডটি হলো: {otp}\nএটি কারো সাথে শেয়ার করবেন না।")

        # Port 587 (TLS) ব্যবহার করা হচ্ছে যা সার্ভারে বেশি স্ট্যাবল
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as smtp:
            smtp.starttls() 
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        
        user_data[message.chat.id] = otp
        bot.reply_to(message, "✅ আপনার ইমেইলে একটি ওটিপি পাঠানো হয়েছে। কোডটি এখানে লিখে দিন।")
    
    except Exception as e:
        bot.reply_to(message, f"❌ ইমেইল পাঠানো যায়নি। এরর: {e}")

@bot.message_handler(func=lambda message: message.text.isdigit())
def verify_otp(message):
    chat_id = message.chat.id
    user_otp = message.text.strip()

    if chat_id in user_data:
        if user_data[chat_id] == user_otp:
            bot.reply_to(message, "🎉 অভিনন্দন! ভেরিফিকেশন সফল হয়েছে।")
            del user_data[chat_id]
        else:
            bot.reply_to(message, "⚠️ ভুল ওটিপি! আবার চেষ্টা করুন।")
    else:
        bot.reply_to(message, "আগে আপনার ইমেইল দিয়ে ওটিপি রিকোয়েস্ট করুন।")

if __name__ == "__main__":
    # ওয়েব সার্ভার ব্যাকগ্রাউন্ডে চালু করা
    t = Thread(target=run)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()
