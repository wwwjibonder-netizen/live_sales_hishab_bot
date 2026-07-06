import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# BotFather থেকে পাওয়া আপনার আসল বটের টোকেনটি এখানে বসান
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# ১১টি অপশনের তালিকা (আপনার প্রজেক্ট অনুযায়ী নামগুলো বদলে নিতে পারেন)
OPTIONS = {
    "1": "📊 স্টক দেখুন (Stock)",
    "2": "💰 দৈনিক বিক্রি (Daily Sales)",
    "3": "🛒 নতুন আইটেম যোগ (Add Item)",
    "4": "📝 হিসাব আপডেট (Update Hishab)",
    "5": "❌ আইটেম বাদ দিন (Delete Item)",
    "6": "📉 লাভ-ক্ষতি (Profit/Loss)",
    "7": "👥 কাস্টমার লিস্ট (Customers)",
    "8": "🧾 ইনভয়েস তৈরি (Invoice)",
    "9": "💳 বাকি হিসাব (Due Register)",
    "10": "📅 মাসিক রিপোর্ট (Monthly Report)",
    "11": "⚙️ সেটিংস (Settings)"
}

# ইউজার যখন /start বা /menu লিখবেন, তখন ১১টি বাটন দেখাবে
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    # ১১টি অপশনকে লুপ ঘুরিয়ে বাটন আকারে সাজানো হচ্ছে (প্রতি লাইনে ২টি করে বাটন)
    buttons = []
    for key, value in OPTIONS.items():
        # callback_data হলো ইউজার ক্লিক করলে ব্যাকগ্রাউন্ডে পাইথনে যে ডাটা আসবে
        btn = InlineKeyboardButton(text=value, callback_data=f"option_{key}")
        buttons.append(btn)
    
    # বাটনগুলোকে ২ কলামে সুন্দর করে সাজানো
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
            
    bot.send_message(message.chat.id, "👋 সেলস হিসাব বটে আপনাকে স্বাগতম!\nনিচের ১১টি অপশন থেকে আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন:", reply_markup=markup)

# ইউজার কোনো বাটনে ক্লিক করলে এই ফাংশনটি কাজ করবে (আপনার ইনপুটের বিকল্প)
@bot.callback_query_handler(func=lambda call: call.data.startswith('option_'))
def callback_listener(call):
    option_id = call.data.split("_")[1] # ক্লিক করা অপশনের নাম্বার (১ থেকে ১১)
    option_name = OPTIONS[option_id]
    
    # স্ক্রিনের ওপর একটি ছোট পপ-আপ নোটিফিকেশন দেখাবে
    bot.answer_callback_query(call.id, text=f"আপনি সিলেক্ট করেছেন: {option_name}")
    
    # এখন পাইথনের ভেতরের অপশন অনুযায়ী কাজ শুরু হবে
    if option_id == "1":
        # এখানে আপনার ১ নম্বর অপশনের কোড বা ফাংশনটি বসবে
        bot.send_message(call.message.chat.id, "📊 আপনার বর্তমান স্টক লোড হচ্ছে... (এখানে আপনার স্টকের হিসাব দেখাবে)")
        
    elif option_id == "2":
        bot.send_message(call.message.chat.id, "💰 আজকের মোট বিক্রি দেখার জন্য কমান্ডটি রান হচ্ছে...")
        
    elif option_id == "3":
        # যদি এই অপশনে কোনো নাম টাইপ করার ইনপুট লাগে, তবে নিচের নিয়মে নিতে হবে:
        sent_msg = bot.send_message(call.message.chat.id, "🛒 যে নতুন আইটেমটি যোগ করতে চান, তার নাম লিখে পাঠান:")
        bot.register_next_step_handler(sent_msg, process_new_item_name)
        
    # বাকি ৪ থেকে ১১ নম্বর অপশনের লজিকগুলোও একইভাবে নিচে বসে যাবে...
    else:
        bot.send_message(call.message.chat.id, f"🛠️ {option_name} অপশনটির কাজ প্রক্রিয়াধীন রয়েছে।")

# অপশন ৩ এর জন্য ইউজার যে নাম লিখে পাঠাবে, তা রিসিভ করার ফাংশন
def process_new_item_name(message):
    item_name = message.text # এটিই আপনার input() এর বিকল্প অনলাইন সিস্টেম
    # এখন এই item_name টি আপনার ডাটাবেজে সেভ করতে পারবেন
    bot.reply_to(message, f"✅ সফলভাবে '{item_name}' আইটেমটি সিস্টেমে যুক্ত করা হয়েছে!")

# বটটি ২৪ ঘণ্টা সচল রাখার কমান্ড
print("বট সফলভাবে চালু হয়েছে...")
bot.infinity_polling()
