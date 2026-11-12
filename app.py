import asyncio
import getpass
import random
import os
import qrcode
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Твої дані з my.telegram.org
api_id = 30872064
api_hash = 'e79a1872da891b0450fa8c8ff76e4f8e'

# Твій головний юзернейм
MY_USERNAME = "bobervtapkax"

# Ініціалізація клієнта з маскуванням під реальний пристрій Android
client = TelegramClient(
    'my_session',
    api_id,
    api_hash,
    device_model="Samsung Galaxy S23",
    system_version="Android 14",
    app_version="10.14.5",
    lang_code="uk",
    system_lang_code="uk-UA"
)

muted_chats = set()

ball_answers = [
    "стопудово", 
    "можливо", 
    "50/50", 
    "ні", 
    "абсолютно так", 
    "я не знаю лол", 
    "ліпше не казати"
]

@client.on(events.NewMessage(incoming=True, outgoing=True))
async def command_handler(event):
    if not event.raw_text:
        return

    text = event.raw_text.strip()
    chat_id = event.chat_id
    sender = await event.get_sender()
    
    # Визначаємо, чи це пишеш ти
    is_me = event.out or (sender and sender.username and sender.username.lower() == MY_USERNAME.lower())

    # 4. Команда .ball працює ДЛЯ ВСІХ у ЛС або твоїх чатах
    if text.startswith('.ball') and (event.is_private or event.out):
        await event.delete()
        parts = text.split(' ', 1)
        question = parts[1] if len(parts) > 1 else "не вказано питання"
        answer = random.choice(ball_answers)
        
        # Отримуємо юзернейм автора або ім'я, якщо юзернейма немає
        if event.out:
            author_tag = f"@{MY_USERNAME}"
        elif sender and sender.username:
            author_tag = f"@{sender.username}"
        elif sender and sender.first_name:
            author_tag = sender.first_name
        else:
            author_tag = "Анонім"

        await client.send_message(
            chat_id, 
            f"👤 Запитання від: **{author_tag}**\n"
            f"🎱 Питання: {question}\n"
            f"🔮 Відповідь кулі: **{answer}**"
        )
        return

    # Усі інші команди працюють ТІЛЬКИ ДЛЯ ТЕБЕ (is_me)
    if is_me and (event.is_private or event.out):
        
        # 1. Команда .mute
        if text == '.mute':
            if event.out:
                await event.edit("🔕 Режим муту увімкнено. Усі повідомлення цього юзера будуть видалятись.")
            else:
                await event.delete()
            muted_chats.add(chat_id)

        # 2. Команда .unmute
        elif text == '.unmute':
            if chat_id in muted_chats:
                muted_chats.remove(chat_id)
            if event.out:
                await event.edit("🔔 Режим муту вимкнено.")
            else:
                await event.delete()

        # 3. Команда .bober
        elif text == '.bober':
            await event.delete()
            for _ in range(10):
                await client.send_message(chat_id, "бобер")
                await asyncio.sleep(0.4)

        # 5. Команда .cmds
        elif text == '.cmds':
            if event.out:
                await event.edit(
                    "🛠 **Доступні команди юзербота:**\n\n"
                    "• `.mute` — мут співрозмовника (тільки для тебе)\n"
                    "• `.unmute` — зняти мут (тільки для тебе)\n"
                    "• `.ball [текст]` — магічна куля (працює для всіх!)\n"
                    "• `.cat` — випадковий кіт (тільки для тебе)\n"
                    "• `.bober` — спам бобрів (тільки для тебе)\n"
                    "• `.cmds` — список команд"
                )
            else:
                await event.delete()
                await client.send_message(chat_id, "🛠 Доступні команди: `.mute`, `.unmute`, `.ball <текст>`, `.cat`, `.bober`, `.cmds`")

        # 6. Команда .cat
        elif text == '.cat':
            await event.delete()
            cat_files = ['cat.png', 'cat1.png', 'cat2.png', 'cat3.png', 'cat4.png', 'cat5.png']
            existing_cats = [f for f in cat_files if os.path.exists(f)]
            
            if existing_cats:
                chosen_cat = random.choice(existing_cats)
                await client.send_file(chat_id, chosen_cat, caption="🐾")
            else:
                await client.send_message(chat_id, "⚠️ У палці немає картинок котів (cat.png тощо)!")

@client.on(events.NewMessage(incoming=True))
async def mute_watcher(event):
    if event.chat_id in muted_chats:
        try:
            await event.delete()
        except Exception:
            pass  

async def main():
    await client.connect()
    
    if not await client.is_user_authorized():
        qr_login = await client.qr_login()
        qr = qrcode.QRCode()
        qr.add_data(qr_login.url)
        qr.print_ascii(invert=True)
        print("\nВідскануй цей QR-код у Telegram: Налаштування -> Пристрої -> Підключити пристрій")
        
        try:
            await qr_login.wait()
        except SessionPasswordNeededError:
            password = getpass.getpass("Введи хмарний пароль (2FA): ")
            await client.sign_in(password=password)

    print("Юзербот успішно запущений і готовий!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
