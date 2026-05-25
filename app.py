from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "bedrock-paraguay-2024"

LEADS_CSV  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.csv")
ADMIN_PASS = "bedrock2030"   # ← CHANGE THIS to your own password

# ── Translations ───────────────────────────────────────────────────────────────
T = {
 "en": {
  "nav_home":"Home","nav_services":"Services","nav_contact":"Contact",
  "hero_title":"Starting Fresh in Paraguay?",
  "hero_sub":"BEDROCK helps immigrants navigate residency, banking, and business — in your language, with zero surprises.",
  "hero_btn":"Free Consultation →",
  "why_title":"Why BEDROCK?",
  "w1t":"Your Language","w1b":"English, Portuguese, Spanish, French, Italian. No language barrier ever.",
  "w2t":"No Hidden Fees","w2b":"Fixed transparent prices before we start. You know every cost upfront.",
  "w3t":"End-to-End Support","w3b":"Documents, appointments, translations, follow-ups — all handled by us.",
  "w4t":"Zero Scam Risk","w4b":"Licensed, referenced service. We work only when you are comfortable.",
  "services_title":"What We Help With",
  "cta_title":"Ready to Start?","cta_sub":"Book a free 30-minute consultation. No commitment.",
  "cta_btn":"Contact Us Now →",
  "contact_title":"Free Consultation Request",
  "contact_name":"Full Name","contact_email":"Email Address",
  "contact_phone":"Phone / WhatsApp","contact_nationality":"Nationality / Country",
  "contact_service":"What do you need help with?","contact_msg":"Tell us more (optional)",
  "contact_btn":"Send Request","contact_ok":"✅ Received! We will contact you within 24 hours.",
  "footer_tag":"Your foundation in Paraguay. | Lambaré, Paraguay",
  "admin_title":"BEDROCK Leads","admin_logout":"Logout",
  "login_title":"Admin Access","login_btn":"Login",
 },
 "pt": {
  "nav_home":"Início","nav_services":"Serviços","nav_contact":"Contato",
  "hero_title":"Recomeçando no Paraguai?",
  "hero_sub":"A BEDROCK ajuda imigrantes com residência, conta bancária e negócios — no seu idioma, sem surpresas.",
  "hero_btn":"Consulta Gratuita →",
  "why_title":"Por que a BEDROCK?",
  "w1t":"Seu Idioma","w1b":"Português, inglês, espanhol, francês e italiano. Zero barreira de idioma.",
  "w2t":"Sem Taxas Ocultas","w2b":"Preços fixos e claros antes de começar. Você sabe tudo que vai pagar.",
  "w3t":"Suporte Completo","w3b":"Documentos, agendamentos, traduções e acompanhamento — tudo por nós.",
  "w4t":"Zero Golpes","w4b":"Serviço licenciado e referenciado. Trabalhamos só quando você estiver confortável.",
  "services_title":"Com o que Ajudamos",
  "cta_title":"Pronto para Começar?","cta_sub":"Agende uma consulta gratuita de 30 minutos. Sem compromisso.",
  "cta_btn":"Fale Conosco →",
  "contact_title":"Solicite uma Consulta Gratuita",
  "contact_name":"Nome Completo","contact_email":"E-mail",
  "contact_phone":"Telefone / WhatsApp","contact_nationality":"Nacionalidade / País",
  "contact_service":"Com o que você precisa de ajuda?","contact_msg":"Conte-nos mais (opcional)",
  "contact_btn":"Enviar Solicitação","contact_ok":"✅ Recebido! Entraremos em contato em até 24 horas.",
  "footer_tag":"Sua base no Paraguai. | Lambaré, Paraguai",
  "admin_title":"BEDROCK Leads","admin_logout":"Sair",
  "login_title":"Acesso Admin","login_btn":"Entrar",
 },
 "es": {
  "nav_home":"Inicio","nav_services":"Servicios","nav_contact":"Contacto",
  "hero_title":"¿Empezando de Nuevo en Paraguay?",
  "hero_sub":"BEDROCK ayuda a inmigrantes con residencia, cuenta bancaria y negocios — en tu idioma, sin sorpresas.",
  "hero_btn":"Consulta Gratuita →",
  "why_title":"¿Por qué BEDROCK?",
  "w1t":"Tu Idioma","w1b":"Inglés, portugués, español, francés e italiano. Sin barrera de idioma.",
  "w2t":"Sin Costos Ocultos","w2b":"Precios fijos antes de empezar. Sabes exactamente cuánto pagas.",
  "w3t":"Apoyo Completo","w3b":"Documentos, citas, traducciones y seguimiento — todo lo manejamos.",
  "w4t":"Cero Estafas","w4b":"Servicio con licencia y referencias. Solo trabajamos cuando estés seguro.",
  "services_title":"En Qué Te Ayudamos",
  "cta_title":"¿Listo para Empezar?","cta_sub":"Agenda una consulta gratuita de 30 minutos. Sin compromiso.",
  "cta_btn":"Contáctanos Ahora →",
  "contact_title":"Solicita una Consulta Gratuita",
  "contact_name":"Nombre Completo","contact_email":"Correo Electrónico",
  "contact_phone":"Teléfono / WhatsApp","contact_nationality":"Nacionalidad / País",
  "contact_service":"¿Con qué necesitas ayuda?","contact_msg":"Cuéntanos más (opcional)",
  "contact_btn":"Enviar Solicitud","contact_ok":"✅ ¡Recibido! Te contactaremos en menos de 24 horas.",
  "footer_tag":"Tu base en Paraguay. | Lambaré, Paraguay",
  "admin_title":"BEDROCK Leads","admin_logout":"Cerrar sesión",
  "login_title":"Acceso Admin","login_btn":"Ingresar",
 },
}

SERVICES = {
 "en": [
  {"icon":"🏠","title":"Temporary & Permanent Residency","desc":"Complete guidance from document prep to final approval. We know every requirement."},
  {"icon":"🏦","title":"Bank Account Opening","desc":"Open personal or business accounts at major Paraguayan banks — no language barrier."},
  {"icon":"🏢","title":"Business Registration","desc":"Register your company, get your RUC tax ID, and operate legally from day one."},
  {"icon":"📄","title":"Document Translation","desc":"Certified translations + apostille + notarization. All accepted by Paraguayan authorities."},
  {"icon":"🏡","title":"Real Estate Assistance","desc":"Find safe housing or land with legal verification. No risk of fraud."},
  {"icon":"⚖️","title":"Legal Consultation","desc":"We connect you with vetted, English/Portuguese-speaking immigration lawyers."},
  {"icon":"🧾","title":"Tax Registration (RUC)","desc":"Register with Tributación as freelancer or company owner. Stay fully compliant."},
  {"icon":"🎓","title":"School Enrollment","desc":"We help families enroll children in schools and navigate the education system."},
 ],
 "pt": [
  {"icon":"🏠","title":"Residência Temporária e Permanente","desc":"Orientação completa desde a preparação de documentos até a aprovação final."},
  {"icon":"🏦","title":"Abertura de Conta Bancária","desc":"Abra conta pessoal ou empresarial nos principais bancos paraguaios sem barreira de idioma."},
  {"icon":"🏢","title":"Abertura de Empresa","desc":"Registre sua empresa, obtenha o RUC e opere legalmente desde o primeiro dia."},
  {"icon":"📄","title":"Tradução de Documentos","desc":"Traduções certificadas + apostila + reconhecimento de firma aceitos pelas autoridades paraguaias."},
  {"icon":"🏡","title":"Auxílio Imobiliário","desc":"Encontre moradia ou terreno seguro com verificação jurídica. Sem risco de golpe."},
  {"icon":"⚖️","title":"Consultoria Jurídica","desc":"Conectamos você a advogados de imigração que falam português."},
  {"icon":"🧾","title":"Registro Tributário (RUC)","desc":"Cadastro na Subsecretaria de Tributação como autônomo ou empresário."},
  {"icon":"🎓","title":"Matrícula Escolar","desc":"Ajudamos famílias a matricular filhos e navegar pelo sistema de ensino paraguaio."},
 ],
 "es": [
  {"icon":"🏠","title":"Residencia Temporal y Permanente","desc":"Guía completa desde la preparación de documentos hasta la aprobación final."},
  {"icon":"🏦","title":"Apertura de Cuenta Bancaria","desc":"Abre cuentas personales o empresariales en bancos paraguayos sin barreras de idioma."},
  {"icon":"🏢","title":"Registro de Empresa","desc":"Registra tu empresa, obtén tu RUC y opera legalmente desde el primer día."},
  {"icon":"📄","title":"Traducción de Documentos","desc":"Traducciones certificadas + apostilla + notarización aceptadas por las autoridades."},
  {"icon":"🏡","title":"Asistencia Inmobiliaria","desc":"Encuentra vivienda o terreno seguro con verificación legal. Sin riesgo de estafa."},
  {"icon":"⚖️","title":"Consulta Jurídica","desc":"Te conectamos con abogados de inmigración que hablan tu idioma."},
  {"icon":"🧾","title":"Registro Tributario (RUC)","desc":"Registro en Tributación como autónomo o dueño de empresa."},
  {"icon":"🎓","title":"Matrícula Escolar","desc":"Ayudamos a familias a inscribir a sus hijos y navegar el sistema educativo paraguayo."},
 ],
}

SERVICE_OPTIONS = {
 "en": ["Residency Permit","Bank Account Opening","Business Registration","Document Translation","Real Estate Help","Legal Consultation","Tax Registration (RUC)","School Enrollment","Other"],
 "pt": ["Residência","Abertura de Conta","Abertura de Empresa","Tradução de Documentos","Imóveis","Consultoria Jurídica","RUC Tributário","Matrícula Escolar","Outro"],
 "es": ["Residencia","Apertura de Cuenta","Registro de Empresa","Traducción de Documentos","Bienes Raíces","Consulta Jurídica","Registro RUC","Matrícula Escolar","Otro"],
}

LANGS = {"en":"English","pt":"Português","es":"Español"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def get_lang():
    return session.get("lang","en")

def init_csv():
    if not os.path.exists(LEADS_CSV):
        with open(LEADS_CSV,"w",newline="",encoding="utf-8-sig") as f:
            csv.DictWriter(f,fieldnames=["date","name","email","phone","nationality","service","message","lang"]).writeheader()

init_csv()

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/lang/<code>")
def set_lang(code):
    if code in LANGS:
        session["lang"] = code
    return redirect(request.referrer or url_for("index"))

@app.route("/")
def index():
    lg = get_lang()
    return render_template("index.html", t=T[lg], services=SERVICES[lg][:4], langs=LANGS, lang=lg)

@app.route("/services")
def services():
    lg = get_lang()
    return render_template("services.html", t=T[lg], services=SERVICES[lg], langs=LANGS, lang=lg)

@app.route("/contact", methods=["GET","POST"])
def contact():
    lg = get_lang()
    success = False
    if request.method == "POST":
        row = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "name": request.form.get("name",""),
            "email": request.form.get("email",""),
            "phone": request.form.get("phone",""),
            "nationality": request.form.get("nationality",""),
            "service": request.form.get("service",""),
            "message": request.form.get("message",""),
            "lang": lg,
        }
        with open(LEADS_CSV,"a",newline="",encoding="utf-8-sig") as f:
            csv.DictWriter(f,fieldnames=row.keys()).writerow(row)
        success = True
    return render_template("contact.html", t=T[lg], service_options=SERVICE_OPTIONS[lg], langs=LANGS, lang=lg, success=success)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
        return redirect(url_for("admin"))
    if not session.get("admin"):
       return render_template(
    "admin_login.html",
    t=T["en"],
    langs=LANGS
)
    leads = []
    if os.path.exists(LEADS_CSV):
        with open(LEADS_CSV,"r",encoding="utf-8-sig") as f:
            leads = list(csv.DictReader(f))
    leads.reverse()  # newest first
    return render_template("admin.html", t=T["en"], leads=leads, total=len(leads), langs=LANGS)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  BEDROCK is running!")
    print("  Open your browser → http://localhost:5000")
    print("  Admin panel      → http://localhost:5000/admin")
    print("="*50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
