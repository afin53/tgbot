import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- МІНІ-СЕРВЕР ДЛЯ RENDER (щоб бот працював 24/7) ---
web_app = Flask('')

@web_app.route('/')
def home():
    return "Бот-шпаргалка працює 24/7! 🚀"

def run_web():
    web_app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()
# -----------------------------------------------------

# Головне меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📐 Математика (6 клас)", callback_data="math_menu")],
        [InlineKeyboardButton("📚 Українська мова (НУШ)", callback_data="ukr_menu")],
        [InlineKeyboardButton("📖 Зарубіжна література", callback_data="lit_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привіт! 🤖 Це твій мега-бот шпаргалка для 6 класу.\n"
        "Вибери предмет, щоб відкрити теми:",
        reply_markup=reply_markup
    )

# Меню підкатегорій предметів
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    back_main = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Головне меню", callback_data="main_menu")]])
    
    # --- ГОЛОВНІ МЕНЮ ПРЕДМЕТІВ ---
    if data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📐 Математика (6 клас)", callback_data="math_menu")],
            [InlineKeyboardButton("📚 Українська мова (НУШ)", callback_data="ukr_menu")],
            [InlineKeyboardButton("📖 Зарубіжна література", callback_data="lit_menu")]
        ]
        await query.edit_message_text(text="Вибери предмет:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "math_menu":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Координатна площина і модуль", callback_data="math_1")],
            [InlineKeyboardButton("2️⃣ Звичайні дроби (додавання/віднімання)", callback_data="math_2")],
            [InlineKeyboardButton("3️⃣ Множення і ділення дробів", callback_data="math_3")],
            [InlineKeyboardButton("4️⃣ Пропорції та відсотки", callback_data="math_4")],
            [InlineKeyboardButton("5️⃣ Додатні та від'ємні числа", callback_data="math_5")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        await query.edit_message_text(text="📐 **МАТЕМАТИКА:** Вибери тему:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "ukr_menu":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Лексикологія (Синоніми, антоніми)", callback_data="ukr_1")],
            [InlineKeyboardButton("2️⃣ Фразеологізми", callback_data="ukr_2")],
            [InlineKeyboardButton("3️⃣ Будова слова та орфографія", callback_data="ukr_3")],
            [InlineKeyboardButton("4️⃣ Іменник як частина мови", callback_data="ukr_4")],
            [InlineKeyboardButton("5️⃣ Прикметник і Числівник", callback_data="ukr_5")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        await query.edit_message_text(text="📚 **УКРАЇНСЬКА МОВА:** Вибери тему:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "lit_menu":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Біблійні міфи (Каїн та Авель, Всесвітній потоп)", callback_data="lit_1")],
            [InlineKeyboardButton("2️⃣ Гомер «Одіссея» та «Іліада»", callback_data="lit_2")],
            [InlineKeyboardButton("3️⃣ Робінзон Крузо (Даніель Дефо)", callback_data="lit_3")],
            [InlineKeyboardButton("4️⃣ Марк Твен «Пригоди Тома Сойєра»", callback_data="lit_4")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        await query.edit_message_text(text="📖 **ЗАРУБІЖНА ЛІТЕРАТУРА:** Вибери тему:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    # --- ТЕМИ З МАТЕМАТИКИ ---
    elif data == "math_1":
        text = (
            "📐 **Координатна площина і модуль**\n\n"
            "• **Координатна площина** — це дві осі ($X$ — горизонтальна, $Y$ — вертикальна), що перетинаються в точці $0$. Координата записується як $(x; y)$. Спочатку рухаємось по $X$, потім по $Y$.\n"
            "• **Модуль ($|x$)** — відстань від 0 до числа. Модуль **завжди додатний** ($|-7| = 7$).\n"
        )
        back_math = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з математики", callback_data="math_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_math, parse_mode="Markdown")

    elif data == "math_2":
        text = (
            "📐 **Звичайні дроби**\n\n"
            "• Дріб складається з чисельника (знизу/згори? Згори — скільки взяли) та знаменника (знизу — на скільки поділили).\n"
            "• **Додавання і віднімання:** Щоб додати чи відністи дроби, вони **обов'язково повинні мати однаковий знаменник**! Якщо різний — шукаємо спільний знаменник (найменше спільне кратне)."
        )
        back_math = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з математики", callback_data="math_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_math, parse_mode="Markdown")

    elif data == "math_3":
        text = (
            "📐 **Множення і ділення дробів**\n\n"
            "• **Множення:** Множимо чисельник на чисельник, а знаменник на знаменник. Можна скорочувати хрест-на-хрест.\n"
            "• **Ділення:** Щоб поділити один дріб на інший, другий дріб треба «перевернути» (поміняти чисельник і знаменник місцями) і помножити!"
        )
        back_math = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з математики", callback_data="math_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_math, parse_mode="Markdown")

    elif data == "math_4":
        text = (
            "📐 **Пропорції та відсотки**\n\n"
            "• **Пропорція** — це рівність двох відношень ($a:b = c:d$). Основна властивість: добуток крайніх членів дорівнює добутку середніх ($a \\cdot d = b \\cdot c$).\n"
            "• **Відсоток** — це одна сота частина ($1\\% = 0.01$). Щоб знайти відсоток від числа, треба число помножити на дріб або поділити на 100."
        )
        back_math = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з математики", callback_data="math_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_math, parse_mode="Markdown")

    elif data == "math_5":
        text = (
            "📐 **Додатні та від'ємні числа**\n\n"
            "• Це числа з мінусом і плюсом (ціле множиство — цілі числа). \n"
            "• **Додавання:** Якщо знаки однакові — додаємо і залишаємо знак. Якщо різні — віднімаємо від більшого менший і ставимо знак більшого.\n"
            "• **Множення/ділення:** Мінус на мінус дає плюс ($(-2) \\cdot (-3) = 6$)."
        )
        back_math = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з математики", callback_data="math_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_math, parse_mode="Markdown")

    # --- ТЕМИ З УКРАЇНСЬКОЇ МОВИ ---
    elif data == "ukr_1":
        text = (
            "📚 **Лексикологія**\n\n"
            "• **Синоніми** — різні слова з однаковим значенням (говорити — казати).\n"
            "• **Антоніми** — слова з протилежним значенням (добро — зло).\n"
            "• **Омоніми** — слова, однакові за звучанням, але різні за змістом (клас у школі та клас! як вигук)."
        )
        back_ukr = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з мови", callback_data="ukr_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_ukr, parse_mode="Markdown")

    elif data == "ukr_2":
        text = (
            "📚 **Фразеологізми**\n\n"
            "• Це стійкі сполучення слів, які дорівнюють одному за значенням (часто дієслову або прислівнику).\n"
            "• *Приклади:* \n"
            "  - Пекти раків — червоніти (соромитися).\n"
            "  - Кדувити ворана — байдикувати, нічого не робити.\n"
            "  - Зарубати на носі — добре запам'ятати."
        )
        back_ukr = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з мови", callback_data="ukr_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_ukr, parse_mode="Markdown")

    elif data == "ukr_3":
        text = (
            "📚 **Будова слова та правопис**\n\n"
            "• **Складові:** Закінчення (змінювана частина), основа (все без закінчення), корінь (головна частина), префікс (перед коренем), суфікс (після кореня).\n"
            "• **Не з різними частинами мови:** Пишеться разом або окремо залежно від правила (якщо без «не» слово не вживається — пишеться разом: *недовіра*)."
        )
        back_ukr = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з мови", callback_data="ukr_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_ukr, parse_mode="Markdown")

    elif data == "ukr_4":
        text = (
            "📚 **Іменник**\n\n"
            "• Самостійна частина мови, що означає предмет і відповідає на питання *хто? що?*.\n"
            "• Має рід (чоловічий, жіночий, середній, спільний), число (однина, множина) та відмінки (їх 7: Називний, Родовий, Давальний, Знахідний, Орудний, Місцевий, Кличний)."
        )
        back_ukr = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з мови", callback_data="ukr_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_ukr, parse_mode="Markdown")

    elif data == "ukr_5":
        text = (
            "📚 **Прикметник і Числівник**\n\n"
            "• **Прикметник:** ознака предмета (*який? яка? яке?*). Змінюється за родами, числами і відмінками.\n"
            "• **Числівник:** кількість або порядок при лічбі (*скільки? який?*). Бувають кількісні (п'ять) та порядкові (п'ятий)."
        )
        back_ukr = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з мови", callback_data="ukr_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_ukr, parse_mode="Markdown")

    # --- ТЕМИ З ЛІТЕРАТУРИ ---
    elif data == "lit_1":
        text = (
            "📖 **Біблійні міфи**\n\n"
            "• **Каїн та Авель:** Сини Адама. Пастух Авель і хлібороб Каїн принесли жертви Богу. Дар Авеля прийняли, а Каїна — ні через зависть. Каїн убив брата. *Сенс:* поборюйте заздрощі всередині.\n"
            "• **Всесвітній потоп і Ной:** Через розбещеність людей Бог вирішив знищити світ, але Ной був праведним. Він збудував ковчег і врятував родину та тварин кожного виду."
        )
        back_lit = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з літератури", callback_data="lit_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_lit, parse_mode="Markdown")

    elif data == "lit_2":
        text = (
            "📖 **Гомер — «Іліада» та «Одіссея»**\n\n"
            "• Давньогрецькі поеми, що основані на міфах про Троянську війну.\n"
            "• **Іліада:** Розповідає про облогу Трої греками через викрадення красуні Олени троянським принцем Парісом.\n"
            "• **Одіссея:** Пригоди царя Одіссея, який після війни 10 років намагався повернутися додому на острів Ітака, долаючи циклопів та сирен."
        )
        back_lit = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з літератури", callback_data="lit_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_lit, parse_mode="Markdown")

    elif data == "lit_3":
        text = (
            "📖 **Даніель Дефо — «Робінзон Крузо»**\n\n"
            "• Історія про моряка, який через корабельну аварію потрапив на безлюдний острів і прожив там сам 28 років.\n"
            "• *Сенс:* Людина здатна вижити у будь-яких умовах завдяки праці, розуму, силі волі та оптимізму. Знайомство з дикуном П'ятницею вчить дружби і людяності."
        )
        back_lit = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з літератури", callback_data="lit_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_lit, parse_mode="Markdown")

    elif data == "lit_4":
        text = (
            "📖 **Марк Твен — «Пригоди Тома Сойєра»**\n\n"
            "• Повість про вигадливого хлопчика Тома, який живе у містечку на березі Міссісіпі.\n"
            "• Відомий епізод, де він змусив інших хлопчаків фарбувати паркан замість нього, перетворивши покарання на привілей.\n"
            "• *Сенс:* Важливість справжньої дружби, дитячої свободи, щирості та боротьби з лицемірством дорослих."
        )
        back_lit = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 До тем з літератури", callback_data="lit_menu")]])
        await query.edit_message_text(text=text, reply_markup=back_lit, parse_mode="Markdown")

if __name__ == '__main__':
    # Запускаємо веб-сервер для фону
    keep_alive()
    
    # Встав сюди свій токен від BotFather
    app = ApplicationBuilder().token("ВАШ_ТОКЕН_ВІД_BOTFATHER").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Мега-бот шпаргалка запущено успішно!")
    app.run_polling()
