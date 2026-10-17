import telebot
from telebot import types
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8806006597:AAH45QsGbiUl67yyLhqfpOzs5C5vE7Hbt2E")
ADMIN_ID = 7087751717
bot = telebot.TeleBot(BOT_TOKEN)

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

@bot.message_handler(commands=['start', 'admin'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {"balance": 0, "mining": False}
        save_users()
    if message.from_user.id == ADMIN_ID and message.text == "/admin":
        total_users = len(users)
        bot.send_message(message.chat.id, f"OWNER PANEL\nTotal Users: {total_users}\nYou have full access!")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Start Mining"), types.KeyboardButton("Balance"))
    markup.add(types.KeyboardButton("Referral"), types.KeyboardButton("Withdraw"))
    text = "Welcome to Robolexm Mining Bot\n\nMining every 6 hours\n1000 coin = 10 USDT / TON\nWithdraw: TON, USDT\n\nStart Mining Now!"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {"balance": 0, "mining": False}
    if message.text == "Start Mining":
        bot.send_message(message.chat.id, "Mining Started!\nCome back after 6 hours to claim reward.")
    elif message.text == "Balance":
        bal = users[user_id]["balance"]
        bot.send_message(message.chat.id, f"Your Balance: {bal} RLX")
    elif message.text == "Referral":
        bot.send_message(message.chat.id, f"Your Referral Link:\nhttps://t.me/RobolexmBot?start={message.from_user.id}")
    elif message.text == "Withdraw":
        bot.send_message(message.chat.id, "Minimum Withdraw: 1000 RLX\nWithdraw methods: TON, USDT")

print("RobolexmBot Running with Full Owner Access...")
bot.infinity_polling()
