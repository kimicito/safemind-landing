#!/usr/bin/env python3
"""
SafeMind Bot — AI Anxiety Diagnosis
@Mentesegura_bot
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

# States for ConversationHandler
LANGUAGE, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, EMAIL = range(12)

QUESTIONS = {
    "en": [
        "1/10: How often do you worry that AI will replace your job?\n\n1 — Never\n2 — Rarely\n3 — Sometimes\n4 — Often\n5 — Every day",
        "2/10: How confident are you in your current skills staying relevant?\n\n1 — Very confident\n2 — Somewhat confident\n3 — Neutral\n4 — Somewhat worried\n5 — Very worried",
        "3/10: Have you learned any new AI-related skill in the last 3 months?\n\n1 — Yes, several\n2 — Yes, one\n3 — Planning to\n4 — No, but thinking about it\n5 — No, and not planning",
        "4/10: How often do you check AI news or updates?\n\n1 — Daily, actively\n2 — Weekly\n3 — Monthly\n4 — Only when major news breaks\n5 — Never",
        "5/10: Do you use AI tools in your current work?\n\n1 — Extensively\n2 — Regularly\n3 — Occasionally\n4 — Tried once\n5 — Never",
        "6/10: How replaceable do you feel your role is?\n\n1 — Completely unique\n2 — Mostly unique\n3 — Mixed\n4 — Somewhat replaceable\n5 — Easily replaceable",
        "7/10: How well do you understand what AI can and cannot do in your field?\n\n1 — Deep expertise\n2 — Good understanding\n3 — Basic understanding\n4 — Vague idea\n5 — No idea",
        "8/10: Have you discussed AI concerns with colleagues or mentors?\n\n1 — Often, we strategize together\n2 — Sometimes\n3 — Once or twice\n4 — Only online anonymously\n5 — Never",
        "9/10: How prepared do you feel for the next 5 years of AI evolution?\n\n1 — Very prepared\n2 — Somewhat prepared\n3 — Neutral\n4 — Somewhat unprepared\n5 — Completely unprepared",
        "10/10: If AI took over part of your job tomorrow, how would you feel?\n\n1 — Excited to focus on higher-value work\n2 — Curious to adapt\n3 — Mixed feelings\n4 — Anxious about income\n5 — Terrified",
    ],
    "ru": [
        "1/10: Как часто вы беспокоитесь, что ИИ заменит вашу работу?\n\n1 — Никогда\n2 — Редко\n3 — Иногда\n4 — Часто\n5 — Каждый день",
        "2/10: Насколько вы уверены в актуальности ваших текущих навыков?\n\n1 — Полностью уверен\n2 — Вполне уверен\n3 — Нейтрально\n4 — Немного тревожно\n5 — Очень тревожно",
        "3/10: Выучили ли вы новый навык, связанный с ИИ, за последние 3 месяца?\n\n1 — Да, несколько\n2 — Да, один\n3 — Планирую\n4 — Нет, но думаю\n5 — Нет, и не планирую",
        "4/10: Как часто вы читаете новости об ИИ?\n\n1 — Ежедневно\n2 — Еженедельно\n3 — Ежемесячно\n4 — Только крупные новости\n5 — Никогда",
        "5/10: Используете ли вы ИИ-инструменты в работе?\n\n1 — Постоянно\n2 — Регулярно\n3 — Иногда\n4 — Пробовал раз\n5 — Никогда",
        "6/10: Насколько заменима ваша роль?\n\n1 — Уникальна\n2 — В основном уникальна\n3 — Смешанно\n4 — Отчасти заменима\n5 — Легко заменима",
        "7/10: Насколько вы понимаете, что ИИ может и чего не может в вашей сфере?\n\n1 — Глубокая экспертиза\n2 — Хорошее понимание\n3 — Базовое понимание\n4 — Смутное представление\n5 — Нет понимания",
        "8/10: Обсуждали ли вы тревоги по ИИ с коллегами или менторами?\n\n1 — Часто, стратегизируем\n2 — Иногда\n3 — Раз или два\n4 — Только анонимно онлайн\n5 — Никогда",
        "9/10: Насколько вы готовы к ИИ-эволюции ближайших 5 лет?\n\n1 — Полностью готов\n2 — Достаточно готов\n3 — Нейтрально\n4 — Немного не готов\n5 — Совсем не готов",
        "10/10: Если ИИ возьмёт часть вашей работы завтра, как вы почувствуете?\n\n1 — Взволнован, перейду к более важной работе\n2 — Любопытно, адаптируюсь\n3 — Смешанные чувства\n4 — Тревога за доход\n5 — Ужас",
    ],
    "es": [
        "1/10: ¿Con qué frecuencia te preocupa que la IA reemplace tu trabajo?\n\n1 — Nunca\n2 — Raramente\n3 — A veces\n4 — Frecuentemente\n5 — Todos los días",
        "2/10: ¿Qué tan confiado estás en que tus habilidades actuales sigan siendo relevantes?\n\n1 — Muy confiado\n2 — Algo confiado\n3 — Neutral\n4 — Algo preocupado\n5 — Muy preocupado",
        "3/10: ¿Has aprendido alguna habilidad relacionada con IA en los últimos 3 meses?\n\n1 — Sí, varias\n2 — Sí, una\n3 — Planeando hacerlo\n4 — No, pero pensando en ello\n5 — No, y no planeo",
        "4/10: ¿Con qué frecuencia revisas noticias sobre IA?\n\n1 — Diariamente, activamente\n2 — Semanalmente\n3 — Mensualmente\n4 — Solo noticias importantes\n5 — Nunca",
        "5/10: ¿Usas herramientas de IA en tu trabajo actual?\n\n1 — Extensivamente\n2 — Regularmente\n3 — Ocasionalmente\n4 — Probé una vez\n5 — Nunca",
        "6/10: ¿Qué tan reemplazable sientes que es tu rol?\n\n1 — Completamente único\n2 — Mayormente único\n3 — Mixto\n4 — Algo reemplazable\n5 — Fácilmente reemplazable",
        "7/10: ¿Qué tan bien entiendes lo que la IA puede y no puede hacer en tu campo?\n\n1 — Experto profundo\n2 — Buen entendimiento\n3 — Entendimiento básico\n4 — Idea vaga\n5 — Ninguna idea",
        "8/10: ¿Has discutido preocupaciones sobre IA con colegas o mentores?\n\n1 — A menudo, estrategizamos juntos\n2 — A veces\n3 — Una o dos veces\n4 — Solo en línea anónimamente\n5 — Nunca",
        "9/10: ¿Qué tan preparado te sientes para los próximos 5 años de evolución de IA?\n\n1 — Muy preparado\n2 — Algo preparado\n3 — Neutral\n4 — Algo despreparado\n5 — Completamente despreparado",
        "10/10: Si la IA tomara parte de tu trabajo mañana, ¿cómo te sentirías?\n\n1 — Emocionado de enfocarme en trabajo de mayor valor\n2 — Curioso por adaptarme\n3 — Sentimientos mixtos\n4 — Ansioso por ingresos\n5 — Aterrorizado",
    ],
}

RESULTS = {
    "en": {
        "low": {
            "title": "🟢 Low Risk — You're in Control",
            "text": "Your AI anxiety is manageable. You actively engage with AI trends, build skills, and adapt.\n\n🎯 Recommendation: Maintain momentum. Consider becoming an AI mentor for others.",
        },
        "medium": {
            "title": "🟡 Medium Risk — Time to Act",
            "text": "You feel the pressure but haven't taken consistent action. The good news: it's not too late.\n\n🎯 Recommendation: Pick ONE AI skill to learn this month. Block 2 hours/week. Join our SafeMind community.",
        },
        "high": {
            "title": "🔴 High Risk — Let's Fix This",
            "text": "Your anxiety is affecting your peace of mind. But anxiety without action is just fear.\n\n🎯 Recommendation: Start with our free Human AI Concierge. Get weekly guidance, answers, and a plan. You don't have to face this alone.",
        },
    },
    "ru": {
        "low": {
            "title": "🟢 Низкий риск — Вы в контроле",
            "text": "Ваша тревога от ИИ под контролем. Вы активно следите за трендами, развиваете навыки, адаптируетесь.\n\n🎯 Рекомендация: Поддерживайте темп. Подумайте о том, чтобы стать ментором по ИИ для других.",
        },
        "medium": {
            "title": "🟡 Средний риск — Пора действовать",
            "text": "Вы чувствуете давление, но не предпринимаете системных шагов. Хорошая новость: ещё не поздно.\n\n🎯 Рекомендация: Выберите ОДИН навык ИИ для изучения в этом месяце. Выделите 2 часа/неделю. Присоединяйтесь к сообществу SafeMind.",
        },
        "high": {
            "title": "🔴 Высокий риск — Давайте исправим",
            "text": "Тревога мешает жить спокойно. Но тревога без действий — это просто страх.\n\n🎯 Рекомендация: Начните с Human AI Concierge ($99/мес). Получайте еженедельные рекомендации, ответы на вопросы и план. Вам не нужно справляться с этим в одиночку.",
        },
    },
    "es": {
        "low": {
            "title": "🟢 Riesgo Bajo — Estás en control",
            "text": "Tu ansiedad por IA es manejable. Participas activamente en tendencias de IA, desarrollas habilidades y te adaptas.\n\n🎯 Recomendación: Mantén el impulso. Considera ser mentor de IA para otros.",
        },
        "medium": {
            "title": "🟡 Riesgo Medio — Es hora de actuar",
            "text": "Sientes la presión pero no has tomado acción consistente. La buena noticia: aún no es tarde.\n\n🎯 Recomendación: Elige UNA habilidad de IA para aprender este mes. Bloquea 2 horas/semana. Únete a nuestra comunidad SafeMind.",
        },
        "high": {
            "title": "🔴 Riesgo Alto — Vamos a solucionarlo",
            "text": "Tu ansiedad está afectando tu tranquilidad. Pero ansiedad sin acción es solo miedo.\n\n🎯 Recomendación: Empieza con nuestro Concierge Humano IA ($99/mes). Recibe orientación semanal, respuestas y un plan. No tienes que enfrentar esto solo.",
        },
    },
}

# --- "I'm definitely being replaced" survival guide ---
SURVIVAL_INSTRUCTIONS = {
    "en": (
        "🔴 *You feel AI is coming for your job? Let's build a survival plan.*\n\n"
        "Here are 5 immediate actions you can take *this week*:\n\n"
        "1️⃣ *Document what only YOU can do* — the judgment calls, relationships, creative leaps that AI can't replicate.\n\n"
        "2️⃣ *Become the AI operator* — don't compete with AI, master it. Learn ONE tool that amplifies your work (ChatGPT, Claude, Midjourney, etc.).\n\n"
        "3️⃣ *Shift from execution to strategy* — AI does tasks. Humans set direction, negotiate, empathize, decide. Move upstream.\n\n"
        "4️⃣ *Build a visible human brand* — be the person clients/colleagues trust, not just a function. Write, speak, mentor.\n\n"
        "5️⃣ *Talk to your manager NOW* — ask: 'What parts of my role are hardest to automate?' Then double down on those.\n\n"
        "🎯 *Next step:* Book a free strategy session with our Human AI Concierge to build your personal 90-day plan.\n\n"
        "You are not replaceable. You just need to prove it. 💪"
    ),
    "ru": (
        "🔴 *Вы уверены, что ИИ заменит вас? Давайте составим план выживания.*\n\n"
        "Вот 5 действий, которые вы можете сделать *уже на этой неделе*:\n\n"
        "1️⃣ *Зафиксируйте, что умеете ТОЛЬКО вы* — решения на основе опыта, отношения, творческие прыжки, которые ИИ не реплицирует.\n\n"
        "2️⃣ *Станьте оператором ИИ* — не конкурируйте с ИИ, освойте его. Выучите ОДИН инструмент, который усиливает вашу работу (ChatGPT, Claude, Midjourney и т.д.).\n\n"
        "3️⃣ *Переходите от исполнения к стратегии* — ИИ выполняет задачи. Люди задают направление, ведут переговоры, эмпатизируют, принимают решения. Двигайтесь выше по течению.\n\n"
        "4️⃣ *Создайте видимый человеческий бренд* — будьте человеком, которому доверяют клиенты и коллеги, а не просто функцией. Пишите, выступайте, менторьте.\n\n"
        "5️⃣ *Поговорите с руководителем ПРЯМО СЕЙЧАС* — спросите: 'Какие части моей роли сложнее всего автоматизировать?' Удвойте усилия там.\n\n"
        "🎯 *Следующий шаг:* Запишитесь на бесплатную стратегическую сессию с Human AI Concierge, чтобы составить персональный 90-дневный план.\n\n"
        "Вы незаменимы. Нужно только это доказать. 💪"
    ),
    "es": (
        "🔴 *¿Sientes que la IA te reemplazará? Construyamos un plan de supervivencia.*\n\n"
        "Aquí hay 5 acciones inmediatas para *esta semana*:\n\n"
        "1️⃣ *Documenta lo que SOLO TÚ puedes hacer* — las decisiones basadas en experiencia, relaciones, saltos creativos que la IA no puede replicar.\n\n"
        "2️⃣ *Conviértete en operador de IA* — no compitas con IA, domínala. Aprende UNA herramienta que amplifique tu trabajo (ChatGPT, Claude, Midjourney, etc.).\n\n"
        "3️⃣ *Pasa de ejecución a estrategia* — la IA hace tareas. Los humanos establecen dirección, negocian, empatizan, deciden. Muévete hacia arriba.\n\n"
        "4️⃣ *Construye una marca humana visible* — sé la persona en quien clientes y colegas confían, no solo una función. Escribe, habla, mentoriza.\n\n"
        "5️⃣ *Habla con tu jefe AHORA* — pregúntale: '¿Qué partes de mi rol son más difíciles de automatizar?' Duplica esfuerzos ahí.\n\n"
        "🎯 *Siguiente paso:* Agenda una sesión estratégica gratuita con nuestro Concierge Humano IA para construir tu plan personal de 90 días.\n\n"
        "No eres reemplazable. Solo necesitas demostrarlo. 💪"
    ),
}

async def survival_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    text = SURVIVAL_INSTRUCTIONS.get(lang, SURVIVAL_INSTRUCTIONS["en"])
    keyboard = [
        [InlineKeyboardButton("🚀 Join SafeMind", url="https://kimicito.github.io/safemind-landing/")]
    ]
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        ]
    ]
    await update.message.reply_text(
        "🧠 *SafeMind Bot*\n"
        "Stay calm in the AI era.\n\n"
        "Choose your language / Выберите язык / Elige tu idioma:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return LANGUAGE


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    texts = {
        "en": "🧠 *SafeMind Commands*\n\n"
              "/start — Begin diagnosis\n"
              "/diagnose — Start 10-min AI Anxiety Assessment\n"
              "/help — This message\n\n"
              "SafeMind helps you understand and manage AI-related anxiety with a real human partner.",
        "ru": "🧠 *Команды SafeMind*\n\n"
              "/start — Начать диагностику\n"
              "/diagnose — 10-мин оценка тревоги ИИ\n"
              "/help — Это сообщение\n\n"
              "SafeMind помогает понять и управлять тревогой от ИИ с помощью реального человека-партнёра.",
        "es": "🧠 *Comandos SafeMind*\n\n"
              "/start — Comenzar diagnóstico\n"
              "/diagnose — Evaluación de 10 min de ansiedad IA\n"
              "/help — Este mensaje\n\n"
              "SafeMind te ayuda a entender y manejar la ansiedad por IA con un compañero humano real.",
    }
    await update.message.reply_text(texts.get(lang, texts["en"]), parse_mode="Markdown")


async def diagnose_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    context.user_data["answers"] = []
    await update.message.reply_text(QUESTIONS[lang][0])
    return Q1


# --- Conversation handlers ---
async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang

    greetings = {
        "en": "✅ *English selected*\n\nWelcome to SafeMind. I'm here to help you understand your AI anxiety and build a plan.\n\nWhat would you like to do?",
        "ru": "✅ *Выбран русский язык*\n\nДобро пожаловать в SafeMind. Я помогу понять вашу тревогу от ИИ и составить план.\n\nЧто хотите сделать?",
        "es": "✅ *Español seleccionado*\n\nBienvenido a SafeMind. Estoy aquí para ayudarte a entender tu ansiedad por IA y construir un plan.\n\n¿Qué te gustaría hacer?",
    }
    buttons = {
        "en": [
            [InlineKeyboardButton("🧠 Start Free Diagnosis", callback_data="start_diagnose")],
            [InlineKeyboardButton("🔴 AI is replacing me — help", callback_data="survival")],
        ],
        "ru": [
            [InlineKeyboardButton("🧠 Пройти бесплатную диагностику", callback_data="start_diagnose")],
            [InlineKeyboardButton("🔴 Меня точно заменят ИИ — что делать", callback_data="survival")],
        ],
        "es": [
            [InlineKeyboardButton("🧠 Comenzar diagnóstico gratis", callback_data="start_diagnose")],
            [InlineKeyboardButton("🔴 La IA me reemplazará — ayuda", callback_data="survival")],
        ],
    }
    await query.edit_message_text(
        greetings[lang],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons[lang]),
    )
    return ConversationHandler.END


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lang = context.user_data.get("lang", "en")
    answers = context.user_data.get("answers", [])

    # Validate input
    try:
        score = int(text)
        if score < 1 or score > 5:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "❌ Please reply with a number 1–5 / Ответьте цифрой 1–5 / Responde con un número 1–5"
        )
        return len(answers) + 1

    answers.append(score)
    context.user_data["answers"] = answers

    if len(answers) < 10:
        await update.message.reply_text(QUESTIONS[lang][len(answers)])
        return len(answers) + 1
    else:
        # Calculate result
        total = sum(answers)
        if total <= 20:
            level = "low"
        elif total <= 35:
            level = "medium"
        else:
            level = "high"

        result = RESULTS[lang][level]

        # Save to file
        user = update.effective_user
        record = {
            "user_id": user.id,
            "username": user.username,
            "lang": lang,
            "score": total,
            "level": level,
            "answers": answers,
            "date": datetime.now().isoformat(),
        }
        save_dir = "/root/.openclaw/workspace/safemind/data"
        os.makedirs(save_dir, exist_ok=True)
        with open(f"{save_dir}/diagnoses.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        keyboard = [
            [InlineKeyboardButton("🚀 Join SafeMind", url="https://kimicito.github.io/safemind-landing/")]
        ]

        await update.message.reply_text(
            f"🎯 *Your Score: {total}/50*\n\n{result['title']}\n\n{result['text']}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Type /start to restart.")
    return ConversationHandler.END


async def start_diagnose_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    context.user_data["answers"] = []
    await query.edit_message_text(QUESTIONS[lang][0])
    # Return Q1 so ConversationHandler catches next messages
    # But since this is outside ConversationHandler, we need to manually track
    # We'll store state in user_data and use a message handler to continue
    context.user_data["question_idx"] = 0
    await query.message.reply_text(QUESTIONS[lang][0])


# --- Main ---
def main():
    application = Application.builder().token(TOKEN).build()

    # Standalone callback handlers (outside conversation)
    application.add_handler(CallbackQueryHandler(survival_callback, pattern="^survival$"))

    # Conversation for diagnosis
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("diagnose", diagnose_cmd),
            CallbackQueryHandler(lang_selected, pattern="^lang_"),
        ],
        states={
            LANGUAGE: [CallbackQueryHandler(lang_selected, pattern="^lang_")],
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
            Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_cmd))

    logger.info("SafeMind Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
