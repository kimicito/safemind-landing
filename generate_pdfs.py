#!/usr/bin/env python3
"""
Generate SafeMind Lead Magnet PDFs by role
3-5 pages, actionable, no fluff
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register a font that supports Cyrillic
try:
    pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    FONT_NAME = 'DejaVu'
except:
    FONT_NAME = 'Helvetica'

OUTPUT_DIR = "/root/.openclaw/workspace/safemind/pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Role-specific content
CONTENT = {
    "en": {
        "manager": {
            "title": "AI Survival Guide for Managers",
            "subtitle": "7 Days to Become the Leader AI Can't Replace",
            "days": [
                ("Day 1: Audit Your Decision-Making", 
                 "List 10 decisions you made this week. Circle the ones that required judgment, context, and stakeholder management. These are your moat. AI can't navigate office politics or build trust."),
                ("Day 2: Become the AI Translator",
                 "Pick ONE AI tool (ChatGPT or Claude). Spend 30 minutes asking it to analyze a team problem. Your job isn't to know AI. It's to translate AI insights into human action."),
                ("Day 3: Delegate the Routine",
                 "Identify 3 tasks you do weekly that are pure execution (scheduling, reporting, data gathering). Delegate these to AI or junior staff. Free up 4 hours for strategy."),
                ("Day 4: Build Your Human Network",
                 "Schedule 1:1s with 3 people outside your direct team. The manager with the best network survives layoffs. AI can't replicate relationships."),
                ("Day 5: Master the AI Briefing",
                 "Learn to write prompts that get useful answers. Practice: 'Analyze this team performance data and suggest 3 concrete actions.' The manager who can brief AI beats the manager who fears it."),
                ("Day 6: Position Yourself as the AI Champion",
                 "Draft a 1-page memo: 'How AI Could Help Our Team.' Share it with your boss. You become the person who 'gets AI' — not the person replaced by it."),
                ("Day 7: Plan Your Next 30 Days",
                 "Block 2 hours every week for 'AI exploration.' Build a personal learning plan. The managers who survive are the ones who treated AI as a tool, not a threat."),
            ],
            "tools": ["ChatGPT", "Claude", "Notion AI", "Fireflies.ai", "Crystal Knows"],
            "checklist": ["Audit decisions", "Learn 1 AI tool", "Delegate routine", "Build network", "Write AI memo", "Schedule learning time"],
        },
        "marketing": {
            "title": "AI Survival Guide for Marketers",
            "subtitle": "7 Days to Outcreate the Algorithms",
            "days": [
                ("Day 1: Find Your Human Angle",
                 "List 5 campaigns you've run. Identify the insight that came from YOU — not data. AI can generate ads. It can't feel cultural shifts or spot the joke before it trends."),
                ("Day 2: Master AI-Powered Research",
                 "Use Perplexity or ChatGPT to analyze 3 competitors in 30 minutes. AI is your intern for research. You remain the strategist who decides what matters."),
                ("Day 3: Automate the Grunt Work",
                 "Set up AI for: social post scheduling, A/B test analysis, email subject line generation. Save 6 hours/week for creative thinking."),
                ("Day 4: Build a Personal Brand",
                 "Start posting ONE original insight weekly on LinkedIn. AI can't replicate your lived experience. Your personal brand is your unemployment insurance."),
                ("Day 5: Learn Visual AI",
                 "Spend 1 hour with Midjourney or DALL-E. Not to replace designers — to speak their language and prototype faster. The marketer who understands visual AI directs the designer who doesn't."),
                ("Day 6: Run an AI vs Human Test",
                 "Create one campaign element (headline, email, post) yourself and with AI. A/B test them. Document what AI does better and what you do better. Knowledge is armor."),
                ("Day 7: Plan Your AI-Proof Career",
                 "Write down: 'In 2 years, I'll be the person who...' Focus on strategy, brand voice, and customer psychology. These are the last things AI will master."),
            ],
            "tools": ["ChatGPT", "Midjourney", "Perplexity", "Copy.ai", "Sprout Social"],
            "checklist": ["Find human angle", "Master AI research", "Automate grunt work", "Build personal brand", "Learn visual AI", "Run AI vs human test"],
        },
        "developer": {
            "title": "AI Survival Guide for Developers",
            "subtitle": "7 Days to Code What AI Can't",
            "days": [
                ("Day 1: Audit Your Code",
                 "Review your last 5 PRs. Which required architectural decisions? Which were boilerplate? The second category is AI's territory now. Focus on the first."),
                ("Day 2: Master AI Pair Programming",
                 "Use GitHub Copilot for 1 hour. Don't just accept suggestions — critique them. The developer who reviews AI code is more valuable than the one who writes it from scratch."),
                ("Day 3: Learn System Design",
                 "AI generates functions. It doesn't design systems. Spend 2 hours on 'Designing Data-Intensive Applications' or a system design course. This is your new moat."),
                ("Day 4: Build Something AI Can't",
                 "Start a side project that requires domain knowledge your company has. AI can't understand your business context. You can."),
                ("Day 5: Become the AI Integrator",
                 "Learn how to connect AI APIs (OpenAI, Anthropic) to your company's systems. The developer who can integrate AI into products is the last one laid off."),
                ("Day 6: Document Like Your Job Depends on It",
                 "Because it does. AI can't maintain what it doesn't understand. Write architecture decision records (ADRs) for your team's key choices."),
                ("Day 7: Plan Your Specialization",
                 "Pick ONE deep area: security, performance, ML ops, or domain-specific logic. AI is a generalist. Specialists survive."),
            ],
            "tools": ["GitHub Copilot", "Claude", "Cursor", "CodeRabbit", "Sourcegraph"],
            "checklist": ["Audit code", "Master Copilot", "Learn system design", "Build side project", "Learn AI integration", "Write ADRs"],
        },
        "generic": {
            "title": "AI Survival Guide",
            "subtitle": "7 Days to Make Yourself Irreplaceable",
            "days": [
                ("Day 1: Find Your Human Edge",
                 "List 5 things you did at work this week that required judgment, empathy, or creativity. These are your superpowers. AI can't replicate them yet."),
                ("Day 2: Learn ONE AI Tool",
                 "Pick ChatGPT, Claude, or Copilot. Spend 30 minutes using it for ONE real work task. Don't try to master everything. Just get started."),
                ("Day 3: Automate One Task",
                 "Find one repetitive task you do weekly. Use AI to do it in 1/10th the time. Free up time for higher-value work."),
                ("Day 4: Talk to Your Manager",
                 "Ask: 'What parts of my role are hardest to automate?' Then double down on those. This conversation alone makes you more visible and more valuable."),
                ("Day 5: Build a Learning Habit",
                 "Block 30 minutes daily for AI learning. Watch one tutorial. Read one article. Small daily investments compound into expertise."),
                ("Day 6: Join a Community",
                 "Find people in your industry learning AI together. SafeMind's community is one option. The people who survive layoffs have networks."),
                ("Day 7: Write Your 30-Day Plan",
                 "Based on what you learned this week, write specific goals for the next month. Concrete plans beat vague anxiety every time."),
            ],
            "tools": ["ChatGPT", "Claude", "Perplexity", "Notion AI", "Grammarly"],
            "checklist": ["Find human edge", "Learn 1 AI tool", "Automate 1 task", "Talk to manager", "Build learning habit", "Join community"],
        },
    },
    "ru": {
        "manager": {
            "title": "Руководство по выживанию для руководителей",
            "subtitle": "7 дней, чтобы стать лидером, которого ИИ не заменит",
            "days": [
                ("День 1: Аудит ваших решений",
                 "Перечислите 10 решений, которые вы приняли на этой неделе. Обведите те, что требовали суждения, контекста и работы со стейкхолдерами. Это ваш ров. ИИ не умеет управлять офисной политикой и строить доверие."),
                ("День 2: Станьте переводчиком ИИ",
                 "Выберите ОДИН инструмент ИИ (ChatGPT или Claude). Потратьте 30 минут, попросив его проанализировать проблему команды. Ваша работа — не знать ИИ, а переводить инсайты ИИ в человеческие действия."),
                ("День 3: Делегируйте рутину",
                 "Найдите 3 задачи, которые делаете еженедельно и которые — чистое исполнение (планирование, отчёты, сбор данных). Делегируйте их ИИ или младшим сотрудникам. Освободите 4 часа на стратегию."),
                ("День 4: Стройте человеческую сеть",
                 "Назначьте 1:1 с 3 людьми вне вашей прямой команды. Руководитель с лучшей сетью переживает сокращения. ИИ не может реплицировать отношения."),
                ("День 5: Освойте брифинг для ИИ",
                 "Научитесь писать промпты, которые дают полезные ответы. Практика: 'Проанализируй данные по производительности команды и предложи 3 конкретных действия.' Руководитель, который умеет брифовать ИИ, побеждает того, кто его боится."),
                ("День 6: Позиционируйте себя как чемпиона ИИ",
                 "Подготовьте мемо на 1 страницу: 'Как ИИ может помочь нашей команде.' Поделитесь с начальником. Вы становитесь человеком, который 'понимает ИИ' — не тем, кого он заменит."),
                ("День 7: Спланируйте следующие 30 дней",
                 "Заблокируйте 2 часа каждую неделю на 'исследование ИИ.' Составьте план обучения. Руководители, которые выживают — те, кто воспринял ИИ как инструмент, а не угрозу."),
            ],
            "tools": ["ChatGPT", "Claude", "Notion AI", "Fireflies.ai", "Crystal Knows"],
            "checklist": ["Аудит решений", "Выучить 1 инструмент ИИ", "Делегировать рутину", "Построить сеть", "Написать мемо об ИИ", "Запланировать время на обучение"],
        },
        "marketing": {
            "title": "Руководство по выживанию для маркетологов",
            "subtitle": "7 дней, чтобы творить то, что алгоритмы не могут",
            "days": [
                ("День 1: Найдите свой человеческий угол",
                 "Перечислите 5 кампаний, которые запускали. Найдите инсайт, который пришёл от ВАС — не от данных. ИИ может генерировать рекламу. Но он не чувствует культурные сдвиги и не замечает шутку до того, как она станет трендом."),
                ("День 2: Освойте исследования на ИИ",
                 "Используйте Perplexity или ChatGPT, чтобы проанализировать 3 конкурента за 30 минут. ИИ — ваш стажёр для исследований. Вы остаётесь стратегом, который решает, что важно."),
                ("День 3: Автоматизируйте грязную работу",
                 "Настройте ИИ для: планирования постов, анализа A/B тестов, генерации тем писем. Экономьте 6 часов в неделю на креативное мышление."),
                ("День 4: Стройте личный бренд",
                 "Начните публиковать ОДИН оригинальный инсайт еженедельно в LinkedIn. ИИ не может реплицировать ваш жизненный опыт. Ваш личный бренд — ваша страховка от безработицы."),
                ("День 5: Выучите визуальный ИИ",
                 "Потратьте 1 час с Midjourney или DALL-E. Не чтобы заменить дизайнеров — чтобы говорить на их языке и прототипировать быстрее. Маркетолог, который понимает визуальный ИИ, управляет дизайнером, который не понимает."),
                ("День 6: Запустите тест ИИ против человека",
                 "Создайте один элемент кампании (заголовок, письмо, пост) сами и с ИИ. A/B тестируйте. Зафиксируйте, что ИИ делает лучше, а что — вы. Знание — броня."),
                ("День 7: Спланируйте карьеру, защищённую от ИИ",
                 "Напишите: 'Через 2 года я буду человеком, который...' Сфокусируйтесь на стратегии, голосе бренда и психологии клиента. Это последнее, что ИИ освоит."),
            ],
            "tools": ["ChatGPT", "Midjourney", "Perplexity", "Copy.ai", "Sprout Social"],
            "checklist": ["Найти человеческий угол", "Освоить исследования на ИИ", "Автоматизировать грязную работу", "Построить личный бренд", "Выучить визуальный ИИ", "Запустить тест ИИ против человека"],
        },
        "developer": {
            "title": "Руководство по выживанию для разработчиков",
            "subtitle": "7 дней, чтобы писать код, который ИИ не напишет",
            "days": [
                ("День 1: Аудит вашего кода",
                 "Пересмотрите ваши последние 5 PR. Какие требовали архитектурных решений? Какие были шаблонными? Вторая категория — территория ИИ. Фокусируйтесь на первой."),
                ("День 2: Освойте парное программирование с ИИ",
                 "Используйте GitHub Copilot 1 час. Не просто принимайте предложения — критикуйте их. Разработчик, который ревьюит код ИИ, ценнее того, кто пишет с нуля."),
                ("День 3: Выучите проектирование систем",
                 "ИИ генерирует функции. Он не проектирует системы. Потратьте 2 часа на 'Designing Data-Intensive Applications' или курс по проектированию систем. Это ваш новый ров."),
                ("День 4: Соберите то, что ИИ не может",
                 "Начните сайд-проект, который требует доменных знаний вашей компании. ИИ не понимает контекст вашего бизнеса. Вы понимаете."),
                ("День 5: Станьте интегратором ИИ",
                 "Научитесь подключать ИИ API (OpenAI, Anthropic) к системам компании. Разработчик, который может интегрировать ИИ в продукты — последний, кого уволят."),
                ("День 6: Документируйте так, будто от этого зависит работа",
                 "Потому что так и есть. ИИ не может поддерживать то, что не понимает. Пишите ADR (Architecture Decision Records) для ключевых решений команды."),
                ("День 7: Спланируйте специализацию",
                 "Выберите ОДНУ глубокую область: безопасность, производительность, ML ops или доменно-специфичную логику. ИИ — генералист. Специалисты выживают."),
            ],
            "tools": ["GitHub Copilot", "Claude", "Cursor", "CodeRabbit", "Sourcegraph"],
            "checklist": ["Аудит кода", "Освоить Copilot", "Выучить проектирование систем", "Собрать сайд-проект", "Научиться интеграции ИИ", "Писать ADR"],
        },
        "generic": {
            "title": "Руководство по выживанию в эпоху ИИ",
            "subtitle": "7 дней, чтобы сделать себя незаменимым",
            "days": [
                ("День 1: Найдите свою человеческую грань",
                 "Перечислите 5 вещей, которые сделали на работе на этой неделе и которые требовали суждения, эмпатии или креативности. Это ваши суперсилы. ИИ пока не может их реплицировать."),
                ("День 2: Выучите ОДИН инструмент ИИ",
                 "Выберите ChatGPT, Claude или Copilot. Потратьте 30 минут, используя его для ОДНОЙ реальной рабочей задачи. Не пытайтесь освоить всё. Просто начните."),
                ("День 3: Автоматизируйте одну задачу",
                 "Найдите одну повторяющуюся задачу, которую делаете еженедельно. Используйте ИИ, чтобы делать её в 10 раз быстрее. Освободите время для более ценной работы."),
                ("День 4: Поговорите с руководителем",
                 "Спросите: 'Какие части моей роли сложнее всего автоматизировать?' Затем удвойте усилия там. Этот разговор сам по себе делает вас заметнее и ценнее."),
                ("День 5: Выработайте привычку учиться",
                 "Блокируйте 30 минут ежедневно на изучение ИИ. Посмотрите один туториал. Прочитайте одну статью. Маленькие ежедневные инвестиции складываются в экспертизу."),
                ("День 6: Присоединяйтесь к сообществу",
                 "Найдите людей в вашей индустрии, которые вместе изучают ИИ. Сообщество SafeMind — один из вариантов. Люди, которые переживают сокращения, имеют сети."),
                ("День 7: Напишите план на 30 дней",
                 "На основе того, что узнали на этой неделе, напишите конкретные цели на следующий месяц. Конкретные планы побеждают расплывчатую тревогу каждый раз."),
            ],
            "tools": ["ChatGPT", "Claude", "Perplexity", "Notion AI", "Grammarly"],
            "checklist": ["Найти человеческую грань", "Выучить 1 инструмент ИИ", "Автоматизировать 1 задачу", "Поговорить с руководителем", "Выработать привычку учиться", "Присоединиться к сообществу"],
        },
    },
}


def create_pdf(lang, role, data):
    filename = f"{OUTPUT_DIR}/safemind_survival_guide_{lang}_{role}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=24,
        textColor=colors.HexColor('#C84B31'),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    day_title_style = ParagraphStyle(
        'DayTitle',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8,
    )
    
    day_text_style = ParagraphStyle(
        'DayText',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=20,
        leading=16,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
        spaceBefore=20,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        leading=16,
    )
    
    story = []
    
    # Title
    story.append(Paragraph(data["title"], title_style))
    story.append(Paragraph(data["subtitle"], subtitle_style))
    story.append(Spacer(1, 20))
    
    # 7 Days
    for day_title, day_text in data["days"]:
        story.append(Paragraph(f"<b>{day_title}</b>", day_title_style))
        story.append(Paragraph(day_text, day_text_style))
    
    story.append(PageBreak())
    
    # Tools section
    story.append(Paragraph("Recommended Tools" if lang == "en" else "Рекомендуемые инструменты", heading_style))
    story.append(Spacer(1, 10))
    
    tools_data = [[tool] for tool in data["tools"]]
    tools_table = Table(tools_data, colWidths=[doc.width])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#faf8f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e8e2da')),
    ]))
    story.append(tools_table)
    
    story.append(Spacer(1, 30))
    
    # Checklist
    story.append(Paragraph("Your Week 1 Checklist" if lang == "en" else "Ваш чек-лист на неделю 1", heading_style))
    story.append(Spacer(1, 10))
    
    for item in data["checklist"]:
        story.append(Paragraph(f"☐ {item}", normal_style))
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 30))
    
    # CTA
    cta_text = ("Ready for the full plan? Join SafeMind for personalized guidance, community support, and expert help." 
                if lang == "en" else 
                "Готовы к полному плану? Присоединяйтесь к SafeMind для персонального руководства, поддержки сообщества и помощи экспертов.")
    story.append(Paragraph(f"<i>{cta_text}</i>", ParagraphStyle(
        'CTA',
        parent=normal_style,
        textColor=colors.HexColor('#C84B31'),
        alignment=TA_CENTER,
        spaceBefore=20,
    )))
    
    doc.build(story)
    print(f"Created: {filename}")


def main():
    for lang in ["en", "ru"]:
        for role in ["manager", "marketing", "developer", "generic"]:
            create_pdf(lang, role, CONTENT[lang][role])
    
    print(f"\nAll PDFs created in {OUTPUT_DIR}/")
    print("Files:")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.pdf'):
            print(f"  - {f}")


if __name__ == "__main__":
    main()
