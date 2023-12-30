import os
import re
import yaml
import shutil
import subprocess
from os import path
from loguru import logger
from computer import Computer
from telebot import types, TeleBot
from wakeonlan import send_magic_packet

ALLOWED_IDS = os.getenv('ALLOWED_IDS')
BOT_TOKEN = os.getenv('BOT_TOKEN')

computers = []
config_path = "config/config.yaml"
messageid = 0
allowed_ids = os.getenv('ALLOWED_IDS')
bot_token = os.getenv('BOT_TOKEN')
statuses = {"online": "✅", "offline": "❌", "unknown": "❓"}
bot = TeleBot(bot_token)
        

# ------------- Get the device status -----------------
def ping(host):
    try:
        p = subprocess.Popen("fping -C1 -q "+ host +"  2>&1 | grep -v '-' | wc -l", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        status = re.findall('\d+', str(output))[0]
        if status=="1":
            return 'online'
        else:
            return 'offline'
    except Exception as e:
        logger.error(str(e))
        return 'unknown'


def wakeup(mac):
    try:
        send_magic_packet(mac)
        return True
    except Exception as e:
        logger.error(str(e))
        return False

# ------------- Get the list of computers from the config file -----------------
def get_computers():
    try:
        logger.info("Loading computers kids list")
        if not path.exists(config_path):
            shutil.copy('config.yaml', config_path)
        with open("config/config.yaml",'r',encoding='utf-8') as stream:
            try:
                for computer in yaml.safe_load(stream)["computers"]:
                    computers.append(Computer(name=computer["name"], mac = computer["mac"], ip = computer["ip"]))
                logger.info(str(len(computers)) + " Computers Loded")
            except yaml.YAMLError as exc:
                logger.error(exc)
    except Exception as e:
        logger.error(str(e))

# ------------- Build command keyboard -----------------
commands = [{"text": "Show all computers", "callback_data": "all"},
    {"text": "Show online computers", "callback_data": "online"},
    {"text": "Show offline computers", "callback_data": "offline"},
    {"text": "Cancel", "callback_data": "exit"},]


# ------------- Build computers keyboard -----------------
def computers_keyboard(status):
    markup = types.InlineKeyboardMarkup()
    markup.row_width=2
    try:
        for computer in computers:
            computer.status = ping(computer.ip)
 
        if status=="all":
            for computer in computers:
                markup.add(types.InlineKeyboardButton(
                    text=computer.name + " (" + statuses[computer.status] + ")",
                    callback_data="_computer_" + computer.mac))
        elif status=="online":
            for computer in computers:
                if computer.status=="online":
                    markup.add(types.InlineKeyboardButton(
                        text=computer.name + " (" + statuses[computer.status] + ")",
                        callback_data="_computer_" + computer.mac))
        else:
            for computer in computers:
                if computer.status=="offline":
                    markup.add(types.InlineKeyboardButton(
                        text=computer.name + " (" + statuses[computer.status] + ")",
                        callback_data="_computer_" + computer.mac))

        markup.add(types.InlineKeyboardButton(
                text="Back ↩",
                callback_data="back"))
        return markup  
    except Exception as e:
        logger.error("Error creating computers keyboard. " + str(e))




# ------------- Build command keyboard -----------------
def command_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=command['text'],
                    callback_data=command["callback_data"]
                )
            ]
            for command in commands
        ], row_width=1
    )


# ---------------- Handle the start menu --------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        global messageid
        if str(message.chat.id) in ALLOWED_IDS:
            messageid=bot.send_message(message.chat.id, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown').message_id
    except Exception as e:
        logger.error(e)


# ---------------- Handle the exit button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'exit')
def exit_callback(call: types.CallbackQuery):
   try:
    global messageid
    bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
   except Exception as e:
       logger.error(e)


# ---------------- Handle Show computers button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'all')
def list_all_computers(call: types.CallbackQuery):
    try:
        global messageid
        if str(call.message.chat.id) in ALLOWED_IDS:
            msg=bot.send_message(call.message.chat.id,text='All Computers', reply_markup=computers_keyboard("all"), parse_mode='Markdown')
            bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
            messageid = msg.message_id
    except Exception as e:
        logger.error("Error getting computers list. " + str(e))

# ---------------- Handle Show online button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'online')
def list_online_computers(call: types.CallbackQuery):
    try:
        global messageid
        if str(call.message.chat.id) in ALLOWED_IDS:
            msg=bot.send_message(call.message.chat.id,text='Online Computers', reply_markup=computers_keyboard("online"), parse_mode='Markdown')
            bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
            messageid = msg.message_id
    except Exception as e:
        logger.error("Error getting online computers list. " + str(e))

# ---------------- Handle Show offline button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'offline')
def list_offline_computers(call: types.CallbackQuery):
    try:
        global messageid
        if str(call.message.chat.id) in ALLOWED_IDS:
            msg=bot.send_message(call.message.chat.id,text='Offline Computers', reply_markup=computers_keyboard("offline"), parse_mode='Markdown')
            bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
            messageid = msg.message_id
    except Exception as e:
        logger.error("Error getting offline computers list. " + str(e))

# ---------------- Handle the back button --------------------
@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_callback(call: types.CallbackQuery):
   try:
    global messageid
    if str(call.message.chat.id) in ALLOWED_IDS:
            bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
            messageid=bot.send_message(call.message.chat.id, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown').message_id
   except Exception as e:
       logger.error(e)

    
@bot.callback_query_handler(func=lambda c: c.data.startswith('_computer_'))
def make_drink(call: types.CallbackQuery):
    try:
        global messageid
        mac=call.data.split("_computer_")[1]
        success = wakeup(mac)
        if success:
            bot.reply_to(call.message, "The magic packet sent successfully.")
        else:
            bot.reply_to(call.message, "Unable to send magick packet.")
        bot.delete_message(message_id=messageid,chat_id=call.message.chat.id)
        messageid=bot.send_message(call.message.chat.id, text="welcome", reply_markup=command_keyboard(), parse_mode='Markdown').message_id
    except Exception as e:
        logger.error("Error preparing drink. " + str(e))    


if __name__=="__main__":
    logger.info("Starting the bot")
    get_computers()
    bot.infinity_polling()
