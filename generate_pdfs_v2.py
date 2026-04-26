#!/usr/bin/env python3
"""
Generate SafeMind Lead Magnet PDFs for industrial/metallurgy roles
8 roles: marketing, hr, teacher, legal, finance, transport, procurement, economist
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
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
    "ru": {
        "marketing": {
            "title": "Руководство: ИИ для маркетолога",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Научите ИИ писать первый черновик отчёта по рынку",
                "✓ День 2: Сгенерируйте структуру презентации за 10 минут",
                "✓ День 3: Попросите ИИ найти 10 трендов в вашей отрасли",
                "✓ День 4: Создайте шаблон аналитического вывода (SWOT, PEST)",
                "✓ День 5: Автоматизируйте обзор конкурентов — еженедельный бриф",
                "✓ День 6: Сделайте ИИ 'вторым мозгом' для проверки логики",
                "✓ День 7: Запишите 3 промпта, которые экономят 2 часа в неделю",
            ],
            "tools": ["ChatGPT", "Perplexity", "Gamma.app (презентации)", "Notion AI"],
            "teaser": "Полный план включает: 30 готовых промптов для маркетолога, шаблоны отчётов, скрипты презентаций, инструкцию по анализу конкурентов и чек-лист 'Что автоматизировать первым'. Доступно в SafeMind Pro.",
        },
        "hr": {
            "title": "Руководство: ИИ для HR-специалиста",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Напишите первое объявление о вакансии с помощью ИИ",
                "✓ День 2: Научите ИИ фильтровать резюме по 3 критериям",
                "✓ День 3: Сгенерируйте план обучения для нового сотрудника",
                "✓ День 4: Создайте банк вопросов для собеседований под вашу отрасль",
                "✓ День 5: Автоматизируйте подготовку курса — структура за 15 минут",
                "✓ День 6: Попросите ИИ составить адаптационный чек-лист",
                "✓ День 7: Зафиксируйте 3 процесса, которые теперь делаются в 2 раза быстрее",
            ],
            "tools": ["ChatGPT", "Claude", "LinkedIn + ИИ", "Trello / Notion"],
            "teaser": "Полный план включает: 50 промптов для HR, шаблоны вакансий, систему скрининга резюме, программы адаптации и обучения, чек-листы собеседований. Доступно в SafeMind Pro.",
        },
        "teacher": {
            "title": "Руководство: ИИ для преподавателя",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Сгенерируйте план урока на любую тему за 5 минут",
                "✓ День 2: Создайте 10 нестандартных заданий с помощью ИИ",
                "✓ День 3: Попросите ИИ проверить 5 работ и дать развёрнутый фидбек",
                "✓ День 4: Соберите подборку свежих кейсов из вашей отрасли",
                "✓ День 5: Автоматизируйте создание тестов и контрольных",
                "✓ День 6: Сделайте ИИ 'учёным редактором' для проверки фактов",
                "✓ День 7: Запишите 3 урока, которые теперь готовятся за 20 минут",
            ],
            "tools": ["ChatGPT", "Claude", "Quizlet / Kahoot", "Canva + ИИ"],
            "teaser": "Полный план включает: 40 промптов для преподавателя, банк заданий, шаблоны уроков, систему проверки работ, подборку кейсов по отраслям и методички. Доступно в SafeMind Pro.",
        },
        "legal": {
            "title": "Руководство: ИИ для юриста",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Попросите ИИ проверить договор на 5 типичных рисков",
                "✓ День 2: Сгенерируйте шаблон претензии за 10 минут",
                "✓ День 3: Создайте базу ответов на типовые вопросы сотрудников",
                "✓ День 4: Попросите ИИ сравнить ваш договор с типовым ГК РФ",
                "✓ День 5: Автоматизируйте подготовку искового заявления — черновик",
                "✓ День 6: Сделайте ИИ 'помощником' по подбору нормативных актов",
                "✓ День 7: Зафиксируйте 3 шаблона, которые теперь создаются за 15 минут",
            ],
            "tools": ["ChatGPT", "Claude", "КонсультантПлюс (проверка)", "Garant / Кодекс"],
            "teaser": "Полный план включает: 35 промптов для юриста, шаблоны договоров и претензий, систему проверки документов, базу ответов сотрудникам, чек-листы рисков. Доступно в SafeMind Pro.",
        },
        "finance": {
            "title": "Руководство: ИИ для финансового менеджера",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Попросите ИИ проанализировать отчёт и выделить 3 тревожных тренда",
                "✓ День 2: Сгенерируйте сводку данных из 5 таблиц в один текст",
                "✓ День 3: Автоматизируйте сверку — ИИ находит расхождения",
                "✓ День 4: Создайте шаблон финансового прогноза на квартал",
                "✓ День 5: Попросите ИИ объяснить сложные показатели простым языком",
                "✓ День 6: Сделайте ИИ 'аудитором' для проверки расчётов",
                "✓ День 7: Запишите 3 отчёта, которые теперь готовятся в 2 раза быстрее",
            ],
            "tools": ["ChatGPT", "Claude", "Excel + ИИ", "Power BI / Tableau"],
            "teaser": "Полный план включает: 40 промптов для финансиста, шаблоны сверок и прогнозов, систему анализа трендов, чек-листы аудита, инструкции по автоматизации отчётности. Доступно в SafeMind Pro.",
        },
        "transport": {
            "title": "Руководство: ИИ для транспортного менеджера",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Попросите ИИ структурировать типовой пакет документов",
                "✓ День 2: Сгенерируйте шаблон сопроводительного письма к перевозке",
                "✓ День 3: Автоматизируйте заполнение типовых форм — шаблоны",
                "✓ День 4: Создайте чек-лист проверки документов на рейс",
                "✓ День 5: Попросите ИИ найти нормативные требования к перевозке",
                "✓ День 6: Сделайте ИИ 'секретарём' для подготовки отчётов по логистике",
                "✓ День 7: Зафиксируйте 3 бумажных процесса, которые ушли в цифру",
            ],
            "tools": ["ChatGPT", "Claude", "OCR + ИИ (для сканов)", "Google Sheets / Excel"],
            "teaser": "Полный план включает: 30 промптов для транспортного менеджера, шаблоны документов, систему проверки рейсов, нормативную базу, инструкции по оцифровке бумажных процессов. Доступно в SafeMind Pro.",
        },
        "procurement": {
            "title": "Руководство: ИИ для закупщика",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Попросите ИИ найти 5 поставщиков и сравнить цены",
                "✓ День 2: Сгенерируйте шаблон запроса котировок за 10 минут",
                "✓ День 3: Автоматизируйте проверку счёта-фактуры на ошибки",
                "✓ День 4: Создайте обзор рынка материалов за последний квартал",
                "✓ День 5: Попросите ИИ проанализировать условия договора поставки",
                "✓ День 6: Сделайте ИИ 'аналитиком' для отслеживания ценовых трендов",
                "✓ День 7: Запишите 3 процесса закупки, которые ускорились в 2 раза",
            ],
            "tools": ["ChatGPT", "Perplexity", "Excel + ИИ", "CRM / 1С"],
            "teaser": "Полный план включает: 35 промптов для закупщика, шаблоны запросов и договоров, систему сравнения поставщиков, анализ ценовых трендов, чек-листы проверки документов. Доступно в SafeMind Pro.",
        },
        "economist": {
            "title": "Руководство: ИИ для экономиста",
            "subtitle": "Быстрый старт за 7 дней (бесплатная версия)",
            "inside": [
                "✓ День 1: Попросите ИИ оценить финансовый отчёт и найти 3 зоны риска",
                "✓ День 2: Сгенерируйте варианты оптимизации затрат на основе данных",
                "✓ День 3: Автоматизируйте расчёт KPI — шаблон и формулы",
                "✓ День 4: Создайте сценарный анализ: лучший / худший / реалистичный",
                "✓ День 5: Попросите ИИ объяснить отклонения бюджета простым языком",
                "✓ День 6: Сделайте ИИ 'консультантом' для поиска точек роста",
                "✓ День 7: Запишите 3 отчёта, которые теперь строятся за 30 минут",
            ],
            "tools": ["ChatGPT", "Claude", "Excel + ИИ", "Power BI"],
            "teaser": "Полный план включает: 40 промптов для экономиста, шаблоны сценарного анализа, систему расчёта KPI, чек-листы оптимизации, инструкции по автоматизации отчётности. Доступно в SafeMind Pro.",
        },
    },
    "en": {
        "marketing": {
            "title": "Guide: AI for Marketing Analyst",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Teach AI to draft your first market report",
                "✓ Day 2: Generate a presentation structure in 10 minutes",
                "✓ Day 3: Ask AI to find 10 trends in your industry",
                "✓ Day 4: Create a template for analytical conclusions (SWOT, PEST)",
                "✓ Day 5: Automate competitor monitoring — weekly briefing",
                "✓ Day 6: Make AI your 'second brain' for logic checking",
                "✓ Day 7: Write down 3 prompts that save 2 hours per week",
            ],
            "tools": ["ChatGPT", "Perplexity", "Gamma.app (presentations)", "Notion AI"],
            "teaser": "The full plan includes: 30 ready-made prompts for marketers, report templates, presentation scripts, competitor analysis guide, and 'What to automate first' checklist. Available in SafeMind Pro.",
        },
        "hr": {
            "title": "Guide: AI for HR Specialist",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Write your first AI-assisted job posting",
                "✓ Day 2: Teach AI to screen resumes by 3 criteria",
                "✓ Day 3: Generate an onboarding plan for a new employee",
                "✓ Day 4: Create an interview question bank for your industry",
                "✓ Day 5: Automate course preparation — structure in 15 minutes",
                "✓ Day 6: Ask AI to build an adaptation checklist",
                "✓ Day 7: Document 3 processes that now run 2x faster",
            ],
            "tools": ["ChatGPT", "Claude", "LinkedIn + AI", "Trello / Notion"],
            "teaser": "The full plan includes: 50 HR prompts, job posting templates, resume screening system, onboarding and training programs, interview checklists. Available in SafeMind Pro.",
        },
        "teacher": {
            "title": "Guide: AI for Educator",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Generate a lesson plan on any topic in 5 minutes",
                "✓ Day 2: Create 10 creative assignments with AI help",
                "✓ Day 3: Ask AI to review 5 papers and give detailed feedback",
                "✓ Day 4: Gather fresh industry cases for your subject",
                "✓ Day 5: Automate test and exam creation",
                "✓ Day 6: Make AI your 'fact-checking editor'",
                "✓ Day 7: Document 3 lessons that now prep in 20 minutes",
            ],
            "tools": ["ChatGPT", "Claude", "Quizlet / Kahoot", "Canva + AI"],
            "teaser": "The full plan includes: 40 educator prompts, assignment bank, lesson templates, paper review system, industry case collections, and teaching guides. Available in SafeMind Pro.",
        },
        "legal": {
            "title": "Guide: AI for Legal Counsel",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Ask AI to review a contract for 5 typical risks",
                "✓ Day 2: Generate a claim letter template in 10 minutes",
                "✓ Day 3: Create a response bank for typical employee questions",
                "✓ Day 4: Ask AI to compare your contract with standard Civil Code",
                "✓ Day 5: Automate lawsuit drafting — first draft",
                "✓ Day 6: Make AI your 'regulatory research assistant'",
                "✓ Day 7: Document 3 templates that now create in 15 minutes",
            ],
            "tools": ["ChatGPT", "Claude", "Legal databases", "Contract analysis tools"],
            "teaser": "The full plan includes: 35 legal prompts, contract and claim templates, document review system, employee response base, risk checklists. Available in SafeMind Pro.",
        },
        "finance": {
            "title": "Guide: AI for Finance Manager",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Ask AI to analyze a report and spot 3 concerning trends",
                "✓ Day 2: Generate a data summary from 5 spreadsheets into one text",
                "✓ Day 3: Automate reconciliation — AI finds discrepancies",
                "✓ Day 4: Create a quarterly financial forecast template",
                "✓ Day 5: Ask AI to explain complex metrics in plain language",
                "✓ Day 6: Make AI your 'auditor' for calculation checking",
                "✓ Day 7: Document 3 reports that now prepare 2x faster",
            ],
            "tools": ["ChatGPT", "Claude", "Excel + AI", "Power BI / Tableau"],
            "teaser": "The full plan includes: 40 finance prompts, reconciliation and forecast templates, trend analysis system, audit checklists, report automation guides. Available in SafeMind Pro.",
        },
        "transport": {
            "title": "Guide: AI for Transport Manager",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Ask AI to structure a typical document package",
                "✓ Day 2: Generate a shipping cover letter template",
                "✓ Day 3: Automate standard form filling — templates",
                "✓ Day 4: Create a pre-trip document checklist",
                "✓ Day 5: Ask AI to find regulatory requirements for shipping",
                "✓ Day 6: Make AI your 'secretary' for logistics reporting",
                "✓ Day 7: Document 3 paper processes that went digital",
            ],
            "tools": ["ChatGPT", "Claude", "OCR + AI (for scans)", "Google Sheets / Excel"],
            "teaser": "The full plan includes: 30 transport manager prompts, document templates, trip verification system, regulatory base, paper-to-digital process guides. Available in SafeMind Pro.",
        },
        "procurement": {
            "title": "Guide: AI for Procurement Specialist",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Ask AI to find 5 suppliers and compare prices",
                "✓ Day 2: Generate an RFQ template in 10 minutes",
                "✓ Day 3: Automate invoice error checking",
                "✓ Day 4: Create a quarterly materials market overview",
                "✓ Day 5: Ask AI to analyze delivery contract terms",
                "✓ Day 6: Make AI your 'analyst' for price trend tracking",
                "✓ Day 7: Document 3 procurement processes that sped up 2x",
            ],
            "tools": ["ChatGPT", "Perplexity", "Excel + AI", "CRM / ERP"],
            "teaser": "The full plan includes: 35 procurement prompts, RFQ and contract templates, supplier comparison system, price trend analysis, document verification checklists. Available in SafeMind Pro.",
        },
        "economist": {
            "title": "Guide: AI for Economist",
            "subtitle": "7-Day Quick Start (Free Preview)",
            "inside": [
                "✓ Day 1: Ask AI to evaluate a financial report and find 3 risk zones",
                "✓ Day 2: Generate cost optimization options from data",
                "✓ Day 3: Automate KPI calculation — template and formulas",
                "✓ Day 4: Create scenario analysis: best / worst / realistic",
                "✓ Day 5: Ask AI to explain budget deviations in plain language",
                "✓ Day 6: Make AI your 'consultant' for finding growth points",
                "✓ Day 7: Document 3 reports that now build in 30 minutes",
            ],
            "tools": ["ChatGPT", "Claude", "Excel + AI", "Power BI"],
            "teaser": "The full plan includes: 40 economist prompts, scenario analysis templates, KPI calculation system, optimization checklists, report automation guides. Available in SafeMind Pro.",
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
        fontSize=20,
        textColor=colors.HexColor('#C84B31'),
        spaceAfter=8,
        alignment=TA_CENTER,
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=24,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=13,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10,
        spaceBefore=14,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        leading=14,
        spaceAfter=6,
    )
    
    teaser_style = ParagraphStyle(
        'Teaser',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        textColor=colors.HexColor('#8B6F4E'),
        leading=13,
        spaceBefore=16,
        leftIndent=10,
        rightIndent=10,
        borderWidth=1,
        borderColor=colors.HexColor('#D4A574'),
        borderPadding=10,
        backColor=colors.HexColor('#faf8f5'),
    )
    
    story = []
    
    story.append(Paragraph("🛡️ SafeMind", ParagraphStyle(
        'Brand', parent=normal_style, alignment=TA_CENTER, 
        textColor=colors.HexColor('#C84B31'), fontSize=10, spaceAfter=4)))
    story.append(Paragraph(data["title"], title_style))
    story.append(Paragraph(data["subtitle"], subtitle_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("What's Inside" if lang == "en" else "Что внутри", heading_style))
    for item in data["inside"]:
        story.append(Paragraph(item, normal_style))
    
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Tools to Try This Week" if lang == "en" else "Инструменты на эту неделю", heading_style))
    for tool in data["tools"]:
        story.append(Paragraph(f"• {tool}", normal_style))
    
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(data["teaser"], teaser_style))
    
    cta = "Get the full plan at safemind.org" if lang == "en" else "Полный план — на safemind.org"
    story.append(Paragraph(f"<b>{cta}</b>", ParagraphStyle(
        'CTA', parent=normal_style, alignment=TA_CENTER, 
        textColor=colors.HexColor('#C84B31'), fontSize=10, spaceBefore=12)))
    
    doc.build(story)
    print(f"Created: {filename}")


def main():
    for lang in ["en", "ru"]:
        for role in ["marketing", "hr", "teacher", "legal", "finance", "transport", "procurement", "economist"]:
            create_pdf(lang, role, CONTENT[lang][role])
    
    print(f"\nAll PDFs created in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
