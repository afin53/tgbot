import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Головне меню з 3 категоріями
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📐 Математика (6 клас)", callback_data="math")],
        [InlineKeyboardButton("📚 Українська мова (НУШ)", callback_data="ukr")],
        [InlineKeyboardButton("📖 Зарубіжна література", callback_data="lit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привіт! 🤖 Це твій бот-шпаргалка для 6 класу.\n"
        "Вибери предмет нижче, щоб згадати найголовніше:",
        reply_markup=reply_markup
    )

# Обробка натискань на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Кнопки для повернення назад
    back_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад до меню", callback_data="main_menu")]])
    
    if data == "math":
        text = (
            "📐 **МАТЕМАТИКА (6 клас)**\n\n"
            "1️⃣ **Координатна площина** — це дві перпендикулярні прямі (осі $X$ та $Y$), які перетинаються в точці $0$ (початок відліку). Кожна точка на ній має свої координати: $(x; y)$. Спершу шукаємо число по осі $X$ (горизонталь), потім по $Y$ (вертикаль).\n\n"
            "2️⃣ **Модуль числа ($|x$)** — це відстань від нуля до заданого числа на координатному промені. Модуль **завжди додатний**! Наприклад: $|-5| = 5$, а $|5| = 5$."
        )
        await query.edit_message_text(text=text, reply_markup=back_keyboard, parse_mode="Markdown")
        
    elif data == "ukr":
        text = (
            "📚 **УКРАЇНСЬКА МОВА (НУШ - головне)**\n\n"
            "1️⃣ **Лексикологія** — це розділ, що вивчає слова. \n"
            "• *Синоніми* — слова, схожі за значенням (рідний — близький).\n"
            "• *Антоніми* — слова з протилежним значенням (день — ніч).\n"
            "• *Омоніми* — слова, однакові за написанням, але різні за змістом (коса — дівоча і коса — інструмент).\n\n"
            "2️⃣ **Частини мови**: діляться на самостійні (іменник, прикметник, дієслово тощо) та службові (прийменник, сполучник, частка)."
        )
        await query.edit_message_text(text=text, reply_markup=back_keyboard, parse_mode="Markdown")
        
    elif data == "lit":
        text = (
            "📖 **ЗАРУБІЖНА ЛІТЕРАТУРА (Біблійні історії)**\n\n"
            "1️⃣ **Каїн та Авель** (Сини Адама і Єви):\n"
            "• *Хто є хто:* Авель був пастухом, а Каїн — хліборобом.\n"
            "• *Суть історії:* Вони принесли дари Богу. Бог прийняв дар Авеля, а дар Каїна — ні (бо той робив це без щирої душі). Через заздрощі Каїн убив свого брата Авеля.\n"
            "• *Сенс:* Історія вчить нас контролювати заздрощі та гнів. Заздрість руйнує людину зсередини і веде до великого гріха."
        )
        await query.edit_message_text(text=text, reply_markup=back_keyboard, parse_mode="Markdown")
        
    elif data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📐 Математика", callback_data="math")],
            [InlineKeyboardButton("📚 Українська мова", callback_data="ukr")],
            [InlineKeyboardButton("📖 Зарубіжна література", callback_data="lit")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Ви повертілися до головного меню. Вибери предмет:",
            reply_markup=reply_markup
        )

if __name__ == '__main__':
    # Встав сюди свій токен від BotFather
    app = ApplicationBuilder().token("8804615504:AAFricacBvBqsk9WfhOki_ZTdFdnx4C4JWE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот-шпаргалка запущено!")
    app.run_polling()
