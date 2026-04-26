#!/usr/bin/env python3
"""Generate Spanish PDFs for SafeMind lead magnet (8 roles)"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register DejaVu fonts (supports Cyrillic and extended Latin)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont('DejaVu', f'{FONT_DIR}/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', f'{FONT_DIR}/DejaVuSans-Bold.ttf'))

ROLES = {
    "marketing": {
        "title": "ESPECIALISTA DE MARKETING",
        "tasks": [
            "Crear presentaciones y reportes",
            "Analizar mercado y competidores",
            "Escribir textos publicitarios",
            "Planificar campañas de contenido"
        ],
        "threats": [
            "IA genera textos y slogans en segundos",
            "Análisis automático de mercado",
            "Generación automática de presentaciones",
            "Optimización de campañas sin humanos"
        ],
        "safety": [
            "Estrategia creativa y conceptos",
            "Entender emociones del cliente",
            "Toma de decisiones bajo incertidumbre",
            "Negociación con partners y clientes"
        ],
        "tools": [
            "ChatGPT — ideas para textos",
            "Perplexity — investigación de mercado",
            "Canva AI — diseño rápido",
            "Notion AI — planificación de contenido"
        ],
        "week1": [
            "Día 1: Audit de tareas — marca qué haces manualmente",
            "Día 2: Prueba ChatGPT para 1 texto publicitario",
            "Día 3: Automatiza 1 reporte con plantilla",
            "Día 4: Aprende 1 prompt para análisis",
            "Día 5: Presenta resultado a tu jefe",
            "Día 6: Lee sobre tendencias de IA en marketing",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "hr": {
        "title": "ESPECIALISTA DE RECURSOS HUMANOS",
        "tasks": [
            "Buscar y seleccionar candidatos",
            "Adaptar empleados nuevos",
            "Organizar capacitaciones",
            "Gestionar documentación personal"
        ],
        "threats": [
            "IA filtra currículums automáticamente",
            "Chatbots realizan entrevistas iniciales",
            "Generación automática de programas de onboarding",
            "Análisis predictivo de rotación"
        ],
        "safety": [
            "Entrevistas profundas con candidatos",
            "Resolución de conflictos entre empleados",
            "Desarrollo de cultura corporativa",
            "Mentoría y apoyo personal"
        ],
        "tools": [
            "ChatGPT — descripciones de vacantes",
            "Perplexity — benchmarking de salarios",
            "Notion — base de conocimientos de RRHH",
            "Gamma — presentaciones para capacitaciones"
        ],
        "week1": [
            "Día 1: Mapea procesos que consumes más tiempo",
            "Día 2: Automatiza 1 descripción de vacante con IA",
            "Día 3: Crea plantilla de onboarding en Notion",
            "Día 4: Prueba Perplexity para benchmarking",
            "Día 5: Presenta mejora a tu jefe",
            "Día 6: Lee tendencias de IA en RRHH",
            "Día 7: Planifica próxima semana con herramientas IA"
        ]
    },
    "teacher": {
        "title": "DOCENTE / CAPACITADOR",
        "tasks": [
            "Preparar lecciones y materiales",
            "Verificar tareas y exámenes",
            "Crear ejercicios interactivos",
            "Mantenerse actualizado en temas"
        ],
        "threats": [
            "IA genera planes de lección automáticamente",
            "Verificación automática de trabajos",
            "Tutores virtuales disponibles 24/7",
            "Generación de ejercicios por IA"
        ],
        "safety": [
            "Conexión emocional con estudiantes",
            "Adaptación a necesidades individuales",
            "Motivación y mentoría",
            "Evaluación de habilidades blandas"
        ],
        "tools": [
            "ChatGPT — ideas para lecciones",
            "Perplexity — investigación actualizada",
            "Canva — materiales visuales",
            "Notion — planificación del curso"
        ],
        "week1": [
            "Día 1: Lista tareas que consumes más tiempo",
            "Día 2: Genera 1 plan de lección con IA",
            "Día 3: Automatiza 1 ejercicio con plantilla",
            "Día 4: Prueba IA para verificar 5 trabajos",
            "Día 5: Presenta mejora al coordinador",
            "Día 6: Lee sobre IA en educación",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "legal": {
        "title": "ESPECIALISTA LEGAL",
        "tasks": [
            "Revisar contratos y documentos",
            "Consultar a empleados",
            "Seguir cambios legislativos",
            "Preparar posiciones para litigios"
        ],
        "threats": [
            "IA analiza contratos en segundos",
            "Chatbots dan consultas legales básicas",
            "Generación automática de documentos",
            "Monitoreo automático de cambios legales"
        ],
        "safety": [
            "Análisis estratégico de riesgos",
            "Negociación y mediación",
            "Toma de decisiones en casos complejos",
            "Comunicación con partes interesadas"
        ],
        "tools": [
            "ChatGPT — borradores de documentos",
            "Perplexity — investigación legal",
            "Notion — base de conocimientos legal",
            "Claude — análisis de contratos largos"
        ],
        "week1": [
            "Día 1: Lista tipos de documentos que creas",
            "Día 2: Genera 1 borrador de documento con IA",
            "Día 3: Automatiza 1 plantilla de contrato",
            "Día 4: Prueba IA para análisis de contrato",
            "Día 5: Presenta mejora al jefe legal",
            "Día 6: Lee sobre IA en servicios legales",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "finance": {
        "title": "GERENTE DE FINANZAS",
        "tasks": [
            "Preparar reportes financieros",
            "Conciliar cuentas y transacciones",
            "Analizar tendencias y presupuestos",
            "Trabajar con documentación bancaria"
        ],
        "threats": [
            "IA genera reportes automáticamente",
            "Conciliación automática en ERP",
            "Análisis predictivo de flujo de caja",
            "Detección automática de anomalías"
        ],
        "safety": [
            "Estrategia financiera y planificación",
            "Negociación con bancos y partners",
            "Gestión de riesgos complejos",
            "Toma de decisiones bajo incertidumbre"
        ],
        "tools": [
            "ChatGPT — análisis de reportes",
            "Perplexity — investigación de mercado",
            "Excel con IA — automatización",
            "Notion — base de conocimientos"
        ],
        "week1": [
            "Día 1: Lista reportes que preparas manualmente",
            "Día 2: Automatiza 1 reporte recurrente",
            "Día 3: Prueba IA para análisis de datos",
            "Día 4: Crea plantilla de conciliación",
            "Día 5: Presenta resultado al CFO",
            "Día 6: Lee tendencias de IA en finanzas",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "transport": {
        "title": "GERENTE DE TRANSPORTE",
        "tasks": [
            "Preparar documentación de envío",
            "Coordinar logística de entregas",
            "Comunicarse con transportistas",
            "Optimizar rutas de transporte"
        ],
        "threats": [
            "IA optimiza rutas automáticamente",
            "Generación automática de documentos",
            "Tracking automático de cargas",
            "Predicción de demoras por IA"
        ],
        "safety": [
            "Negociación con transportistas",
            "Resolución de problemas urgentes",
            "Relaciones con clientes",
            "Gestión de situaciones imprevistas"
        ],
        "tools": [
            "ChatGPT — comunicaciones con partners",
            "Perplexity — benchmarking de tarifas",
            "Notion — base de rastreo de envíos",
            "Excel IA — optimización de rutas"
        ],
        "week1": [
            "Día 1: Mapea procesos de documentación",
            "Día 2: Automatiza 1 plantilla de envío",
            "Día 3: Prueba IA para optimizar 1 ruta",
            "Día 4: Crea dashboard de seguimiento",
            "Día 5: Presenta mejora al jefe",
            "Día 6: Lee sobre IA en logística",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "procurement": {
        "title": "ESPECIALISTA DE COMPRAS",
        "tasks": [
            "Analizar precios y proveedores",
            "Negociar contratos y condiciones",
            "Preparar documentación de compra",
            "Investigar mercado de materiales"
        ],
        "threats": [
            "IA compara precios automáticamente",
            "Generación automática de RFQ",
            "Análisis predictivo de demanda",
            "Negociación automatizada con proveedores"
        ],
        "safety": [
            "Negociación compleja con proveedores",
            "Evaluación de calidad y riesgos",
            "Construcción de relaciones a largo plazo",
            "Toma de decisiones estratégicas"
        ],
        "tools": [
            "ChatGPT — comparativas de proveedores",
            "Perplexity — investigación de mercado",
            "Notion — base de proveedores",
            "Excel IA — análisis de precios"
        ],
        "week1": [
            "Día 1: Lista procesos que consumes más tiempo",
            "Día 2: Automatiza 1 comparativa de precios",
            "Día 3: Prueba IA para análisis de proveedor",
            "Día 4: Crea plantilla de RFQ",
            "Día 5: Presenta mejora al jefe",
            "Día 6: Lee sobre IA en procurement",
            "Día 7: Planifica semana con herramientas IA"
        ]
    },
    "economist": {
        "title": "ECONOMISTA",
        "tasks": [
            "Analizar indicadores económicos",
            "Preparar reportes financieros",
            "Optimizar costos y procesos",
            "Investigar tendencias de mercado"
        ],
        "threats": [
            "IA genera análisis económico automáticamente",
            "Predicción automática de indicadores",
            "Optimización de costos por algoritmos",
            "Reportes automáticos de tendencias"
        ],
        "safety": [
            "Interpretación cualitativa de datos",
            "Estrategia bajo incertidumbre",
            "Comunicación con stakeholders",
            "Toma de decisiones complejas"
        ],
        "tools": [
            "ChatGPT — análisis de datos",
            "Perplexity — investigación económica",
            "Excel IA — modelado financiero",
            "Notion — base de conocimientos"
        ],
        "week1": [
            "Día 1: Lista reportes que preparas manualmente",
            "Día 2: Automatiza 1 análisis con IA",
            "Día 3: Crea plantilla de reporte",
            "Día 4: Prueba IA para predicción",
            "Día 5: Presenta resultado al jefe",
            "Día 6: Lee sobre IA en economía",
            "Día 7: Planifica semana con herramientas IA"
        ]
    }
}

OUTPUT_DIR = "pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_bold_text(c, x, y, text, font_size=11):
    c.setFont("DejaVu-Bold", font_size)
    c.drawString(x, y, text)
    return c.getStringWidth(text, "DejaVu-Bold", font_size)

def draw_text(c, x, y, text, font_size=10):
    c.setFont("DejaVu", font_size)
    c.drawString(x, y, text)
    return c.getStringWidth(text, "DejaVu", font_size)

def draw_wrapped_text(c, x, y, text, max_width, font_size=10):
    """Simple text wrapping"""
    c.setFont("DejaVu", font_size)
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = c.stringWidth(word + " ", "DejaVu", font_size)
        if current_width + word_width > max_width and current_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width
    
    if current_line:
        lines.append(" ".join(current_line))
    
    for i, line in enumerate(lines):
        c.drawString(x, y - i * (font_size + 2), line)
    
    return len(lines) * (font_size + 2)

def create_pdf(role_key, role_data):
    filename = f"{OUTPUT_DIR}/safemind_survival_guide_es_{role_key}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Colors
    accent = (0.784, 0.294, 0.192)  # #C84B31
    dark = (0.173, 0.243, 0.314)    # #2C3E50
    muted = (0.4, 0.4, 0.4)
    
    # Page 1
    # Header bar
    c.setFillColor(accent)
    c.rect(0, height - 2.5*cm, width, 2.5*cm, fill=1, stroke=0)
    
    c.setFillColor((1,1,1))
    c.setFont("DejaVu-Bold", 16)
    c.drawString(2*cm, height - 1.6*cm, "SafeMind — Guía de Supervivencia IA")
    c.setFont("DejaVu", 10)
    c.drawString(2*cm, height - 2.1*cm, "7 días para hacerte insustituible en la era de la IA")
    
    y = height - 4*cm
    
    # Role title
    c.setFillColor(accent)
    c.setFont("DejaVu-Bold", 18)
    c.drawString(2*cm, y, role_data["title"])
    y -= 1.2*cm
    
    # What you do
    c.setFillColor(dark)
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, y, "¿Qué haces en tu trabajo?")
    y -= 0.8*cm
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    for task in role_data["tasks"]:
        c.drawString(2.5*cm, y, f"• {task}")
        y -= 0.5*cm
    
    y -= 0.5*cm
    
    # Threats
    c.setFillColor((0.8, 0.2, 0.2))
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, y, "⚠️ Amenazas de IA")
    y -= 0.8*cm
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    for threat in role_data["threats"]:
        c.drawString(2.5*cm, y, f"• {threat}")
        y -= 0.5*cm
    
    y -= 0.5*cm
    
    # Safety
    c.setFillColor((0.15, 0.6, 0.3))
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, y, "🛡️ Lo que la IA NO puede reemplazar")
    y -= 0.8*cm
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    for safe in role_data["safety"]:
        c.drawString(2.5*cm, y, f"• {safe}")
        y -= 0.5*cm
    
    y -= 0.5*cm
    
    # Tools
    c.setFillColor(dark)
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, y, "🛠️ Herramientas IA para empezar")
    y -= 0.8*cm
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    for tool in role_data["tools"]:
        c.drawString(2.5*cm, y, f"• {tool}")
        y -= 0.5*cm
    
    # Page 2
    c.showPage()
    
    # Header
    c.setFillColor(accent)
    c.rect(0, height - 1.5*cm, width, 1.5*cm, fill=1, stroke=0)
    c.setFillColor((1,1,1))
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, height - 1*cm, f"SafeMind — Plan de 7 Días para {role_data['title']}")
    
    y = height - 3*cm
    
    c.setFillColor(dark)
    c.setFont("DejaVu-Bold", 14)
    c.drawString(2*cm, y, "📋 Tu Semana 1: De la Supervivencia a la Ventaja")
    y -= 1*cm
    
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    for day in role_data["week1"]:
        wrapped_height = draw_wrapped_text(c, 2.5*cm, y, day, width - 5*cm, 10)
        y -= wrapped_height + 0.4*cm
    
    y -= 0.5*cm
    
    # Teaser
    c.setFillColor(accent)
    c.setFont("DejaVu-Bold", 12)
    c.drawString(2*cm, y, "🚀 ¿Quieres más?")
    y -= 0.6*cm
    c.setFillColor(muted)
    c.setFont("DejaVu", 10)
    teaser_text = "El plan completo de 30 días con mapas detallados, plantillas, scripts de comunicación y check-ins semanales — disponible en SafeMind Pro."
    draw_wrapped_text(c, 2*cm, y, teaser_text, width - 4*cm, 10)
    
    # Footer
    c.setFillColor((0.7, 0.7, 0.7))
    c.setFont("DejaVu", 8)
    c.drawString(2*cm, 1.5*cm, "SafeMind — Mantente Humano en la Era de la IA  |  safemind.pro  |  @SafeMindBot")
    
    c.save()
    print(f"Created: {filename}")

# Generate all PDFs
for role_key, role_data in ROLES.items():
    create_pdf(role_key, role_data)

print(f"\n✅ Done! Generated {len(ROLES)} Spanish PDFs in {OUTPUT_DIR}/")
