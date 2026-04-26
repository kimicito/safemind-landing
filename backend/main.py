"""
SafeMind Backend — Lead Capture + Drip Email Campaign
Stack: FastAPI + SQLAlchemy + PostgreSQL + Resend
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import resend
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

# ─── Config ──────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/safemind")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "hello@safemind.pro")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "dev-token-change-me")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://safemind.pro")

resend.api_key = RESEND_API_KEY

# ─── Logging ─────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Database ────────────────────────────────────────────────────────────
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    lang = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_email_sent = Column(DateTime(timezone=True), nullable=True)
    email_count = Column(Integer, default=0)
    status = Column(String, default="subscribed")  # subscribed, unsubscribed, bounced
    welcome_sent = Column(Integer, default=0)  # 0 = no, 1 = yes
    drip_day3_sent = Column(Integer, default=0)
    drip_day7_sent = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# ─── Pydantic Models ─────────────────────────────────────────────────────
class SubscribeRequest(BaseModel):
    email: EmailStr
    role: str
    lang: str = "en"

class LeadResponse(BaseModel):
    id: int
    email: str
    role: str
    lang: str
    created_at: datetime
    last_email_sent: Optional[datetime]
    email_count: int
    status: str
    welcome_sent: int
    drip_day3_sent: int
    drip_day7_sent: int
    
    class Config:
        from_attributes = True

# ─── FastAPI App ─────────────────────────────────────────────────────────
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    logger.info("Scheduler started")
    yield
    scheduler.shutdown()

app = FastAPI(title="SafeMind Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Dependencies ────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_admin(token: str = Header(..., alias="X-Admin-Token")):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return True

# ─── Email Templates ─────────────────────────────────────────────────────
PDF_URLS = {
    "en": {
        "marketing": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_marketing.pdf",
        "hr": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_hr.pdf",
        "teacher": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_teacher.pdf",
        "legal": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_legal.pdf",
        "finance": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_finance.pdf",
        "transport": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_transport.pdf",
        "procurement": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_procurement.pdf",
        "economist": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_en_economist.pdf",
    },
    "ru": {
        "marketing": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_marketing.pdf",
        "hr": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_hr.pdf",
        "teacher": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_teacher.pdf",
        "legal": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_legal.pdf",
        "finance": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_finance.pdf",
        "transport": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_transport.pdf",
        "procurement": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_procurement.pdf",
        "economist": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_ru_economist.pdf",
    },
    "es": {
        "marketing": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_marketing.pdf",
        "hr": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_hr.pdf",
        "teacher": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_teacher.pdf",
        "legal": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_legal.pdf",
        "finance": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_finance.pdf",
        "transport": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_transport.pdf",
        "procurement": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_procurement.pdf",
        "economist": f"{FRONTEND_URL}/pdfs/safemind_survival_guide_es_economist.pdf",
    }
}

EMAIL_TEMPLATES = {
    "en": {
        "welcome": {
            "subject": "Your AI Survival Guide is here 🛡️",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h1 style="color: #C84B31;">Welcome to SafeMind</h1>
<p>You made a smart move. While others panic about AI, you're taking action.</p>
<p>Here's your <strong>AI Survival Guide</strong> tailored to your role:</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0;">
<a href="{pdf_url}" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">📥 Download Your Guide</a>
</div>
<p>Over the next week, I'll send you:</p>
<ul>
<li>Day 3: A real case study of someone who turned AI anxiety into a promotion</li>
<li>Day 7: The full 30-day roadmap (and how to get it)</li>
</ul>
<p>Questions? Just reply to this email — a real human reads every message.</p>
<p style="color: #666;">— The SafeMind Team</p>
</body></html>"""
        },
        "drip3": {
            "subject": "She cut her report time from 3 days to 3 hours",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">Real Story: Ana, Marketing Analyst</h2>
<p>3 months ago, Ana spent 3 days on monthly market reports. Her boss hinted that "AI could do this faster." She couldn't sleep.</p>
<p><strong>Week 1:</strong> She learned ChatGPT for data analysis.</p>
<p><strong>Week 3:</strong> She automated the report structure.</p>
<p><strong>Week 4:</strong> She presented a new "AI-assisted workflow" and became the team's "AI lead."</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<div style="font-size: 2rem; font-weight: 800; color: #C84B31;">85%</div>
<div style="color: #666;">Time Reduction</div>
</div>
<p>Ana didn't become a tech expert. She just learned which AI tools helped <em>her</em> job — and used them before her company forced her to.</p>
<p><a href="{frontend_url}" style="color: #C84B31; font-weight: 700;">Want the full 30-day plan? →</a></p>
<p style="color: #666;">— SafeMind</p>
</body></html>"""
        },
        "drip7": {
            "subject": "Your 7-day checklist is done. What's next?",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">You've completed Week 1 🎉</h2>
<p>If you've been following the guide, you've already:</p>
<ul>
<li>Audited your tasks for AI automation</li>
<li>Tried at least one AI tool</li>
<li>Automated one recurring report</li>
</ul>
<p>That's more than 90% of your colleagues have done.</p>
<h3>But here's the truth...</h3>
<p>The 7-day guide gives you quick wins. The <strong>30-day SafeMind Pro plan</strong> gives you:</p>
<ul>
<li>Detailed week-by-week roadmaps for your exact role</li>
<li>Templates, scripts, and prompt libraries</li>
<li>Weekly check-ins with a real human</li>
<li>Priority access to our community</li>
</ul>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<a href="{frontend_url}/#pricing" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">Explore SafeMind Pro →</a>
</div>
<p>Either way, you're already ahead. Keep going.</p>
<p style="color: #666;">— The SafeMind Team</p>
</body></html>"""
        }
    },
    "ru": {
        "welcome": {
            "subject": "Ваш гид по выживанию в эпоху ИИ 🛡️",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h1 style="color: #C84B31;">Добро пожаловать в SafeMind</h1>
<p>Вы поступили умно. Пока другие паникуют из-за ИИ, вы действуете.</p>
<p>Ваш <strong>гид по выживанию</strong>, адаптированный под вашу роль:</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0;">
<a href="{pdf_url}" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">📥 Скачать гид</a>
</div>
<p>В течение недели я пришлю вам:</p>
<ul>
<li>День 3: Реальный кейс человека, который преврал тревогу от ИИ в повышение</li>
<li>День 7: Полный 30-дневный план (и как его получить)</li>
</ul>
<p>Вопросы? Просто ответьте на это письмо — его читает живой человек.</p>
<p style="color: #666;">— Команда SafeMind</p>
</body></html>"""
        },
        "drip3": {
            "subject": "Она сократила время отчёта с 3 дней до 3 часов",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">История: Анна, маркетолог-аналитик</h2>
<p>3 месяца назад Анна тратила 3 дня на ежемесячные отчёты. Начальник намекнул, что «ИИ справится быстрее». Она не спала.</p>
<p><strong>Неделя 1:</strong> Научилась использовать ChatGPT для анализа данных.</p>
<p><strong>Неделя 3:</strong> Автоматизировала структуру отчёта.</p>
<p><strong>Неделя 4:</strong> Представила новый «ИИ-ассистированный воркфлоу» и стала «ИИ-лидом» команды.</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<div style="font-size: 2rem; font-weight: 800; color: #C84B31;">85%</div>
<div style="color: #666;">Сокращение времени</div>
</div>
<p>Анна не стала техническим экспертом. Она просто узнала, какие ИИ-инструменты помогают в <em>её</em> работе — и начала использовать их раньше, чем компания заставила.</p>
<p><a href="{frontend_url}" style="color: #C84B31; font-weight: 700;">Хотите полный 30-дневный план? →</a></p>
<p style="color: #666;">— SafeMind</p>
</body></html>"""
        },
        "drip7": {
            "subject": "Ваш чек-лист на 7 дней выполнен. Что дальше?",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">Вы завершили неделю 1 🎉</h2>
<p>Если вы следовали гиду, вы уже:</p>
<ul>
<li>Провели аудит задач на автоматизацию</li>
<li>Попробовали хотя бы один ИИ-инструмент</li>
<li>Автоматизировали один повторяющийся отчёт</li>
</ul>
<p>Это больше, чем сделали 90% ваших коллег.</p>
<h3>Но вот правда...</h3>
<p>7-дневный гид даёт быстрые победы. <strong>План SafeMind Pro на 30 дней</strong> даёт:</p>
<ul>
<li>Детальные дорожные карты под вашу роль</li>
<li>Шаблоны, скрипты и библиотеки промптов</li>
<li>Еженедельные чек-ины с живым человеком</li>
<li>Приоритетный доступ к сообществу</li>
</ul>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<a href="{frontend_url}/ru/index.html#pricing" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">Посмотреть SafeMind Pro →</a>
</div>
<p>В любом случае, вы уже впереди. Продолжайте.</p>
<p style="color: #666;">— Команда SafeMind</p>
</body></html>"""
        }
    },
    "es": {
        "welcome": {
            "subject": "Tu Guía de Supervivencia IA está aquí 🛡️",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h1 style="color: #C84B31;">Bienvenido a SafeMind</h1>
<p>Hiciste un movimiento inteligente. Mientras otros entran en pánico por la IA, tú estás tomando acción.</p>
<p>Aquí está tu <strong>Guía de Supervivencia IA</strong> adaptada a tu rol:</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0;">
<a href="{pdf_url}" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">📥 Descargar tu guía</a>
</div>
<p>Durante la próxima semana, te enviaré:</p>
<ul>
<li>Día 3: Un caso real de alguien que convirtió la ansiedad por IA en un ascenso</li>
<li>Día 7: El plan completo de 30 días (y cómo obtenerlo)</li>
</ul>
<p>¿Preguntas? Solo responde a este email — un humano real lee cada mensaje.</p>
<p style="color: #666;">— El equipo de SafeMind</p>
</body></html>"""
        },
        "drip3": {
            "subject": "Ella redujo el tiempo de su reporte de 3 días a 3 horas",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">Historia real: Ana, analista de marketing</h2>
<p>Hace 3 meses, Ana pasaba 3 días en reportes de mercado mensuales. Su jefe insinuó que "la IA podría hacerlo más rápido." No podía dormir.</p>
<p><strong>Semana 1:</strong> Aprendió ChatGPT para análisis de datos.</p>
<p><strong>Semana 3:</strong> Automatizó la estructura del reporte.</p>
<p><strong>Semana 4:</strong> Presentó un nuevo "flujo de trabajo asistido por IA" y se convirtió en la "líder de IA" del equipo.</p>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<div style="font-size: 2rem; font-weight: 800; color: #C84B31;">85%</div>
<div style="color: #666;">Reducción de tiempo</div>
</div>
<p>Ana no se convirtió en experta tecnológica. Solo aprendió qué herramientas de IA ayudan en <em>su</em> trabajo — y las usó antes de que la compañía la obligara.</p>
<p><a href="{frontend_url}" style="color: #C84B31; font-weight: 700;">¿Quieres el plan completo de 30 días? →</a></p>
<p style="color: #666;">— SafeMind</p>
</body></html>"""
        },
        "drip7": {
            "subject": "Tu checklist de 7 días está completo. ¿Y ahora?",
            "body": """<html>
<body style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a;">
<h2 style="color: #C84B31;">Completaste la Semana 1 🎉</h2>
<p>Si has seguido la guía, ya has:</p>
<ul>
<li>Auditado tus tareas para automatización con IA</li>
<li>Probado al menos una herramienta de IA</li>
<li>Automatizado un reporte recurrente</li>
</ul>
<p>Eso es más de lo que ha hecho el 90% de tus colegas.</p>
<h3>Pero aquí está la verdad...</h3>
<p>La guía de 7 días te da victorias rápidas. El <strong>plan SafeMind Pro de 30 días</strong> te da:</p>
<ul>
<li>Mapas detallados semana a semana para tu rol exacto</li>
<li>Plantillas, scripts y bibliotecas de prompts</li>
<li>Check-ins semanales con un humano real</li>
<li>Acceso prioritario a nuestra comunidad</li>
</ul>
<div style="background: #f5f1ec; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
<a href="{frontend_url}/es/index.html#pricing" style="background: #C84B31; color: white; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: 700; display: inline-block;">Explorar SafeMind Pro →</a>
</div>
<p>De cualquier manera, ya vas adelante. Sigue así.</p>
<p style="color: #666;">— El equipo de SafeMind</p>
</body></html>"""
        }
    }
}

# ─── Email Service ───────────────────────────────────────────────────────
def send_email(to: str, subject: str, html_body: str) -> bool:
    """Send email via Resend"""
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set, skipping email send")
        return False
    
    try:
        params = {
            "from": f"SafeMind <{FROM_EMAIL}>",
            "to": [to],
            "subject": subject,
            "html": html_body,
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent to {to}: {response}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        return False

def get_pdf_url(role: str, lang: str) -> str:
    """Get PDF URL for role and language"""
    role_map = {
        "marketing": "marketing", "hr": "hr", "teacher": "teacher", "legal": "legal",
        "finance": "finance", "transport": "transport", "procurement": "procurement",
        "economist": "economist"
    }
    mapped_role = role_map.get(role, "marketing")
    urls = PDF_URLS.get(lang, PDF_URLS["en"])
    return urls.get(mapped_role, urls["marketing"])

def send_welcome_email(lead: Lead):
    """Send welcome email with PDF"""
    lang = lead.lang if lead.lang in EMAIL_TEMPLATES else "en"
    template = EMAIL_TEMPLATES[lang]["welcome"]
    pdf_url = get_pdf_url(lead.role, lang)
    
    body = template["body"].format(pdf_url=pdf_url, frontend_url=FRONTEND_URL)
    
    success = send_email(lead.email, template["subject"], body)
    return success

def send_drip_email(lead: Lead, drip_type: str):
    """Send drip email (day3 or day7)"""
    lang = lead.lang if lead.lang in EMAIL_TEMPLATES else "en"
    template = EMAIL_TEMPLATES[lang][drip_type]
    
    body = template["body"].format(frontend_url=FRONTEND_URL)
    
    success = send_email(lead.email, template["subject"], body)
    return success

# ─── API Endpoints ───────────────────────────────────────────────────────
@app.post("/subscribe", status_code=200)
def subscribe(
    req: SubscribeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Subscribe a new lead and trigger welcome email"""
    
    # Check if already exists
    existing = db.query(Lead).filter(Lead.email == req.email).first()
    if existing:
        if existing.status == "unsubscribed":
            existing.status = "subscribed"
            db.commit()
            return {"message": "Resubscribed successfully", "lead_id": existing.id}
        return {"message": "Already subscribed", "lead_id": existing.id}
    
    # Create new lead
    lead = Lead(
        email=req.email,
        role=req.role,
        lang=req.lang,
        status="subscribed"
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    # Send welcome email in background
    background_tasks.add_task(send_welcome_and_update, lead.id)
    
    logger.info(f"New lead subscribed: {req.email} ({req.role}, {req.lang})")
    return {"message": "Subscribed successfully", "lead_id": lead.id}

def send_welcome_and_update(lead_id: int):
    """Send welcome email and update lead record"""
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return
        
        success = send_welcome_email(lead)
        if success:
            lead.welcome_sent = 1
            lead.last_email_sent = func.now()
            lead.email_count += 1
            db.commit()
            logger.info(f"Welcome email sent to {lead.email}")
    finally:
        db.close()

@app.get("/leads", response_model=List[LeadResponse])
def get_leads(
    _: bool = Depends(verify_admin),
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    lang: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """Get all leads (admin only)"""
    query = db.query(Lead)
    
    if status:
        query = query.filter(Lead.status == status)
    if lang:
        query = query.filter(Lead.lang == lang)
    
    leads = query.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()
    return leads

@app.get("/leads/count")
def get_lead_count(
    _: bool = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """Get lead statistics"""
    total = db.query(Lead).count()
    by_lang = db.query(Lead.lang, func.count(Lead.id)).group_by(Lead.lang).all()
    by_role = db.query(Lead.role, func.count(Lead.id)).group_by(Lead.role).all()
    
    return {
        "total": total,
        "by_language": {lang: count for lang, count in by_lang},
        "by_role": {role: count for role, count in by_role}
    }

@app.post("/trigger-drip")
def trigger_drip(
    lead_id: Optional[int] = None,
    drip_type: str = "drip3",  # drip3 or drip7
    _: bool = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """Manually trigger drip email for a lead or all pending leads"""
    
    if lead_id:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        success = send_drip_email(lead, drip_type)
        if success:
            if drip_type == "drip3":
                lead.drip_day3_sent = 1
            else:
                lead.drip_day7_sent = 1
            lead.last_email_sent = func.now()
            lead.email_count += 1
            db.commit()
        
        return {"message": f"Drip {drip_type} sent to {lead.email}", "success": success}
    
    # Send to all pending leads
    query = db.query(Lead).filter(Lead.status == "subscribed")
    
    if drip_type == "drip3":
        query = query.filter(Lead.welcome_sent == 1, Lead.drip_day3_sent == 0)
        # Only leads who subscribed 3+ days ago
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        query = query.filter(Lead.created_at <= three_days_ago)
    elif drip_type == "drip7":
        query = query.filter(Lead.drip_day3_sent == 1, Lead.drip_day7_sent == 0)
        # Only leads who got drip3 4+ days ago (so 7+ days total)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Lead.created_at <= seven_days_ago)
    
    leads = query.all()
    sent = 0
    failed = 0
    
    for lead in leads:
        success = send_drip_email(lead, drip_type)
        if success:
            if drip_type == "drip3":
                lead.drip_day3_sent = 1
            else:
                lead.drip_day7_sent = 1
            lead.last_email_sent = func.now()
            lead.email_count += 1
            sent += 1
        else:
            failed += 1
    
    db.commit()
    return {"message": f"Drip {drip_type} campaign complete", "sent": sent, "failed": failed}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "resend_configured": bool(RESEND_API_KEY)
    }

# ─── Scheduled Drip Jobs ─────────────────────────────────────────────────
def run_daily_drip():
    """Run daily drip campaign check"""
    logger.info("Running daily drip check...")
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        
        # Day 3 drip
        three_days_ago = now - timedelta(days=3)
        day3_leads = db.query(Lead).filter(
            Lead.status == "subscribed",
            Lead.welcome_sent == 1,
            Lead.drip_day3_sent == 0,
            Lead.created_at <= three_days_ago
        ).all()
        
        for lead in day3_leads:
            success = send_drip_email(lead, "drip3")
            if success:
                lead.drip_day3_sent = 1
                lead.last_email_sent = func.now()
                lead.email_count += 1
                logger.info(f"Day 3 drip sent to {lead.email}")
        
        # Day 7 drip
        seven_days_ago = now - timedelta(days=7)
        day7_leads = db.query(Lead).filter(
            Lead.status == "subscribed",
            Lead.drip_day3_sent == 1,
            Lead.drip_day7_sent == 0,
            Lead.created_at <= seven_days_ago
        ).all()
        
        for lead in day7_leads:
            success = send_drip_email(lead, "drip7")
            if success:
                lead.drip_day7_sent = 1
                lead.last_email_sent = func.now()
                lead.email_count += 1
                logger.info(f"Day 7 drip sent to {lead.email}")
        
        db.commit()
        logger.info(f"Daily drip complete. Day3: {len(day3_leads)}, Day7: {len(day7_leads)}")
    except Exception as e:
        logger.error(f"Daily drip failed: {e}")
    finally:
        db.close()

# Schedule daily drip check at 10:00 UTC
scheduler.add_job(run_daily_drip, "cron", hour=10, minute=0, id="daily_drip")

# ─── Run ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
