import telebot

# আপনার নতুন টোকেনটি এখানে বসানো হলো
API_TOKEN = '8816266276:AAECNvhB4uqXNsOBCcdGjl_hsshIXb9DE7A'
bot = telebot.TeleBot(API_TOKEN)

from datetime import datetime  
import json  
import os

# Pyroid3 এর জন্য ফোনের Documents ফোল্ডারে ফাইল সেভ করার পাথ ফিক্স করা হলো
STORAGE_DIR = "/storage/emulated/0/Documents"
DB_FILE = os.path.join(STORAGE_DIR, "inventory_data.json")

# ফোল্ডার না থাকলে তৈরি করার চেষ্টা করবে
if not os.path.exists(STORAGE_DIR):
    try:
        os.makedirs(STORAGE_DIR, exist_ok=True)
    except:
        DB_FILE = "inventory_data.json"

# প্রোগ্রাম चालू হওয়ার সময় ফাইল থেকে ডাটা লোড করার ফাংশন
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("item_database", {}), data.get("sales_history", {})
        except:
            return {}, {}
    return {}, {}

# ভুল সংশোধন ১: ফাংশনটি কল করে পুরনো ডাটা লোড করা হলো
# ভুল সংশোধন ২: নিচে আর নতুন করে item_database = {} লিখে খালি করা হয়নি
item_database, sales_history = load_data()

current_now = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
print("========================================")
print(f"⏰Current D/Time:{current_now}")
print("========================================\n")

print("--- enter your item information ---")
#name = input("    item Name: ")
#quantity = int(input("item Quantity: "))
print("********************")

# আগে থেকে আইটেমটি থাকলে পরিমাণ যোগ হবে, না থাকলে নতুন তৈরি হবে (যাতে পুরনো ডাটা না মুছে যায়)
if name in item_database:
    item_database[name] += quantity
else:
    item_database[name] = quantity

input_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p') 
print(f"✅succss! Date:{input_time}]")
print(f"item name: {name} ---quantity: {item_database[name]}\n")
print("********************")

import threading

# টেলিগ্রাম বটের কাজ সামলানোর জন্য বিশেষ ফাংশন
def start_telegram_bot():
    @bot.message_handler(commands=['start', 'menu'])
    def welcome(message):
        bot.reply_to(message, "📊 Live Sales Hishab Bot অনলাইনে সচল আছে!\nস্টক দেখতে টাইপ করুন: /stock")

    @bot.message_handler(commands=['stock'])
    def send_stock(message):
        # এটি সরাসরি আপনার ফাইলে থাকা লাইভ স্টক টেলিগ্রামে দেখাবে
        if not item_database:
            bot.reply_to(message, "⚠️ Stock is empty!")
            return
        reply = "📦 --- CURRENT ITEM STOCK LIST ---\n"
        for item_name, qty in item_database.items():
            reply += f"Name: {item_name} = Quantity: {qty}\n"
        bot.reply_to(message, reply)

    bot.infinity_polling(timeout=10, long_polling_timeout=5)

# আপনার while True: মেনু শুরু হওয়ার ঠিক উপরে বটটিকে ব্যাকগ্রাউন্ডে চালু করা হলো
# এটি আপনার কনসোলের ইনপুটকে কোনো ডিস্টার্ব করবে না
threading.Thread(target=start_telegram_bot, daemon=True).start()
print("🤖 টেলিগ্রাম বট সফলভাবে ব্যাকগ্রাউন্ডে চালু হয়েছে!")


while True:
    print("\n--- enter your choice ---")
    print("1.  (Exit)")
    print("2.  (Sell item)")
    print("3.  (Add/Update item)")
    print("4.  (All item list & Sales History)")
    print("5.  (Delete)")
    print("6.  (Search)")
    print("7,  (personal item input rate)")
    print("8.  (save data)")
    print("9.  (item edit)")
    print("10.(day by day data sho)")
    print("11. (day by day rate)")
    choice = input("enter your choice (1-11): ") 
    
    if choice == '1':
        # এক্সিট করার সময় স্বয়ংক্রিয়ভাবে সেভ হবে
        data_to_save = {"item_database": item_database, "sales_history": sales_history}
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print("💾 Data safely auto-saved before exit!")
        except Exception as e:
            print(f"❌ Auto-save failed: {e}")
            
        exit_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(f"The program exited at {exit_time}. Thanks!")
        break
    elif choice == '2':
        print("\n--- Sell Item ---")
        sell_name = input("Enter item name to sell: ").strip()
        if sell_name in item_database:
            sell_qty = int(input(f"Enter quantity to sell (Available: {item_database[sell_name]}): "))
            if sell_qty <= item_database[sell_name]:
                item_database[sell_name] -= sell_qty
                
                # sales_history আপডেট করার লজিক (তারিখ অনুযায়ী ডিকশনারি)
                today_date = datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.now().strftime('%I:%M:%S %p')
                
                if today_date not in sales_history:
                    sales_history[today_date] = []
                
                sales_history[today_date].append({
                    "time": current_time,
                    "item": sell_name,
                    "quantity": sell_qty
                })
                print(f"✅ Success! Sold {sell_qty} of {sell_name}.")
            else:
                print("❌ Not enough quantity in stock!")
        else:
            print("❌ Item not found in database!")

    elif choice == '3':
        print("\n--- Add/Update Item ---")
        name = input("    item Name: ")
        quantity = int(input("item Quantity: "))
        if name in item_database:
            item_database[name] += quantity
        else:
            item_database[name] = quantity
        print(f"✅ Success! Updated {name} quantity to {item_database[name]}.")

    elif choice == '4':
        if not item_database:
            print("\n⚠️ Stock is empty!")
        else:
            print(f"\n📦 --- CURRENT ITEM STOCK LIST ---")
            for name, info in item_database.items():
                print(f"Name: {name} = Quantity: {info}")
        print("\n📊 --- SALES HISTORY BY DATE ---")
        if not sales_history:
            print("No items sold yet!")
        else:
            for date, sales_list in sales_history.items():
                print(f"📅 Date: {date}")
                for sale in sales_list:
                    print(f"   - [{sale['time']}] Sold: {sale['item']} | Quantity: {sale['quantity']}")

    elif choice == '5':
        print("\n--- Delete Item ---")
        del_name = input("Enter the item name to delete from stock: ").strip()
        if del_name in item_database:
            del item_database[del_name]
            print(f"✅ '{del_name}' has been deleted from database.")
        else:
            print("❌ Item not found!")

    elif choice == '6':
        print("\n--- Search Item ---")
        search_name = input("Enter item name to search: ").strip()
        if search_name in item_database:
            print(f"🔍 Found! Item: {search_name} | Available Quantity: {item_database[search_name]}")
        else:
            print("❌ Item not found!")

    elif choice =='7':
        print("\n==========================================")
        print("      enter item price     ")
        print("==========================================")
        if not item_database:
            print("enter your item")
        else:
            grand_total = 0  # সর্বমোট বিল রাখার জন্য
            # ২০টি এন্ট্রির মধ্য থেকে নির্দিষ্ট আইটেম ফিল্টার করা
            filter_input = input("only anather input_time (exum: com, box)। all report only enter: ")
            # ইনপুট প্রসেস করে লিস্টে রূপান্তর করা
            requested_items = []
            if filter_input.strip():
                requested_items = [i.strip() for i in filter_input.split(',')]
            print("\n------ account trport ------")
            for item_name, item_quantity in item_database.items():
                # যদি নির্দিষ্ট ফিল্টার থাকে এবং এই আইটেমটি ফিল্টারের তালিকায় না থাকে, তবে এটি স্কিপ করবে
                if requested_items and item_name not in requested_items:
                    continue
                # ইনপুট নেওয়ার সময় খালি (Enter) রাখলে এরর হ্যান্ডেল করা
                price_input = input(f"enter price for {item_name} (not inpit entry Enter press): ")
                
                # যদি ইউজার কিছু না লিখে সরাসরি এন্টার চাপে, তবে দাম ০ ধরা হবে এবং এরর আসবে না
                if price_input.strip() == '':
                    price = 0
                else:
                    price = int(price_input)
                # যদি দাম ০ হয়, তবে সেটি রিপোর্টে দেখানোর প্রয়োজন নেই (পরের আইটেমে চলে যাবে)
                if price == 0:
                    continue
                total = item_quantity * price
                grand_total += total
                # কাঙ্ক্ষিত ফরম্যাট: com-20*130=2600
                print(f"👉 {item_name}-{item_quantity}*{price}={total}")
                print("------------------------------------------")
                print(f"💵  (Grand Total): {grand_total}")
                print("==========================================") 

    elif choice == '8':
        data_to_save = {
            "item_database": item_database,
            "sales_history": sales_history
        }
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            print("💾 Data saved successfully!")
        except Exception as e:
            print(f"❌ Save failed: {e}")

    elif choice == '9':
        print("*************************")
        edit_name = input("Enter the item name you want to EDIT: ")
        if edit_name in item_database:
            print(f"Current Quantity of '{edit_name}' is: {item_database[edit_name]}")
            print("What do you want to change?")
            print("1. Change Item Name")
            print("2. Change Quantity (Overwrite)")
            print("3. Change Both (Name & Quantity)")
            sub_choice = input("Enter your edit option (1/2/3): ")
            if sub_choice == '1':
                changed_name = input("Enter NEW Item Name: ")
                item_database[changed_name] = item_database.pop(edit_name)
                print(f"✅ Success! Name changed from '{edit_name}' to '{changed_name}'")
            elif sub_choice == '2':
                changed_quantity = int(input("Enter NEW Quantity: "))
                item_database[edit_name] = changed_quantity
                print(f"✅ Success! Quantity updated to {changed_quantity}")
            elif sub_choice == '3':
                changed_name = input("Enter NEW Item Name: ")
                changed_quantity = int(input("Enter NEW Quantity: "))
                item_database.pop(edit_name)
                item_database[changed_name] = changed_quantity
                print(f"✅ Success! Both Name and Quantity updated.")
            else:
                print("Invalid Option selected!")

    elif choice == '10':
        search_date = input("📅 যে তারিখের তথ্য দেখতে চান তা লিখুন (Format: YYYY-MM-DD): ").strip()
        try:
            parts = search_date.split('-')
            if len(parts) == 3:
                search_date = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        except Exception:
            pass

        print(f"\n================📊 {search_date} তারিখের বিক্রয়ের ইতিহাস 📊================")
        if search_date in sales_history:
            sales_list = sales_history[search_date]
            for sale in sales_list:
                print(f"   - [{sale['time']}] Sold: {sale['item']} | Quantity: {sale['quantity']}")
        else:
            print("❌ এই তারিখে কোনো বিক্রয়ের তথ্য পাওয়া যায়নি।")
        print("===================================================================\n")

    elif choice == '11':
        search_date = input("📅 যে তারিখের মোট বিক্রয় হিসাব করতে চান (Format: YYYY-MM-DD): ").strip()
        try:
            parts = search_date.split('-')
            if len(parts) == 3:
                search_date = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        except Exception:
            pass

        print(f"\n================💰 {search_date} তারিখের লাইভ হিসাব 💰================")
        if search_date in sales_history:
            sales_list = sales_history[search_date]
            summary_sales = {}
            for sale in sales_list:
                item_name = sale['item']
                qty = sale['quantity']
                summary_sales[item_name] = summary_sales.get(item_name, 0) + qty
                
            print("🛒 এই তারিখে বিক্রিত আইটেমের তালিকা ও দাম ইনপুট দিন:")
            print("-" * 50)
            
            total_revenue = 0
            final_report = []
            for item_name, total_qty in summary_sales.items():
                print(f"➔ আইটেম: {item_name} | মোট বিক্রি: {total_qty} টি")
                rate = float(input(f"   💸 এই আইটেমটির প্রতি পিসের দাম (Rate) লিখুন: "))
                item_total = total_qty * rate
                total_revenue += item_total
                final_report.append((item_name, total_qty, rate, item_total))
                print()
                
            print("-" * 50)
            print(f"{'Item Name':<15} | {'Total Qty':<10} | {'Rate':<8} | {'Total':<10}")
            print("-" * 50)
            for item_name, total_qty, rate, item_total in final_report:
                print(f"{item_name:<15} | {total_qty:<10} | {rate:<8.2f} | {item_total:<10.2f} টাকা")
                
            print("-" * 50)
            print(f"🎉 {search_date} তারিখে সর্বমোট বিক্রি হয়েছে: {total_revenue:.2f} টাকা")
        else:
            print("❌ এই তারিখে কোনো বিক্রয়ের তথ্য পাওয়া যায়নি।")
        print("===================================================================\n")


                          
    
else:
            print("❌ Item not found in stock!")
            print("*************************")
            import threading

# টেলিগ্রাম বটের কমান্ড হ্যান্ডলার ফাংশন
def telegram_bot_setup():
    import telebot
    
    API_TOKEN = '8816266276:AAECNvhB4uqXNsOBCcdGjl_hsshIXb9DE7A'
    bot = telebot.TeleBot(API_TOKEN)
    
    @bot.message_handler(commands=['start', 'menu'])
    def send_welcome(message):
        bot.reply_to(message, "📊 Live Sales Hishab Bot চালু আছে! আপনি অ্যাপ বা কনসোল থেকে হিসাব নিয়ন্ত্রণ করুন।")

    @bot.message_handler(commands=['stock'])
    def show_stock(message):
        # এটি সরাসরি আপনার গ্লোবাল item_database থেকে লাইভ স্টক দেখাবে
        reply_text = "📦 --- CURRENT ITEM STOCK LIST ---\n"
        for name, info in item_database.items():
            reply_text += f"Name: {name} = Quantity: {info}\n"
        bot.reply_to(message, reply_text)
        
    print("🤖 টেলিগ্রাম বট ব্যাকগ্রাউন্ডে কানেক্ট হচ্ছে...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    bot_thread = threading.Thread(target=telegram_bot_setup, daemon=True)
    bot_thread.start()

# ----------------------------------------------------
# এরপর আপনার আসল ১১টি অপশনের while True মেনু কোডটি থাকবে
# ----------------------------------------------------
