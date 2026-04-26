#!/usr/bin/env python3
"""
Generate SHORT SafeMind Lead Magnet PDFs (3-4 pages max)
Teaser for full paid plan at the end
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    FONT_NAME = 'DejaVu'
except:
    FONT_NAME = 'Helvetica'

OUTPUT_DIR = "/root/.openclaw/workspace/safemind/pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CONTENT = {
    "en": {
        "manager": {
            "title": "AI Survival Guide: Manager Edition",
            "subtitle": "Your 7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Audit your decisions — find what's AI-proof",
                "✓ Day 2: Become the AI translator for your team", 
                "✓ Day 3: Delegate routine to AI, keep strategy for you",
                "✓ Day 4: Build your human network (AI can't replicate relationships)",
                "✓ Day 5: Master the 5-minute AI briefing",
                "✓ Day 6: Position yourself as the AI champion",
                "✓ Day 7: Lock in your 30-day learning habit",
            ],
            "tools": ["ChatGPT", "Claude", "Notion AI", "Fireflies.ai"],
            "teaser": "The full Manager's Plan includes: 30-day detailed roadmap, email templates for AI conversations with your team, meeting scripts, a 'Defend Your Role' presentation deck, and weekly check-ins. Available in SafeMind Pro.",
        },
        "marketing": {
            "title": "AI Survival Guide: Marketer Edition",
            "subtitle": "Your 7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Find your human angle that AI can't copy",
                "✓ Day 2: Use AI for research, you keep strategy",
                "✓ Day 3: Automate grunt work (scheduling, analysis)",
                "✓ Day 4: Build personal brand as unemployment insurance",
                "✓ Day 5: Learn visual AI to direct designers, not replace them",
                "✓ Day 6: Run AI vs Human A/B test",
                "✓ Day 7: Plan your AI-proof career path",
            ],
            "tools": ["ChatGPT", "Midjourney", "Perplexity", "Copy.ai"],
            "teaser": "The full Marketer's Plan includes: 30-day content calendar with AI-assisted workflows, brand voice preservation guide, campaign templates, client conversation scripts about AI, and community access. Available in SafeMind Pro.",
        },
        "developer": {
            "title": "AI Survival Guide: Developer Edition",
            "subtitle": "Your 7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Audit your code — what's boilerplate vs. architecture",
                "✓ Day 2: Master AI pair programming (review, don't just accept)",
                "✓ Day 3: Learn system design (AI generates functions, not systems)",
                "✓ Day 4: Build something requiring your company's domain knowledge",
                "✓ Day 5: Become the AI integrator (connect APIs to products)",
                "✓ Day 6: Document like your job depends on it (it does)",
                "✓ Day 7: Pick your specialization — AI is generalist, you go deep",
            ],
            "tools": ["GitHub Copilot", "Claude", "Cursor", "CodeRabbit"],
            "teaser": "The full Developer's Plan includes: 30-day skill roadmap, system design practice projects, AI integration tutorials, ADR templates, code review checklists for AI-generated code, and career pivot guides. Available in SafeMind Pro.",
        },
        "generic": {
            "title": "AI Survival Guide",
            "subtitle": "Your 7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Find your human edge (judgment, empathy, creativity)",
                "✓ Day 2: Learn ONE AI tool for ONE real task",
                "✓ Day 3: Automate one repetitive task",
                "✓ Day 4: Talk to your manager about AI-proof parts of your role",
                "✓ Day 5: Build a 30-minute daily learning habit",
                "✓ Day 6: Join a community of people learning AI together",
                "✓ Day 7: Write your concrete 30-day plan",
            ],
            "tools": ["ChatGPT", "Claude", "Perplexity", "Notion AI"],
            "teaser": "The full Survival Plan includes: 30-day detailed roadmap with daily actions, conversation scripts for managers, learning resource directory by role, anxiety management techniques, and community access. Available in SafeMind Pro.",
        },
    },
    "ru": {
        "manager": {
            "title": "Руководство по выживанию: для руководителей",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Аудит решений — найдите, что ИИ не заменит",
                "✓ День 2: Станьте переводчиком ИИ для команды",
                "✓ День 3: Делегируйте рутину ИИ, стратегию оставьте себе",
                "✓ День 4: Стройте человеческую сеть (ИИ не умеет строить отношения)",
                "✓ День 5: Освойте 5-минутный брифинг для ИИ",
                "✓ День 6: Позиционируйте себя как чемпиона ИИ",
                "✓ День 7: Заблокируйте привычку обучения на 30 дней",
            ],
            "tools": ["ChatGPT", "Claude", "Notion AI", "Fireflies.ai"],
            "teaser": "Полный план для руководителей включает: детальную дорожную карту на 30 дней, шаблоны писем для разговоров об ИИ с командой, скрипты совещаний, презентацию 'Защити свою роль' и еженедельные чек-ины. Доступно в SafeMind Pro.",
        },
        "marketing": {
            "title": "Руководство по выживанию: для маркетологов",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Найдите свой человеческий угол, который ИИ не скопирует",
                "✓ День 2: Используйте ИИ для исследований, стратегию оставьте себе",
                "✓ День 3: Автоматизируйте грязную работу (планирование, анализ)",
                "✓ День 4: Стройте личный бренд как страховку от безработицы",
                "✓ День 5: Выучите визуальный ИИ, чтобы управлять дизайнерами",
                "✓ День 6: Запустите тест ИИ против человека",
                "✓ День 7: Спланируйте карьеру, защищённую от ИИ",
            ],
            "tools": ["ChatGPT", "Midjourney", "Perplexity", "Copy.ai"],
            "teaser": "Полный план для маркетологов включает: контент-календарь на 30 дней с ИИ-воркфлоу, гид по сохранению голоса бренда, шаблоны кампаний, скрипты разговоров с клиентами об ИИ и доступ к сообществу. Доступно в SafeMind Pro.",
        },
        "developer": {
            "title": "Руководство по выживанию: для разработчиков",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Аудит кода — что шаблонно, что требует архитектуры",
                "✓ День 2: Освойте парное программирование с ИИ (ревьюйте, не просто принимайте)",
                "✓ День 3: Выучите проектирование систем (ИИ генерирует функции, не системы)",
                "✓ День 4: Соберите что-то, требующее знаний домена вашей компании",
                "✓ День 5: Станьте интегратором ИИ (подключайте API к продуктам)",
                "✓ День 6: Документируйте так, будто от этого зависит работа (так и есть)",
                "✓ День 7: Выберите специализацию — ИИ генералист, вы уходите вглубь",
            ],
            "tools": ["GitHub Copilot", "Claude", "Cursor", "CodeRabbit"],
            "teaser": "Полный план для разработчиков включает: дорожную карту навыков на 30 дней, проекты для практики системного дизайна, туториалы по интеграции ИИ, шаблоны ADR, чек-листы ревью кода от ИИ и гиды по смене карьеры. Доступно в SafeMind Pro.",
        },
        "generic": {
            "title": "Руководство по выживанию в эпоху ИИ",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Найдите свою человеческую грань (суждение, эмпатия, креативность)",
                "✓ День 2: Выучите ОДИН инструмент ИИ для ОДНОЙ реальной задачи",
                "✓ День 3: Автоматизируйте одну повторяющуюся задачу",
                "✓ День 4: Поговорите с руководителем о частях роли, сложных для автоматизации",
                "✓ День 5: Выработайте привычку: 30 минут ежедневно на изучение ИИ",
                "✓ День 6: Присоединитесь к сообществу людей, изучающих ИИ",
                "✓ День 7: Напишите конкретный план на 30 дней",
            ],
            "tools": ["ChatGPT", "Claude", "Perplexity", "Notion AI"],
            "teaser": "Полный план выживания включает: детальную дорожную карту на 30 дней с ежедневными действиями, скрипты разговоров с руководителем, каталог ресурсов по ролям, техники управления тревогой и доступ к сообществу. Доступно в SafeMind Pro.",
        },
    },
}


def create_pdf(lang, role, data):
    filename = f"{OUTPUT_DIR}/safemind_survival_guide_{lang}_{role}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=22,
        textColor=colors.HexColor('#C84B31'),
        spaceAfter=8,
        alignment=TA_CENTER,
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=14,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
        spaceBefore=16,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10.5,
        textColor=colors.HexColor('#333333'),
        leading=15,
        spaceAfter=8,
    )
    
    teaser_style = ParagraphStyle(
        'Teaser',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=colors.HexColor('#8B6F4E'),
        leading=14,
        spaceBefore=20,
        leftIndent=12,
        rightIndent=12,
        borderWidth=1,
        borderColor=colors.HexColor('#D4A574'),
        borderPadding=12,
        backColor=colors.HexColor('#faf8f5'),
    )
    
    story = []
    
    # Header
    story.append(Paragraph("🛡️ SafeMind", ParagraphStyle(
        'Brand', parent=normal_style, alignment=TA_CENTER, 
        textColor=colors.HexColor('#C84B31'), fontSize=11, spaceAfter=4)))
    story.append(Paragraph(data["title"], title_style))
    story.append(Paragraph(data["subtitle"], subtitle_style))
    story.append(Spacer(1, 10))
    
    # What's Inside
    story.append(Paragraph("What's Inside" if lang == "en" else "Что внутри", heading_style))
    for item in data["inside"]:
        story.append(Paragraph(item, normal_style))
    
    story.append(Spacer(1, 10))
    
    # Tools
    story.append(Paragraph("Tools to Try This Week" if lang == "en" else "Инструменты на эту неделю", heading_style))
    for tool in data["tools"]:
        story.append(Paragraph(f"• {tool}", normal_style))
    
    story.append(Spacer(1, 10))
    
    # Teaser for paid version
    story.append(Paragraph(data["teaser"], teaser_style))
    
    # Footer CTA
    cta = ("Get the full plan at safemind.pro" if lang == "en" else "Полный план — на safemind.pro")
    story.append(Paragraph(f"<b>{cta}</b>", ParagraphStyle(
        'CTA', parent=normal_style, alignment=TA_CENTER, 
        textColor=colors.HexColor('#C84B31'), fontSize=11, spaceBefore=16)))
    
    doc.build(story)
    print(f"Created: {filename}")


def main():
    for lang in ["en", "ru"]:
        for role in ["manager", "marketing", "developer", "generic"]:
            create_pdf(lang, role, CONTENT[lang][role])
    
    print(f"\nAll PDFs created in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
