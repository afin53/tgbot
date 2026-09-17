import logging
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- НАЛАШТУВАННЯ ---
TOKEN = "8947181297:AAFWwYMv3COTxHuNlnYhpDBhPDARlBqDfSc"  # Замініть на токен від @BotFather
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- ГЕНЕРАЦІЯ ТА СХОВИЩЕ КЛЮЧІВ ---
def generate_key():
    """Генерує ключ формату XXXX-XXXX-XXXX-XXXX"""
    parts = []
    for _ in range(4):
        part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        parts.append(part)
    return '-'.join(parts)

# 15 згенерованих ключів
VALID_KEYS = [generate_key() for _ in range(15)]

# Стан користувачів (для прототипу — у пам'яті)
# user_id: {"activated": bool, "used_key": str}
user_sessions = {}

# --- РЕЦЕПТ ---
SALAD_RECIPE = """🐟 Оселедець під шубою

🥗 Інгредієнти:

    🐟 оселедець солоний — 2 шт.;
    🧅 цибуля — 1 шт.;
    🥔 картопля — 3 шт.;
    🥕 морква — 3 шт.;
    🟣 буряк — 2 шт.;
    🍏 яблуко — 2 шт.;
    🥚 яйця — 2 шт.;
    🤍 майонез — 200 г;
    🧂 сіль — за смаком.

👩‍🍳 Приготування:

    🔪 Оселедець обробити на філе і нарізати невеликими шматочками.
    🥔 Картоплю, моркву і буряк вимити і відварити в мундирі до готовності. Дати охолонути.
    🫘 Усі овочі та яблуко очистити і натерти окремо: на великій тертці, цибулю подрібнити.
    🥚 Яйця зварити круто і натерти на дрібній тертці.
    🍽 На велику тарілку викласти половину картоплі, потім — шар оселедця та цибулі, змастити майонезом.
    🥕 Далі викласти шар моркви, потім — шар буряків, яйця. Кожен шар злегка посолити і змастити майонезом.
    🍎 Останнім шаром викласти картоплю, яблука. Зверху і з боків покласти буряк.
    🥄 Розрівняти поверхню, змастити майонезом і поставити в холодильник на 2–3 години.
    🌿 Перед подачею можна присипати подрібненою зеленою цибулею.

Смачного! 😋"""

# --- КЛАВІАТУРИ ---
def get_start_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔑 Ввести ключ", callback_data="enter_key")],
        [InlineKeyboardButton("💳 Отримати ключ", callback_data="get_key")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_key_info_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_start")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_enter_key_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_start")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🥗 Салати", callback_data="cat_salads")],
        [InlineKeyboardButton("🍳 Смачні сніданки", callback_data="cat_breakfast")],
        [InlineKeyboardButton("🍲 Обід", callback_data="cat_lunch")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_salads_keyboard():
    keyboard = [
        [InlineKeyboardButton("🐟 Оселедець під шубою", callback_data="recipe_herring")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_in_dev_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# --- ХЕНДЛЕРИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка /start"""
    user_id = update.effective_user.id

    # Скидаємо стан при новому /start (окрім вже активованих)
    if user_id not in user_sessions or not user_sessions[user_id].get("activated"):
        user_sessions[user_id] = {"activated": False, "used_key": None}

    text = (
        "👋 Ласкаво просимо до бота з домашніми рецептами!\n\n"
        "Тут ви знайдете перевірені рецепти страв, які легко приготувати вдома."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=get_start_keyboard())
    else:
        await update.message.reply_text(text, reply_markup=get_start_keyboard())


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка всіх inline-кнопок"""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if user_id not in user_sessions:
        user_sessions[user_id] = {"activated": False, "used_key": None}

    session = user_sessions[user_id]

    # --- НАВІГАЦІЯ ---
    if data == "back_to_start":
        text = (
            "👋 Ласкаво просимо до бота з домашніми рецептами!\n\n"
            "Тут ви знайдете перевірені рецепти страв, які легко приготувати вдома."
        )
        await query.edit_message_text(text, reply_markup=get_start_keyboard())
        return

    if data == "get_key":
        text = (
            "💳 Щоб отримати ключ доступу, напишіть користувачу @Ketotifen\n\n"
            "Ви зможете купити ключ всього за 15 грн/місяць."
        )
        await query.edit_message_text(text, reply_markup=get_key_info_keyboard())
        return

    if data == "enter_key":
        if session["activated"]:
            await query.edit_message_text(
                "✅ Ви вже активували ключ. Перейдіть до меню рецептів.",
                reply_markup=get_back_to_menu_keyboard()
            )
            return
        text = "🔑 Введіть ваш ключ у форматі XXXX-XXXX-XXXX-XXXX:"
        await query.edit_message_text(text, reply_markup=get_enter_key_keyboard())
        # Встановлюємо стан очікування введення ключа
        context.user_data["awaiting_key"] = True
        return

    # --- МЕНЮ КАТЕГОРІЙ (доступне після активації) ---
    if data == "back_to_menu":
        if not session["activated"]:
            await query.edit_message_text(
                "🔑 Спочатку введіть ключ доступу.",
                reply_markup=get_start_keyboard()
            )
            return
        text = "📖 Оберіть категорію рецептів:"
        await query.edit_message_text(text, reply_markup=get_main_menu_keyboard())
        return

    # --- КАТЕГОРІЇ ---
    if data == "cat_salads":
        text = "🥗 Салати:\n\nОберіть рецепт:"
        await query.edit_message_text(text, reply_markup=get_salads_keyboard())
        return

    if data in ("cat_breakfast", "cat_lunch"):
        text = "🚧 Розділ у розробці. Зовсім скоро тут з'являться нові рецепти!"
        await query.edit_message_text(text, reply_markup=get_in_dev_keyboard())
        return

    # --- РЕЦЕПТИ ---
    if data == "recipe_herring":
        await query.edit_message_text(SALAD_RECIPE, reply_markup=get_back_to_menu_keyboard())
        return


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка текстових повідомлень (введення ключа)"""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Перевіряємо, чи користувач зараз у режимі введення ключа
    if context.user_data.get("awaiting_key"):

        if user_id not in user_sessions:
            user_sessions[user_id] = {"activated": False, "used_key": None}

        session = user_sessions[user_id]

        # Перевірка: чи вже активовано
        if session["activated"]:
            await update.message.reply_text("✅ Ви вже активували ключ.")
            context.user_data["awaiting_key"] = False
            return

        # Перевірка формату ключа
        key_input = text.upper().strip()
        if key_input not in VALID_KEYS:
            await update.message.reply_text(
                "❌ Невірний ключ. Спробуйте ще раз або поверніться назад.",
                reply_markup=get_enter_key_keyboard()
            )
            return

        # Перевірка: чи ключ вже використано кимось іншим
        key_already_used = any(
            s.get("used_key") == key_input
            for uid, s in user_sessions.items()
            if s.get("activated") and uid != user_id
        )

        if key_already_used:
            await update.message.reply_text(
                "❌ Цей ключ вже було використано іншим користувачем.",
                reply_markup=get_enter_key_keyboard()
            )
            return

        # Успішна активація
        session["activated"] = True
        session["used_key"] = key_input
        context.user_data["awaiting_key"] = False

        await update.message.reply_text(
            "✅ Ключ успішно активовано! Ласкаво просимо до рецептів.",
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Якщо не в режимі введення ключа — підказка
    await update.message.reply_text(
        "Скористайтеся кнопками в меню або введіть /start.",
        reply_markup=get_start_keyboard()
    )


# --- ЗАПУСК ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
