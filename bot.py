#!/usr/bin/env python3
"""
SafeMind Bot - Stay Human in the AI Era
@Mentesegura_bot / @SafeMindBot
Real humans helping real humans protect their jobs from AI.
"""
import os
import json
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="/root/.openclaw/workspace/safemind/bot.log",
)
logger = logging.getLogger(__name__)

# States
LANGUAGE, MENU = range(2)
WORKPLACE_ROLE, WORKPLACE_COMPANY, WORKPLACE_INDUSTRY, WORKPLACE_FEARS, WORKPLACE_TOOLS = range(2, 7)
Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10 = range(7, 17)

# --- Data ---
QUESTIONS = {
    "en": [
        "1/10: How often do you worry that AI will replace your job?\n\n1 - Never\n2 - Rarely\n3 - Sometimes\n4 - Often\n5 - Every day",
        "2/10: How confident are you in your current skills staying relevant?\n\n1 - Very confident\n2 - Somewhat confident\n3 - Neutral\n4 - Somewhat worried\n5 - Very worried",
        "3/10: Have you learned any new AI-related skill in the last 3 months?\n\n1 - Yes, several\n2 - Yes, one\n3 - Planning to\n4 - No, but thinking about it\n5 - No, and not planning",
        "4/10: How often do you check AI news or updates?\n\n1 - Daily, actively\n2 - Weekly\n3 - Monthly\n4 - Only when major news breaks\n5 - Never",
        "5/10: Do you use AI tools in your current work?\n\n1 - Extensively\n2 - Regularly\n3 - Occasionally\n4 - Tried once\n5 - Never",
        "6/10: How replaceable do you feel your role is?\n\n1 - Completely unique\n2 - Mostly unique\n3 - Mixed\n4 - Somewhat replaceable\n5 - Easily replaceable",
        "7/10: How well do you understand what AI can and cannot do in your field?\n\n1 - Deep expertise\n2 - Good understanding\n3 - Basic understanding\n4 - Vague idea\n5 - No idea",
        "8/10: Have you discussed AI concerns with colleagues or mentors?\n\n1 - Often, we strategize together\n2 - Sometimes\n3 - Once or twice\n4 - Only online anonymously\n5 - Never",
        "9/10: How prepared do you feel for the next 5 years of AI evolution?\n\n1 - Very prepared\n2 - Somewhat prepared\n3 - Neutral\n4 - Somewhat unprepared\n5 - Completely unprepared",
        "10/10: If AI took over part of your job tomorrow, how would you feel?\n\n1 - Excited to focus on higher-value work\n2 - Curious to adapt\n3 - Mixed feelings\n4 - Anxious about income\n5 - Terrified",
    ],
    "ru": [
        "1/10: Как часто вы беспокоитесь, что ИИ заменит вашу работу?\n\n1 - Никогда\n2 - Редко\n3 - Иногда\n4 - Часто\n5 - Каждый день",
        "2/10: Насколько вы уверены в актуальности ваших текущих навыков?\n\n1 - Полностью уверен\n2 - Вполне уверен\n3 - Нейтрально\n4 - Немного тревожно\n5 - Очень тревожно",
        "3/10: Выучили ли вы новый навык, связанный с ИИ, за последние 3 месяца?\n\n1 - Да, несколько\n2 - Да, один\n3 - Планирую\n4 - Нет, но думаю\n5 - Нет, и не планирую",
        "4/10: Как часто вы читаете новости об ИИ?\n\n1 - Ежедневно\n2 - Еженедельно\n3 - Ежемесячно\n4 - Только крупные новости\n5 - Никогда",
        "5/10: Используете ли вы ИИ-инструменты в работе?\n\n1 - Постоянно\n2 - Регулярно\n3 - Иногда\n4 - Пробовал раз\n5 - Никогда",
        "6/10: Насколько заменима ваша роль?\n\n1 - Уникальна\n2 - В основном уникальна\n3 - Смешанно\n4 - Отчасти заменима\n5 - Легко заменима",
        "7/10: Насколько вы понимаете, что ИИ может и чего не может в вашей сфере?\n\n1 - Глубокая экспертиза\n2 - Хорошее понимание\n3 - Базовое понимание\n4 - Смутное представление\n5 - Нет понимания",
        "8/10: Обсуждали ли вы тревоги по ИИ с коллегами или менторами?\n\n1 - Часто, стратегизируем\n2 - Иногда\n3 - Раз или два\n4 - Только анонимно онлайн\n5 - Никогда",
        "9/10: Насколько вы готовы к ИИ-эволюции ближайших 5 лет?\n\n1 - Полностью готов\n2 - Достаточно готов\n3 - Нейтрально\n4 - Немного не готов\n5 - Совсем не готов",
        "10/10: Если ИИ возьмет часть вашей работы завтра, как вы почувствуете?\n\n1 - Взволнован, перейду к более важной работе\n2 - Любопытно, адаптируюсь\n3 - Смешанные чувства\n4 - Тревога за доход\n5 - Ужас",
    ],
    "es": [
        "1/10: Con que frecuencia te preocupa que la IA reemplace tu trabajo?\n\n1 - Nunca\n2 - Raramente\n3 - A veces\n4 - Frecuentemente\n5 - Todos los dias",
        "2/10: Que tan confiado estas en que tus habilidades actuales sigan siendo relevantes?\n\n1 - Muy confiado\n2 - Algo confiado\n3 - Neutral\n4 - Algo preocupado\n5 - Muy preocupado",
        "3/10: Has aprendido alguna habilidad relacionada con IA en los ultimos 3 meses?\n\n1 - Si, varias\n2 - Si, una\n3 - Planeando hacerlo\n4 - No, pero pensando en ello\n5 - No, y no planeo",
        "4/10: Con que frecuencia revisas noticias sobre IA?\n\n1 - Diariamente, activamente\n2 - Semanalmente\n3 - Mensualmente\n4 - Solo noticias importantes\n5 - Nunca",
        "5/10: Usas herramientas de IA en tu trabajo actual?\n\n1 - Extensivamente\n2 - Regularmente\n3 - Ocasionalmente\n4 - Probe una vez\n5 - Nunca",
        "6/10: Que tan reemplazable sientes que es tu rol?\n\n1 - Completamente unico\n2 - Mayormente unico\n3 - Mixto\n4 - Algo reemplazable\n5 - Facilmente reemplazable",
        "7/10: Que tan bien entiendes lo que la IA puede y no puede hacer en tu campo?\n\n1 - Experto profundo\n2 - Buen entendimiento\n3 - Entendimiento basico\n4 - Idea vaga\n5 - Ninguna idea",
        "8/10: Has discutido preocupaciones sobre IA con colegas o mentores?\n\n1 - A menudo, estrategizamos juntos\n2 - A veces\n3 - Una o dos veces\n4 - Solo en linea anonimamente\n5 - Nunca",
        "9/10: Que tan preparado te sientes para los proximos 5 anos de evolucion de IA?\n\n1 - Muy preparado\n2 - Algo preparado\n3 - Neutral\n4 - Algo despreparado\n5 - Completamente despreparado",
        "10/10: Si la IA tomara parte de tu trabajo manana, como te sentirias?\n\n1 - Emocionado de enfocarme en trabajo de mayor valor\n2 - Curioso por adaptarme\n3 - Sentimientos mixtos\n4 - Ansioso por ingresos\n5 - Aterrorizado",
    ],
}

RESULTS = {
    "en": {
        "low": {"title": "Risk: Low", "text": "Your AI anxiety is manageable. Keep building skills and stay ahead."},
        "medium": {"title": "Risk: Medium", "text": "You feel the pressure but haven't taken consistent action. Time to build a plan."},
        "high": {"title": "Risk: High", "text": "Your anxiety is affecting your peace of mind. Let's build a survival plan together."},
    },
    "ru": {
        "low": {"title": "Риск: низкий", "text": "Тревога под контролем. Продолжайте развивать навыки и держать руку на пульсе."},
        "medium": {"title": "Риск: средний", "text": "Вы чувствуете давление, но действуете нерегулярно. Пора составить план."},
        "high": {"title": "Риск: высокий", "text": "Тревога мешает жить спокойно. Давайте вместе составим план выживания."},
    },
    "es": {
        "low": {"title": "Riesgo: Bajo", "text": "Tu ansiedad es manejable. Sigue desarrollando habilidades."},
        "medium": {"title": "Riesgo: Medio", "text": "Sientes la presion pero no actuas consistentemente. Es hora de un plan."},
        "high": {"title": "Riesgo: Alto", "text": "Tu ansiedad afecta tu tranquilidad. Construyamos un plan juntos."},
    },
}

WORKPLACE_PROMPTS = {
    "en": {
        "role": "💼 Let's figure out your AI situation.\n\n*What is your job title or role?*\n\n(e.g., Marketing Manager, Software Engineer, Accountant)",
        "company": "Got it.\n\n*What industry is your company in?*\n\n(e.g., Tech, Finance, Healthcare, Retail, Manufacturing)",
        "fears": "Understood.\n\n*What specifically worries you most about AI at work?*\n\n(e.g., 'My company is testing AI tools', 'My manager mentioned automation', 'I don't know which skills to learn')",
        "tools": "Almost done.\n\n*Which AI tools (if any) do you already use?*\n\n(e.g., ChatGPT, Claude, Midjourney, Copilot, None)\n\nType 'None' if you haven't used any.",
    },
    "ru": {
        "role": "💼 Давайте разберем вашу ситуацию с ИИ.\n\n*Какая у вас должность или роль?*\n\n(например, маркетолог, разработчик, бухгалтер)",
        "company": "Понял.\n\n*В какой отрасли ваша компания?*\n\n(например, IT, финансы, медицина, ритейл, производство)",
        "fears": "Понял.\n\n*Что конкретно вас больше всего беспокоит в части ИИ на работе?*\n\n(например, 'Компания тестирует нейросети', 'Начальник говорил об автоматизации', 'Не знаю, какие навыки качать')",
        "tools": "Почти готово.\n\n*Какие ИИ-инструменты (если есть) вы уже используете?*\n\n(например, ChatGPT, Claude, Midjourney, Copilot, никакие)\n\nНапишите 'никакие', если не использовали.",
    },
    "es": {
        "role": "💼 Vamos a analizar tu situacion con IA.\n\n*Cual es tu puesto o rol?*\n\n(ej. Gerente de Marketing, Ingeniero de Software, Contador)",
        "company": "Entendido.\n\n*En que industria esta tu empresa?*\n\n(ej. Tecnologia, Finanzas, Salud, Retail, Manufactura)",
        "fears": "Entendido.\n\n*Que te preocupa especificamente de la IA en el trabajo?*\n\n(ej. 'Mi empresa prueba herramientas de IA', 'Mi jefe menciono automatizacion', 'No se que habilidades aprender')",
        "tools": "Casi listo.\n\n*Que herramientas de IA (si alguna) ya usas?*\n\n(ej. ChatGPT, Claude, Midjourney, Copilot, Ninguna)\n\nEscribe 'Ninguna' si no has usado ninguna.",
    },
}

MAIN_MENU = {
    "en": {
        "text": "🛡️ *SafeMind*\n\nWe're real humans helping you stay employable in the AI era. Not a chatbot. Not algorithms. Just people who get it.\n\nWhat do you need help with?",
        "buttons": [
            [InlineKeyboardButton("💼 Workplace AI Help", callback_data="menu_workplace")],
            [InlineKeyboardButton("🧠 AI Anxiety Check", callback_data="menu_diagnose")],
            [InlineKeyboardButton("👥 Join Community", url="https://t.me/SafeMindCommunity")],
            [InlineKeyboardButton("🧘 Book with Dr. Elena", callback_data="menu_book")],
        ],
    },
    "ru": {
        "text": "🛡️ *SafeMind*\n\nМы - реальные люди, которые помогают оставаться востребованными в эпоху ИИ. Не чат-бот. Не алгоритмы. Просто люди, которые понимают.\n\nС чем нужна помощь?",
        "buttons": [
            [InlineKeyboardButton("💼 Помощь с ИИ на работе", callback_data="menu_workplace")],
            [InlineKeyboardButton("🧠 Проверить тревогу от ИИ", callback_data="menu_diagnose")],
            [InlineKeyboardButton("👥 Присоединиться к сообществу", url="https://t.me/SafeMindCommunity")],
            [InlineKeyboardButton("🧘 Записаться к др. Елене", callback_data="menu_book")],
        ],
    },
    "es": {
        "text": "🛡️ *SafeMind*\n\nSomos personas reales que te ayudan a mantenerte empleable en la era de la IA. No un chatbot. No algoritmos. Solo gente que entiende.\n\nEn que necesitas ayuda?",
        "buttons": [
            [InlineKeyboardButton("💼 Ayuda con IA en el trabajo", callback_data="menu_workplace")],
            [InlineKeyboardButton("🧠 Evaluar ansiedad por IA", callback_data="menu_diagnose")],
            [InlineKeyboardButton("👥 Unirse a la comunidad", url="https://t.me/SafeMindCommunity")],
            [InlineKeyboardButton("🧘 Agendar con Dra. Elena", callback_data="menu_book")],
        ],
    },
}

SURVIVAL_GUIDES = {
    "en": (
        "🔴 *Let's build your survival plan.*\n\n"
        "Here are 5 things you can do *this week*:\n\n"
        "1️⃣ *Document what only YOU can do* - judgment calls, relationships, creative leaps that AI can't replicate.\n\n"
        "2️⃣ *Master one AI tool* - don't compete with AI, use it. Pick ONE: ChatGPT, Claude, or Copilot. Spend 30 min/day for 7 days.\n\n"
        "3️⃣ *Shift upstream* - AI does tasks. Humans set direction, negotiate, empathize. Move from execution to strategy.\n\n"
        "4️⃣ *Build a human brand* - be the person colleagues trust, not just a function. Write, speak, mentor.\n\n"
        "5️⃣ *Talk to your manager* - ask: 'What parts of my role are hardest to automate?' Double down on those.\n\n"
        "🎯 *Want a personalized 30-day plan?* Get the full AI Work Audit on our site."
    ),
    "ru": (
        "🔴 *Давайте составим ваш план выживания.*\n\n"
        "Вот 5 вещей, которые вы можете сделать *уже на этой неделе*:\n\n"
        "1️⃣ *Зафиксируйте, что умеете ТОЛЬКО вы* - решения на опыте, отношения, творческие прыжки, которые ИИ не скопирует.\n\n"
        "2️⃣ *Освойте один ИИ-инструмент* - не конкурируйте с ИИ, используйте его. Выберите ОДИН: ChatGPT, Claude или Copilot. 30 минут в день, 7 дней.\n\n"
        "3️⃣ *Двигайтесь выше по течению* - ИИ выполняет задачи. Люди задают направление, ведут переговоры, эмпатизируют. Переходите от исполнения к стратегии.\n\n"
        "4️⃣ *Создайте человеческий бренд* - будьте человеком, которому доверяют коллеги, а не просто функцией. Пишите, выступайте, менторьте.\n\n"
        "5️⃣ *Поговорите с руководителем* - спросите: 'Какие части моей роли сложнее всего автоматизировать?' Усильте усилия там.\n\n"
        "🎯 *Нужен персональный 30-дневный план?* Получите полный аудит ИИ для вашей работы на нашем сайте."
    ),
    "es": (
        "🔴 *Construyamos tu plan de supervivencia.*\n\n"
        "Aqui hay 5 cosas que puedes hacer *esta semana*:\n\n"
        "1️⃣ *Documenta lo que SOLO TU puedes hacer* - decisiones basadas en experiencia, relaciones, saltos creativos que la IA no replica.\n\n"
        "2️⃣ *Domina una herramienta de IA* - no compitas con IA, usala. Elige UNA: ChatGPT, Claude o Copilot. 30 min/dia por 7 dias.\n\n"
        "3️⃣ *Muévete hacia arriba* - la IA hace tareas. Los humanos establecen direccion, negocian, empatizan. Pasa de ejecucion a estrategia.\n\n"
        "4️⃣ *Construye una marca humana* - se la persona en quien confian colegas, no solo una funcion. Escribe, habla, mentoriza.\n\n"
        "5️⃣ *Habla con tu jefe* - pregúntale: 'Que partes de mi rol son mas dificiles de automatizar?' Duplica esfuerzos ahi.\n\n"
        "🎯 *Quieres un plan personal de 30 dias?* Obtén la auditoria completa de IA para tu trabajo en nuestro sitio."
    ),
}

# --- Helpers ---

def save_record(record: dict):
    save_dir = "/root/.openclaw/workspace/safemind/data"
    os.makedirs(save_dir, exist_ok=True)
    with open(f"{save_dir}/records.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "en")


# --- Command handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} started bot")

    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Русский", callback_data="lang_ru"),
            InlineKeyboardButton("Espanol", callback_data="lang_es"),
        ]
    ]
    await update.message.reply_text(
        "🛡️ *SafeMind Bot*\nStay Human in the AI Era.\n\nChoose your language:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return LANGUAGE


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    texts = {
        "en": "🧠 *SafeMind*\n\n/start - Main menu\n/diagnose - AI Anxiety Check (10 questions)\n/workplace - Workplace AI Help\n/help - This message\n\nReal humans. Real support. Zero bots.",
        "ru": "🧠 *SafeMind*\n\n/start - Главное меню\n/diagnose - Проверить тревогу от ИИ (10 вопросов)\n/workplace - Помощь с ИИ на работе\n/help - Это сообщение\n\nРеальные люди. Реальная поддержка. Ноль ботов.",
        "es": "🧠 *SafeMind*\n\n/start - Menu principal\n/diagnose - Evaluar ansiedad por IA (10 preguntas)\n/workplace - Ayuda con IA en el trabajo\n/help - Este mensaje\n\nPersonas reales. Apoyo real. Cero bots.",
    }
    await update.message.reply_text(texts.get(lang, texts["en"]), parse_mode="Markdown")


async def diagnose_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if "lang" not in context.user_data:
        await update.message.reply_text("Please /start first to choose language.")
        return ConversationHandler.END
    context.user_data["answers"] = []
    context.user_data["question_idx"] = 0
    await update.message.reply_text(QUESTIONS[lang][0])
    return Q1


async def workplace_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    if "lang" not in context.user_data:
        await update.message.reply_text("Please /start first to choose language.")
        return ConversationHandler.END
    context.user_data["workplace"] = {}
    await update.message.reply_text(WORKPLACE_PROMPTS[lang]["role"], parse_mode="Markdown")
    return WORKPLACE_ROLE


# --- Menu handlers ---

async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang
    await show_main_menu(query, context)
    return MENU


async def show_main_menu(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    menu = MAIN_MENU[lang]
    await query.edit_message_text(
        menu["text"],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(menu["buttons"]),
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    lang = get_lang(context)

    if action == "menu_workplace":
        context.user_data["workplace"] = {}
        await query.edit_message_text(WORKPLACE_PROMPTS[lang]["role"], parse_mode="Markdown")
        return WORKPLACE_ROLE

    elif action == "menu_diagnose":
        context.user_data["answers"] = []
        context.user_data["question_idx"] = 0
        await query.edit_message_text(QUESTIONS[lang][0])
        return Q1

    elif action == "menu_book":
        texts = {
            "en": "🧘‍♀️ *Book with Dr. Elena*\n\nComing soon. Paid therapy sessions will be available here.\n\nFor now, join our free community for peer support.",
            "ru": "🧘‍♀️ *Запись к др. Елене*\n\nСкоро запуск. Платные терапевтические сессии будут доступны здесь.\n\nА пока присоединяйтесь к нашему бесплатному сообществу за поддержкой сверстников.",
            "es": "🧘‍♀️ *Agendar con Dra. Elena*\n\nProximamente. Las sesiones de terapia pagadas estaran disponibles aqui.\n\nPor ahora, unete a nuestra comunidad gratuita para apoyo entre pares.",
        }
        keyboard = [[InlineKeyboardButton("Back", callback_data="menu_back")]]
        await query.edit_message_text(texts[lang], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return MENU

    elif action == "menu_back":
        await show_main_menu(query, context)
        return MENU

    return MENU


# --- Workplace conversation ---

async def handle_workplace_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data["workplace"]["role"] = update.message.text.strip()
    await update.message.reply_text(WORKPLACE_PROMPTS[lang]["company"], parse_mode="Markdown")
    return WORKPLACE_COMPANY


async def handle_workplace_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data["workplace"]["company"] = update.message.text.strip()
    await update.message.reply_text(WORKPLACE_PROMPTS[lang]["fears"], parse_mode="Markdown")
    return WORKPLACE_FEARS


async def handle_workplace_fears(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data["workplace"]["fears"] = update.message.text.strip()
    await update.message.reply_text(WORKPLACE_PROMPTS[lang]["tools"], parse_mode="Markdown")
    return WORKPLACE_TOOLS


async def handle_workplace_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data["workplace"]["tools"] = update.message.text.strip()
    wp = context.user_data["workplace"]

    # Build personalized response
    role = wp.get("role", "")
    fears = wp.get("fears", "").lower()
    tools = wp.get("tools", "").lower()

    # Detect patterns
    high_risk_keywords = ["automate", "replace", "layoff", "fired", "сократ", "замен", "увол", "automatizar", "despedir"]
    is_high_risk = any(k in fears for k in high_risk_keywords)

    no_tools = tools in ["none", "никакие", "ninguna", "no", "нет"]

    if is_high_risk:
        guide_key = "high_risk"
    elif no_tools:
        guide_key = "no_tools"
    else:
        guide_key = "general"

    responses = {
        "en": {
            "high_risk": (
                f"⚠️ *Your situation needs immediate attention.*\n\n"
                f"Role: *{role}*\n\n"
                f"Your company is already moving on AI. Here's what to do *this week*:\n\n"
                f"1. *Schedule a 1:1 with your manager* - ask directly: 'How is AI affecting our team? What's the timeline?'\n"
                f"2. *Identify your irreplaceable tasks* - the ones requiring judgment, relationships, creativity. Double down on those.\n"
                f"3. *Learn ONE tool in 7 days* - pick ChatGPT or Claude. 30 min/day. Document what you learn.\n"
                f"4. *Start an 'AI initiative' memo* - suggest ONE way AI could help your team. Position yourself as the person who *understands* AI, not fears it.\n\n"
                f"🎯 *Need a full 30-day emergency plan?* Get the AI Work Audit on our site."
            ),
            "no_tools": (
                f"📊 *Quick assessment for {role}:*\n\n"
                f"You haven't used AI tools yet - that's actually common, but it's becoming a liability. Here's your starter kit:\n\n"
                f"1. *ChatGPT* - for writing, analysis, brainstorming. Start with 1 task/day you normally do manually.\n"
                f"2. *Claude* - for longer documents, coding help, research. Great for deep work.\n"
                f"3. *Perplexity* - for staying updated on your industry without drowning in news.\n\n"
                f"*This week's challenge:* Use ChatGPT for ONE real work task. Doesn't matter if it's 'perfect' - just get started.\n\n"
                f"🎯 *Want a personalized tool list for your exact role?* Check out our AI Tool Audit."
            ),
            "general": (
                f"✅ *Good news: you're already thinking about this.*\n\n"
                f"Role: *{role}*\nTools you're using: {wp.get('tools', 'none')}\n\n"
                f"Here's your next step:\n\n"
                f"1. *Audit your tasks* - list everything you do in a week. Mark which ones AI could do vs which require YOU.\n"
                f"2. *Automate the boring stuff* - use AI for repetitive tasks. Free up time for strategic work.\n"
                f"3. *Become the 'AI person'* - share what you learn with colleagues. Become indispensable as the bridge between humans and AI.\n\n"
                f"🎯 *Want the full AI Work Plan tailored to {role}?* Visit our site."
            ),
        },
        "ru": {
            "high_risk": (
                f"⚠️ *Ваша ситуация требует немедленного внимания.*\n\n"
                f"Роль: *{role}*\n\n"
                f"Ваша компания уже движется в сторону ИИ. Вот что сделать *на этой неделе*:\n\n"
                f"1. *Назначьте 1:1 с руководителем* - спросите прямо: 'Как ИИ влияет на нашу команду? Какие сроки?'\n"
                f"2. *Определите незаменимые задачи* - те, что требуют суждения, отношений, креативности. Усильте их.\n"
                f"3. *Выучите ОДИН инструмент за 7 дней* - ChatGPT или Claude. 30 минут в день. Фиксируйте, что узнали.\n"
                f"4. *Начните мемо 'Инициатива ИИ'* - предложите ОДИН способ, как ИИ может помочь команде. Позиционируйте себя как человека, который *понимает* ИИ, а не боится.\n\n"
                f"🎯 *Нужен полный 30-дневный экстренный план?* Получите аудит ИИ для вашей работы на нашем сайте."
            ),
            "no_tools": (
                f"📊 *Быстрая оценка для {role}:*\n\n"
                f"Вы еще не использовали ИИ-инструменты - это нормально, но становится риском. Вот ваш стартовый набор:\n\n"
                f"1. *ChatGPT* - для письма, анализа, мозгового штурма. Начните с 1 задачи в день, которую обычно делаете вручную.\n"
                f"2. *Claude* - для длинных документов, помощи в коде, исследований. Отличен для глубокой работы.\n"
                f"3. *Perplexity* - чтобы быть в курсе индустрии без потока новостей.\n\n"
                f"*Челлендж на неделю:* Используйте ChatGPT для ОДНОЙ реальной рабочей задачи. Не важно, 'идеально' ли - просто начните.\n\n"
                f"🎯 *Хотите персональный список инструментов для вашей роли?* Смотрите наш AI Tool Audit."
            ),
            "general": (
                f"✅ *Хорошая новость: вы уже думаете об этом.*\n\n"
                f"Роль: *{role}*\nИнструменты: {wp.get('tools', 'никакие')}\n\n"
                f"Ваш следующий шаг:\n\n"
                f"1. *Аудит задач* - перечислите всё, что делаете за неделю. Отметьте, что может ИИ, а что требует именно ВАС.\n"
                f"2. *Автоматизируйте скучное* - используйте ИИ для рутины. Освободите время для стратегии.\n"
                f"3. *Станьте 'ИИ-человеком'* - делитесь знаниями с коллегами. Станьте незаменимым мостом между людьми и ИИ.\n\n"
                f"🎯 *Нужен полный план ИИ для роли {role}?* Заходите на сайт."
            ),
        },
        "es": {
            "high_risk": (
                f"⚠️ *Tu situacion necesita atencion inmediata.*\n\n"
                f"Rol: *{role}*\n\n"
                f"Tu empresa ya se esta moviendo hacia IA. Esto es lo que hacer *esta semana*:\n\n"
                f"1. *Agenda 1:1 con tu jefe* - pregunta directamente: 'Como esta afectando la IA a nuestro equipo? Cual es el cronograma?'\n"
                f"2. *Identifica tus tareas irremplazables* - las que requieren juicio, relaciones, creatividad. Duplica esfuerzos ahi.\n"
                f"3. *Aprende UNA herramienta en 7 dias* - ChatGPT o Claude. 30 min/dia. Documenta lo que aprendes.\n"
                f"4. *Inicia un memo 'Iniciativa IA'* - sugiere UNA forma en que IA podria ayudar a tu equipo. Posicionate como la persona que *entiende* IA, no la que teme.\n\n"
                f"🎯 *Necesitas un plan de emergencia de 30 dias?* Obtén la Auditoria IA en nuestro sitio."
            ),
            "no_tools": (
                f"📊 *Evaluacion rapida para {role}:*\n\n"
                f"Aun no usas herramientas de IA - eso es comun, pero se esta convirtiendo en un riesgo. Tu kit de inicio:\n\n"
                f"1. *ChatGPT* - para escribir, analizar, brainstorming. Empieza con 1 tarea/dia que normalmente haces manualmente.\n"
                f"2. *Claude* - para documentos largos, ayuda con codigo, investigacion. Excelente para trabajo profundo.\n"
                f"3. *Perplexity* - para mantenerte actualizado en tu industria sin ahogarte en noticias.\n\n"
                f"*Desafio de esta semana:* Usa ChatGPT para UNA tarea real de trabajo. No importa si es 'perfecto' - solo empieza.\n\n"
                f"🎯 *Quieres una lista personalizada de herramientas para tu rol?* Revisa nuestra Auditoria de Herramientas IA."
            ),
            "general": (
                f"✅ *Buenas noticias: ya estas pensando en esto.*\n\n"
                f"Rol: *{role}*\nHerramientas: {wp.get('tools', 'ninguna')}\n\n"
                f"Tu siguiente paso:\n\n"
                f"1. *Audita tus tareas* - lista todo lo que haces en una semana. Marca lo que IA podria hacer vs lo que requiere TI.\n"
                f"2. *Automatiza lo aburrido* - usa IA para tareas repetitivas. Libera tiempo para trabajo estrategico.\n"
                f"3. *Conviertete en la persona de IA* - comparte lo que aprendes con colegas. Vuelvete indispensable como puente entre humanos e IA.\n\n"
                f"🎯 *Quieres el Plan Completo de IA adaptado a {role}?* Visita nuestro sitio."
            ),
        },
    }

    response = responses[lang][guide_key]

    # Save record
    user = update.effective_user
    save_record({
        "type": "workplace",
        "user_id": user.id,
        "username": user.username,
        "lang": lang,
        "role": wp.get("role"),
        "company": wp.get("company"),
        "fears": wp.get("fears"),
        "tools": wp.get("tools"),
        "guide_key": guide_key,
        "date": datetime.now().isoformat(),
    })

    keyboard = [
        [InlineKeyboardButton("Get Full AI Work Plan", url="https://kimicito.github.io/safemind-landing/")],
        [InlineKeyboardButton("Back to Menu", callback_data="menu_back")],
    ] if lang == "en" else [
        [InlineKeyboardButton("Полный план по ИИ", url="https://kimicito.github.io/safemind-landing/")],
        [InlineKeyboardButton("Назад в меню", callback_data="menu_back")],
    ] if lang == "ru" else [
        [InlineKeyboardButton("Plan Completo de IA", url="https://kimicito.github.io/safemind-landing/")],
        [InlineKeyboardButton("Volver al menu", callback_data="menu_back")],
    ]

    await update.message.reply_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return MENU


# --- Diagnosis conversation ---

async def handle_diagnosis_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lang = get_lang(context)
    answers = context.user_data.get("answers", [])

    try:
        score = int(text)
        if score < 1 or score > 5:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "Reply with 1-5 / Ответьте цифрой 1-5 / Responde 1-5"
        )
        return len(answers) + 7  # Q1=7, Q2=8, etc.

    answers.append(score)
    context.user_data["answers"] = answers

    if len(answers) < 10:
        await update.message.reply_text(QUESTIONS[lang][len(answers)])
        return len(answers) + 7
    else:
        total = sum(answers)
        if total <= 20:
            level = "low"
        elif total <= 35:
            level = "medium"
        else:
            level = "high"

        result = RESULTS[lang][level]

        user = update.effective_user
        save_record({
            "type": "diagnosis",
            "user_id": user.id,
            "username": user.username,
            "lang": lang,
            "score": total,
            "level": level,
            "answers": answers,
            "date": datetime.now().isoformat(),
        })

        keyboard = [
            [InlineKeyboardButton("Join SafeMind", url="https://kimicito.github.io/safemind-landing/")],
            [InlineKeyboardButton("Back to Menu", callback_data="menu_back")],
        ] if lang == "en" else [
            [InlineKeyboardButton("Присоединиться", url="https://kimicito.github.io/safemind-landing/")],
            [InlineKeyboardButton("Назад в меню", callback_data="menu_back")],
        ] if lang == "ru" else [
            [InlineKeyboardButton("Unirse", url="https://kimicito.github.io/safemind-landing/")],
            [InlineKeyboardButton("Volver", callback_data="menu_back")],
        ]

        await update.message.reply_text(
            f"*Score: {total}/50*\n\n{result['title']}\n\n{result['text']}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU


# --- Fallbacks ---

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Type /start to restart.")
    return ConversationHandler.END


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_menu(query, context)
    return MENU


# --- Main ---

def main():
    application = Application.builder().token(TOKEN).build()

    # Menu callbacks (outside conversation)
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^menu_back$"))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))

    # Main conversation
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("diagnose", diagnose_cmd),
            CommandHandler("workplace", workplace_cmd),
            CallbackQueryHandler(lang_selected, pattern="^lang_"),
        ],
        states={
            LANGUAGE: [CallbackQueryHandler(lang_selected, pattern="^lang_")],
            MENU: [CallbackQueryHandler(menu_callback, pattern="^menu_")],
            WORKPLACE_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workplace_role)],
            WORKPLACE_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workplace_company)],
            WORKPLACE_FEARS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workplace_fears)],
            WORKPLACE_TOOLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workplace_tools)],
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
            Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_diagnosis_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_cmd))

    logger.info("SafeMind Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
