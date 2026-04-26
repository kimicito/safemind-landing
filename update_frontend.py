#!/usr/bin/env python3
"""Update frontend JS to use backend API instead of localStorage"""

import re

# New handleLeadMagnet function (EN)
EN_JS = '''// API config
const API_BASE = "https://safemind-backend.onrender.com";

function handleLeadMagnet(e) {
e.preventDefault();
const email = document.getElementById('lmEmail').value;
const role = document.getElementById('lmRole').value;
const lang = 'en';

if(!email || !email.includes('@') || !role) {
alert('Please enter a valid email and select your role');
return;
}

// Show loading
const btn = e.target.querySelector('button[type="submit"]');
const originalText = btn.innerHTML;
btn.innerHTML = '⏳ Sending...';
btn.disabled = true;

// Send to backend
fetch(`${API_BASE}/subscribe`, {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({email, role, lang})
})
.then(r => r.json())
.then(data => {
btn.innerHTML = originalText;
btn.disabled = false;

// Map role to PDF
const roleToPdf = {
'marketing': 'safemind_survival_guide_en_marketing.pdf',
'hr': 'safemind_survival_guide_en_hr.pdf',
'teacher': 'safemind_survival_guide_en_teacher.pdf',
'legal': 'safemind_survival_guide_en_legal.pdf',
'finance': 'safemind_survival_guide_en_finance.pdf',
'transport': 'safemind_survival_guide_en_transport.pdf',
'procurement': 'safemind_survival_guide_en_procurement.pdf',
'economist': 'safemind_survival_guide_en_economist.pdf'
};
const pdfFile = roleToPdf[role] || roleToPdf['marketing'];

// Show success
const successDiv = document.getElementById('lmSuccess');
successDiv.innerHTML = `
<div style="text-align: center; padding: 24px;">
<div style="font-size: 3rem; margin-bottom: 12px;">✅</div>
<h3 style="margin-bottom: 8px;">Check your email!</h3>
<p style="color: var(--muted); margin-bottom: 20px;">Your personalized AI Survival Guide is on its way. If you don't see it in 2 minutes, check your spam folder.</p>
<a href="pdfs/${pdfFile}" download class="btn-primary" style="display: inline-flex; margin-bottom: 16px;">
📥 Download PDF Now
</a>
<div style="background: linear-gradient(135deg, var(--gradient3), var(--gradient4)); border-radius: 12px; padding: 16px; margin-top: 8px;">
<p style="font-size: 0.85rem; color: #fff; margin: 0;">
<strong>Want the full 30-day plan?</strong><br>
Detailed roadmaps, templates, scripts, and weekly check-ins — available in SafeMind Pro.
</p>
<a href="#pricing" class="btn-primary" style="margin-top: 12px; background: #fff; color: var(--accent);" onclick="closeComingSoon()">
See Plans →
</a>
</div>
</div>
`;
successDiv.style.display = 'block';
document.querySelector('.leadmagnet-form').style.display = 'none';
})
.catch(err => {
btn.innerHTML = originalText;
btn.disabled = false;
console.error('Subscribe error:', err);
alert('Something went wrong. Please try again or email us at hello@safemind.pro');
});
}'''

# RU version
RU_JS = '''// API config
const API_BASE = "https://safemind-backend.onrender.com";

function handleLeadMagnet(e) {
e.preventDefault();
const email = document.getElementById('lmEmail').value;
const role = document.getElementById('lmRole').value;
const lang = 'ru';

if(!email || !email.includes('@') || !role) {
alert('Пожалуйста, введите email и выберите роль');
return;
}

// Show loading
const btn = e.target.querySelector('button[type="submit"]');
const originalText = btn.innerHTML;
btn.innerHTML = '⏳ Отправка...';
btn.disabled = true;

// Send to backend
fetch(`${API_BASE}/subscribe`, {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({email, role, lang})
})
.then(r => r.json())
.then(data => {
btn.innerHTML = originalText;
btn.disabled = false;

// Map role to PDF
const roleToPdf = {
'marketing': 'safemind_survival_guide_ru_marketing.pdf',
'hr': 'safemind_survival_guide_ru_hr.pdf',
'teacher': 'safemind_survival_guide_ru_teacher.pdf',
'legal': 'safemind_survival_guide_ru_legal.pdf',
'finance': 'safemind_survival_guide_ru_finance.pdf',
'transport': 'safemind_survival_guide_ru_transport.pdf',
'procurement': 'safemind_survival_guide_ru_procurement.pdf',
'economist': 'safemind_survival_guide_ru_economist.pdf'
};
const pdfFile = roleToPdf[role] || roleToPdf['marketing'];

// Show success
const successDiv = document.getElementById('lmSuccess');
successDiv.innerHTML = `
<div style="text-align: center; padding: 24px;">
<div style="font-size: 3rem; margin-bottom: 12px;">✅</div>
<h3 style="margin-bottom: 8px;">Проверьте email!</h3>
<p style="color: var(--muted); margin-bottom: 20px;">Ваш персональный гид уже в пути. Если не видите письмо через 2 минуты — проверьте папку Спам.</p>
<a href="pdfs/${pdfFile}" download class="btn-primary" style="display: inline-flex; margin-bottom: 16px;">
📥 Скачать PDF сейчас
</a>
<div style="background: linear-gradient(135deg, var(--gradient3), var(--gradient4)); border-radius: 12px; padding: 16px; margin-top: 8px;">
<p style="font-size: 0.85rem; color: #fff; margin: 0;">
<strong>Хотите полный 30-дневный план?</strong><br>
Детальные карты, шаблоны, скрипты и еженедельные чек-ины — в SafeMind Pro.
</p>
<a href="#pricing" class="btn-primary" style="margin-top: 12px; background: #fff; color: var(--accent);" onclick="closeComingSoon()">
Смотреть планы →
</a>
</div>
</div>
`;
successDiv.style.display = 'block';
document.querySelector('.leadmagnet-form').style.display = 'none';
})
.catch(err => {
btn.innerHTML = originalText;
btn.disabled = false;
console.error('Subscribe error:', err);
alert('Что-то пошло не так. Попробуйте снова или напишите нам: hello@safemind.pro');
});
}'''

# ES version
ES_JS = '''// API config
const API_BASE = "https://safemind-backend.onrender.com";

function handleLeadMagnet(e) {
e.preventDefault();
const email = document.getElementById('lmEmail').value;
const role = document.getElementById('lmRole').value;
const lang = 'es';

if(!email || !email.includes('@') || !role) {
alert('Por favor ingresa un email válido y selecciona tu rol');
return;
}

// Show loading
const btn = e.target.querySelector('button[type="submit"]');
const originalText = btn.innerHTML;
btn.innerHTML = '⏳ Enviando...';
btn.disabled = true;

// Send to backend
fetch(`${API_BASE}/subscribe`, {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({email, role, lang})
})
.then(r => r.json())
.then(data => {
btn.innerHTML = originalText;
btn.disabled = false;

// Map role to PDF
const roleToPdf = {
'marketing': 'safemind_survival_guide_es_marketing.pdf',
'hr': 'safemind_survival_guide_es_hr.pdf',
'teacher': 'safemind_survival_guide_es_teacher.pdf',
'legal': 'safemind_survival_guide_es_legal.pdf',
'finance': 'safemind_survival_guide_es_finance.pdf',
'transport': 'safemind_survival_guide_es_transport.pdf',
'procurement': 'safemind_survival_guide_es_procurement.pdf',
'economist': 'safemind_survival_guide_es_economist.pdf'
};
const pdfFile = roleToPdf[role] || roleToPdf['marketing'];

// Show success
const successDiv = document.getElementById('lmSuccess');
successDiv.innerHTML = `
<div style="text-align: center; padding: 24px;">
<div style="font-size: 3rem; margin-bottom: 12px;">✅</div>
<h3 style="margin-bottom: 8px;">¡Revisa tu email!</h3>
<p style="color: var(--muted); margin-bottom: 20px;">Tu guía personalizada está en camino. Si no la ves en 2 minutos, revisa tu carpeta de spam.</p>
<a href="pdfs/${pdfFile}" download class="btn-primary" style="display: inline-flex; margin-bottom: 16px;">
📥 Descargar PDF ahora
</a>
<div style="background: linear-gradient(135deg, var(--gradient3), var(--gradient4)); border-radius: 12px; padding: 16px; margin-top: 8px;">
<p style="font-size: 0.85rem; color: #fff; margin: 0;">
<strong>¿Quieres el plan completo de 30 días?</strong><br>
Mapas detallados, plantillas, scripts y check-ins semanales — en SafeMind Pro.
</p>
<a href="#pricing" class="btn-primary" style="margin-top: 12px; background: #fff; color: var(--accent);" onclick="closeComingSoon()">
Ver planes →
</a>
</div>
</div>
`;
successDiv.style.display = 'block';
document.querySelector('.leadmagnet-form').style.display = 'none';
})
.catch(err => {
btn.innerHTML = originalText;
btn.disabled = false;
console.error('Subscribe error:', err);
alert('Algo salió mal. Por favor intenta de nuevo o escríbenos: hello@safemind.pro');
});
}'''

def replace_in_file(filepath, new_js):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find and replace the handleLeadMagnet function
    pattern = r'function handleLeadMagnet\(e\) \{.*?document\.querySelector\(\'\.leadmagnet-form\'\)\.style\.display = \'none\';\n\}'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_js, content, count=1, flags=re.DOTALL)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {filepath}")
    else:
        print(f"❌ Pattern not found in: {filepath}")

replace_in_file('/root/.openclaw/workspace/safemind/en/index.html', EN_JS)
replace_in_file('/root/.openclaw/workspace/safemind/ru/index.html', RU_JS)
replace_in_file('/root/.openclaw/workspace/safemind/es/index.html', ES_JS)
