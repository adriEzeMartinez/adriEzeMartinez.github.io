#!/usr/bin/env python3
"""Generador del sitio trilingüe aemartinez.com (ES en la raíz, EN en /en/, IT en /it/).

Uso:  python3 generate.py <carpeta_de_salida>
Para cambiar un texto, editá el diccionario T y volvé a ejecutar.
"""
import posixpath
import sys
from pathlib import Path

BASE = "https://aemartinez.com"
# >>> Reemplazá por tu endpoint real de Formspree (el mismo que ya usás en el repo) <<<
FORMSPREE = "https://formspree.io/f/mlgqjbye"
GOATCOUNTER = "https://aemartinez.goatcounter.com/count"
EMAIL = "adri.eze.martinez@gmail.com"
LINKEDIN = "linkedin.com/in/adrianemartinez"

LANGS = ["es", "en", "it"]
LANG_LABEL = {"es": "ES", "en": "EN", "it": "IT"}
OG_LOCALE = {"es": "es_ES", "en": "en_GB", "it": "it_IT"}
LANG_NAME = {"es": "Español", "en": "English", "it": "Italiano"}

# Banderas en SVG inline (los emojis de bandera no se ven en Windows)
FLAGS = {
    "es": '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true" focusable="false"><rect width="3" height="2" fill="#AA151B"/><rect y="0.5" width="3" height="1" fill="#F1BF00"/></svg>',
    "it": '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true" focusable="false"><rect width="1" height="2" fill="#009246"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#CE2B37"/></svg>',
    "en": '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true" focusable="false"><clipPath id="uk-s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="uk-t"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath><g clip-path="url(#uk-s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#uk-t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
}

# Ruta (relativa a la raíz del sitio) de cada página en cada idioma
PATHS = {
    "es": {"home": "", "services": "servicios.html", "about": "sobre-mi.html", "contact": "contacto.html"},
    "en": {"home": "en/", "services": "en/services.html", "about": "en/about.html", "contact": "en/contact.html"},
    "it": {"home": "it/", "services": "it/servizi.html", "about": "it/chi-sono.html", "contact": "it/contatti.html"},
}
PAGES = ["home", "services", "about", "contact"]

FRAMEWORKS_1 = "ISO 27001 · ISO 20000 · NIS2 · DORA · ENS · GDPR/LOPDGDD"
FRAMEWORKS_2 = "Magerit v3 · ISO 27005 · ISO 31000"

T = {
    "es": {
        "html_lang": "es",
        "nav": {"services": "Servicios", "about": "Sobre mí", "contact": "Contacto"},
        "nav_label": "Navegación principal",
        "lang_label": "Idioma",
        "footer": "Auditor de Ciberseguridad y Cumplimiento Normativo",
        "home": {
            "title": "Adrián Martínez — Auditoría de Ciberseguridad y Cumplimiento",
            "desc": "Auditoría de ciberseguridad y cumplimiento normativo: ISO 27001, NIS2, DORA, ENS, GDPR. Lead Auditor certificado AENOR.",
            "h1": "Auditoría de ciberseguridad y cumplimiento normativo",
            "lead": "Más de 5 años auditando y asesorando en Governance, Risk &amp; Compliance para banca de inversión, telecomunicaciones y consultoras tecnológicas de primer nivel en Europa. Lead Auditor certificado AENOR.",
            "cta": "Solicitar consultoría",
            "intro_title": "Especialista en GRC y ciberseguridad",
            "intro": "Especialista en Governance, Risk &amp; Compliance (GRC) y ciberseguridad, con experiencia auditando organizaciones del sector financiero, telecomunicaciones y consultoría enterprise en distintos países de Europa. Combino formación técnica en seguridad y desarrollo con certificaciones de auditor líder para ofrecer evaluaciones rigurosas y planes de acción concretos.",
            "intro_btn": "Conocer los servicios",
            "schema_desc": "Auditoría de ciberseguridad y cumplimiento normativo: ISO 27001, NIS2, DORA, ENS, GDPR.",
            "job": "Auditor de Ciberseguridad y Cumplimiento Normativo",
        },
        "services": {
            "title": "Servicios — Adrián Martínez",
            "desc": "Auditoría de cumplimiento, consultoría GRC, análisis forense digital y automatización de evidencias.",
            "h2": "Servicios",
            "sub": "Auditoría, consultoría y análisis forense orientados a que tu organización cumpla con los principales marcos normativos de ciberseguridad y protección de datos, y llegue preparada a cualquier auditoría externa.",
            "ideal": "Ideal para:",
            "cta": "Solicitar consultoría",
            "items": [
                (FRAMEWORKS_1, "Auditoría de cumplimiento normativo",
                 "Evaluación integral de tus controles de seguridad frente a los requisitos normativos aplicables. Identificación de brechas (gap analysis), revisión de evidencia documental y preparación exhaustiva para auditorías externas de certificación o supervisión regulatoria.",
                 "entidades financieras, operadores críticos, empresas tecnológicas que necesitan certificarse o mantener el cumplimiento vigente."),
                (FRAMEWORKS_2, "Consultoría GRC",
                 "Diseño e implementación de políticas de seguridad, marcos de gestión de riesgos y documentación de controles. Acompañamiento continuo para que el cumplimiento normativo forme parte de la operación diaria, no solo de un momento puntual antes de una auditoría.",
                 "organizaciones que están construyendo o madurando su programa de seguridad y compliance."),
                ("Perito Forense Informático — UNIR", "Análisis y peritaje forense digital",
                 "Investigaciones forenses ante incidentes de seguridad, fraude o disputas que requieren evidencia técnica válida. Metodología certificada aplicada con rigurosidad pericial.",
                 "empresas que enfrentan un incidente, necesitan evidencia para un proceso legal, o requieren una investigación independiente."),
                ("Python · automatización de evidencias", "Automatización de evidencias y reportes",
                 "Desarrollo de herramientas propias en Python para automatizar la recolección de evidencia, el análisis de logs y la generación de reportes de cumplimiento. Reduce el tiempo y el margen de error de los procesos manuales de auditoría interna.",
                 "equipos de compliance o seguridad que gestionan auditorías recurrentes y quieren optimizar el proceso."),
            ],
        },
        "about": {
            "title": "Sobre mí — Adrián Martínez",
            "desc": "Trayectoria, certificaciones y formación de Adrián Martínez, auditor GRC y ciberseguridad.",
            "h2": "Sobre mí",
            "intro": "Soy Adrián Martínez, Auditor de Ciberseguridad y Cumplimiento Normativo, Lead Auditor certificado por AENOR en ISO 27001, ISO 20000 y NIS2. Mi trabajo combina una base técnica sólida en seguridad y desarrollo de software con más de cinco años de experiencia auditando y asesorando organizaciones en materia de Governance, Risk &amp; Compliance.",
            "timeline": [
                ("Banca de inversión — GRC &amp; Security Engineer", "Validación de cumplimiento normativo (DORA, NIS2, ISO 27001), análisis de activos de información críticos y revisión de arquitecturas de seguridad."),
                ("Consultoría tecnológica europea — Consultor Senior GRC", "Asesoría a clientes enterprise en ISO 27001/27002/27005, ENS y GDPR, coordinando stakeholders en múltiples países."),
                ("Infraestructura cloud — Cloud Security &amp; DevSecOps", "Hardening de infraestructura Azure/AWS y participación en ejercicios de Red/Blue/Purple Team para simular ataques a gran escala."),
                ("Gestión de incidentes", "Triage de incidentes (N1/N2) mediante monitoreo de logs y alertas, reportando directamente a comités de dirección (CEO/CISO)."),
                ("Docencia universitaria", "Profesor en la Licenciatura en Ciberseguridad de la Universidad de Palermo — Seguridad en Aplicaciones Web / Hacking de Aplicaciones, Arquitectura Web, Seguridad de Redes y Seguridad Ofensiva."),
            ],
            "certs_title": "Certificaciones y formación",
            "certs": [
                ("AENOR", "Lead Auditor ISO 27001, ISO 20000, NIS2"),
                ("AENOR", "Gestión de Riesgos de Seguridad de la Información"),
                ("UNIR", "Perito Forense Informático certificado"),
                ("Universidad de Palermo", "Licenciatura en Ciberseguridad"),
                ("Universidad de Palermo", "Ingeniería en Informática"),
                ("EF SET", "Inglés C1 Advanced"),
            ],
        },
        "contact": {
            "title": "Contacto — Adrián Martínez",
            "desc": "Contactá a Adrián Martínez para auditorías de cumplimiento, consultoría GRC o análisis forense.",
            "h2": "Contacto",
            "sub": "¿Necesitás auditar el cumplimiento de tu organización frente a ISO 27001, NIS2, DORA u otro marco normativo? ¿Tenés un incidente que requiere análisis forense? Conversemos.",
            "name": "Nombre", "company": "Empresa", "email": "Email", "message": "Mensaje",
            "send": "Enviar mensaje", "linkedin": "LinkedIn",
        },
    },
    "en": {
        "html_lang": "en",
        "nav": {"services": "Services", "about": "About", "contact": "Contact"},
        "nav_label": "Main navigation",
        "lang_label": "Language",
        "footer": "Cybersecurity &amp; Regulatory Compliance Auditor",
        "home": {
            "title": "Adrián Martínez — Cybersecurity Audit &amp; Compliance",
            "desc": "Cybersecurity audit and regulatory compliance: ISO 27001, NIS2, DORA, ENS, GDPR. AENOR-certified Lead Auditor.",
            "h1": "Cybersecurity audit and regulatory compliance",
            "lead": "Over 5 years auditing and advising on Governance, Risk &amp; Compliance for investment banking, telecommunications and leading technology consultancies across Europe. AENOR-certified Lead Auditor.",
            "cta": "Request a consultation",
            "intro_title": "GRC and cybersecurity specialist",
            "intro": "Specialist in Governance, Risk &amp; Compliance (GRC) and cybersecurity, with experience auditing organisations in the financial, telecommunications and enterprise consulting sectors across Europe. I combine hands-on technical training in security and software development with lead auditor certifications to deliver rigorous assessments and concrete action plans.",
            "intro_btn": "Explore the services",
            "schema_desc": "Cybersecurity audit and regulatory compliance: ISO 27001, NIS2, DORA, ENS, GDPR.",
            "job": "Cybersecurity and Regulatory Compliance Auditor",
        },
        "services": {
            "title": "Services — Adrián Martínez",
            "desc": "Compliance audit, GRC consulting, digital forensics and evidence automation.",
            "h2": "Services",
            "sub": "Audit, consulting and forensic analysis to help your organisation meet the main cybersecurity and data protection frameworks and arrive prepared for any external audit.",
            "ideal": "Ideal for:",
            "cta": "Request a consultation",
            "items": [
                (FRAMEWORKS_1, "Regulatory compliance audit",
                 "A comprehensive assessment of your security controls against the applicable regulatory requirements. Gap analysis, review of documentary evidence and thorough preparation for external certification audits or regulatory supervision.",
                 "financial institutions, critical operators and technology companies that need to certify or maintain ongoing compliance."),
                (FRAMEWORKS_2, "GRC consulting",
                 "Design and implementation of security policies, risk management frameworks and controls documentation. Ongoing support so that regulatory compliance becomes part of day-to-day operations, not just a one-off effort before an audit.",
                 "organisations building or maturing their security and compliance programme."),
                ("Certified Forensic Computing Expert — UNIR", "Digital forensics and expert analysis",
                 "Forensic investigations following security incidents, fraud or disputes that require technically valid evidence. Certified methodology applied with expert rigour.",
                 "companies facing an incident, needing evidence for legal proceedings, or requiring an independent investigation."),
                ("Python · evidence automation", "Evidence and compliance reporting automation",
                 "Custom Python tooling to automate evidence collection, log analysis and compliance report generation. Cuts the time and error rate of manual internal audit processes.",
                 "compliance or security teams running recurring audits that want to streamline the process."),
            ],
        },
        "about": {
            "title": "About — Adrián Martínez",
            "desc": "Career, certifications and education of Adrián Martínez, GRC and cybersecurity auditor.",
            "h2": "About me",
            "intro": "I'm Adrián Martínez, Cybersecurity and Regulatory Compliance Auditor and AENOR-certified Lead Auditor for ISO 27001, ISO 20000 and NIS2. My work combines a solid technical background in security and software development with more than five years of experience auditing and advising organisations on Governance, Risk &amp; Compliance.",
            "timeline": [
                ("Investment banking — GRC &amp; Security Engineer", "Regulatory compliance validation (DORA, NIS2, ISO 27001), analysis of critical information assets and security architecture reviews."),
                ("European technology consultancy — Senior GRC Consultant", "Advising enterprise clients on ISO 27001/27002/27005, ENS and GDPR, coordinating stakeholders across multiple countries."),
                ("Cloud infrastructure — Cloud Security &amp; DevSecOps", "Azure/AWS infrastructure hardening and participation in Red/Blue/Purple Team exercises simulating large-scale attacks."),
                ("Incident management", "Incident triage (L1/L2) through log and alert monitoring, reporting directly to executive committees (CEO/CISO)."),
                ("University teaching", "Professor in the Bachelor's Degree in Cybersecurity at Universidad de Palermo — Web Application Security / Application Hacking, Web Architecture, Network Security and Offensive Security."),
            ],
            "certs_title": "Certifications and education",
            "certs": [
                ("AENOR", "Lead Auditor ISO 27001, ISO 20000, NIS2"),
                ("AENOR", "Information Security Risk Management"),
                ("UNIR", "Certified Computer Forensics Expert"),
                ("Universidad de Palermo", "Bachelor's Degree in Cybersecurity"),
                ("Universidad de Palermo", "Computer Engineering"),
                ("EF SET", "English C1 Advanced"),
            ],
        },
        "contact": {
            "title": "Contact — Adrián Martínez",
            "desc": "Get in touch with Adrián Martínez for compliance audits, GRC consulting or digital forensics.",
            "h2": "Contact",
            "sub": "Do you need to audit your organisation's compliance against ISO 27001, NIS2, DORA or another framework? Facing an incident that requires forensic analysis? Let's talk.",
            "name": "Name", "company": "Company", "email": "Email", "message": "Message",
            "send": "Send message", "linkedin": "LinkedIn",
        },
    },
    "it": {
        "html_lang": "it",
        "nav": {"services": "Servizi", "about": "Chi sono", "contact": "Contatti"},
        "nav_label": "Navigazione principale",
        "lang_label": "Lingua",
        "footer": "Auditor di Cybersecurity e Conformità Normativa",
        "home": {
            "title": "Adrián Martínez — Audit di Cybersecurity e Conformità",
            "desc": "Audit di cybersecurity e conformità normativa: ISO 27001, NIS2, DORA, ENS, GDPR. Lead Auditor certificato AENOR.",
            "h1": "Audit di cybersecurity e conformità normativa",
            "lead": "Oltre 5 anni di esperienza nell'audit e nella consulenza in Governance, Risk &amp; Compliance per investment banking, telecomunicazioni e primarie società di consulenza tecnologica in Europa. Lead Auditor certificato AENOR.",
            "cta": "Richiedi una consulenza",
            "intro_title": "Specialista in GRC e cybersecurity",
            "intro": "Specialista in Governance, Risk &amp; Compliance (GRC) e cybersecurity, con esperienza nell'audit di organizzazioni del settore finanziario, delle telecomunicazioni e della consulenza enterprise in diversi paesi europei. Unisco una solida formazione tecnica in sicurezza e sviluppo software alle certificazioni di lead auditor per offrire valutazioni rigorose e piani d'azione concreti.",
            "intro_btn": "Scopri i servizi",
            "schema_desc": "Audit di cybersecurity e conformità normativa: ISO 27001, NIS2, DORA, ENS, GDPR.",
            "job": "Auditor di Cybersecurity e Conformità Normativa",
        },
        "services": {
            "title": "Servizi — Adrián Martínez",
            "desc": "Audit di conformità, consulenza GRC, analisi forense digitale e automazione delle evidenze.",
            "h2": "Servizi",
            "sub": "Audit, consulenza e analisi forense per aiutare la tua organizzazione a rispettare i principali standard di cybersecurity e protezione dei dati e ad arrivare preparata a qualsiasi audit esterno.",
            "ideal": "Ideale per:",
            "cta": "Richiedi una consulenza",
            "items": [
                (FRAMEWORKS_1, "Audit di conformità normativa",
                 "Valutazione completa dei tuoi controlli di sicurezza rispetto ai requisiti normativi applicabili. Gap analysis, revisione delle evidenze documentali e preparazione approfondita agli audit esterni di certificazione o di vigilanza regolamentare.",
                 "istituti finanziari, operatori critici e aziende tecnologiche che devono certificarsi o mantenere la conformità nel tempo."),
                (FRAMEWORKS_2, "Consulenza GRC",
                 "Progettazione e implementazione di policy di sicurezza, framework di gestione del rischio e documentazione dei controlli. Un affiancamento continuo perché la conformità normativa diventi parte dell'operatività quotidiana e non solo uno sforzo puntuale prima di un audit.",
                 "organizzazioni che stanno costruendo o rafforzando il proprio programma di sicurezza e compliance."),
                ("Perito Informatico Forense Certificato — UNIR", "Analisi e perizia forense digitale",
                 "Indagini forensi a seguito di incidenti di sicurezza, frodi o controversie che richiedono evidenze tecniche valide. Metodologia certificata applicata con rigore peritale.",
                 "aziende che affrontano un incidente, necessitano di prove per un procedimento legale o di un'indagine indipendente."),
                ("Python · automazione delle evidenze", "Automazione di evidenze e report di compliance",
                 "Sviluppo di strumenti Python su misura per automatizzare la raccolta delle evidenze, l'analisi dei log e la generazione dei report di conformità. Riduce tempi ed errori dei processi manuali di audit interno.",
                 "team di compliance o sicurezza che gestiscono audit ricorrenti e vogliono ottimizzare il processo."),
            ],
        },
        "about": {
            "title": "Chi sono — Adrián Martínez",
            "desc": "Percorso, certificazioni e formazione di Adrián Martínez, auditor GRC e cybersecurity.",
            "h2": "Chi sono",
            "intro": "Sono Adrián Martínez, Auditor di Cybersecurity e Conformità Normativa, Lead Auditor certificato AENOR per ISO 27001, ISO 20000 e NIS2. Il mio lavoro unisce una solida base tecnica in sicurezza e sviluppo software a oltre cinque anni di esperienza nell'audit e nella consulenza alle organizzazioni in materia di Governance, Risk &amp; Compliance.",
            "timeline": [
                ("Investment banking — GRC &amp; Security Engineer", "Validazione della conformità normativa (DORA, NIS2, ISO 27001), analisi degli asset informativi critici e revisione delle architetture di sicurezza."),
                ("Consulenza tecnologica europea — Senior GRC Consultant", "Consulenza a clienti enterprise su ISO 27001/27002/27005, ENS e GDPR, coordinando stakeholder in più paesi."),
                ("Infrastruttura cloud — Cloud Security &amp; DevSecOps", "Hardening dell'infrastruttura Azure/AWS e partecipazione a esercitazioni Red/Blue/Purple Team che simulano attacchi su larga scala."),
                ("Gestione degli incidenti", "Triage degli incidenti (L1/L2) tramite monitoraggio di log e alert, con reporting diretto ai comitati di direzione (CEO/CISO)."),
                ("Docenza universitaria", "Professore nel corso di laurea in Cybersecurity della Universidad de Palermo — Sicurezza delle Applicazioni Web / Hacking di Applicazioni, Architettura Web, Sicurezza di Rete e Sicurezza Offensiva."),
            ],
            "certs_title": "Certificazioni e formazione",
            "certs": [
                ("AENOR", "Lead Auditor ISO 27001, ISO 20000, NIS2"),
                ("AENOR", "Gestione del Rischio per la Sicurezza delle Informazioni"),
                ("UNIR", "Perito Informatico Forense certificato"),
                ("Universidad de Palermo", "Laurea in Cybersecurity"),
                ("Universidad de Palermo", "Ingegneria Informatica"),
                ("EF SET", "Inglese C1 Advanced"),
            ],
        },
        "contact": {
            "title": "Contatti — Adrián Martínez",
            "desc": "Contatta Adrián Martínez per audit di conformità, consulenza GRC o analisi forense digitale.",
            "h2": "Contatti",
            "sub": "Devi verificare la conformità della tua organizzazione a ISO 27001, NIS2, DORA o ad altri standard? Hai un incidente che richiede un'analisi forense? Parliamone.",
            "name": "Nome", "company": "Azienda", "email": "Email", "message": "Messaggio",
            "send": "Invia messaggio", "linkedin": "LinkedIn",
        },
    },
}

CHIPS = ["ISO 27001", "ISO 20000", "NIS2", "DORA", "ENS", "GDPR / LOPDGDD"]


def url(lang, page):
    return f"{BASE}/{PATHS[lang][page]}"


_CUR = {"lang": "es", "page": "home"}  # página que se está generando (para rutas relativas)


def _file_of(lang, page):
    p = PATHS[lang][page] or "index.html"
    return p + "index.html" if p.endswith("/") else p


def href(lang, page):
    """Ruta RELATIVA desde la página actual: funciona abriendo los archivos desde disco y en cualquier servidor."""
    cur_dir = posixpath.dirname(_file_of(_CUR["lang"], _CUR["page"])) or "."
    return posixpath.relpath(_file_of(lang, page), start=cur_dir)


def asset(name):
    cur_dir = posixpath.dirname(_file_of(_CUR["lang"], _CUR["page"])) or "."
    return posixpath.relpath(name, start=cur_dir)


def head(lang, page):
    t = T[lang][page]
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{url(l, page)}">' for l in LANGS
    )
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{url("es", page)}">'
    og_alt = "\n".join(
        f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang
    )
    og_type = "profile" if page == "about" else "website"
    schema = ""
    if page == "home":
        h = T[lang]["home"]
        schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Adrián Martínez",
  "url": "{url(lang, 'home')}",
  "description": "{h['schema_desc']}",
  "inLanguage": "{lang}",
  "areaServed": ["ES", "IT", "EU"],
  "founder": {{
    "@type": "Person",
    "name": "Adrián Martínez",
    "jobTitle": "{h['job']}",
    "knowsLanguage": ["es", "en", "it"],
    "sameAs": "https://www.linkedin.com/in/adrianemartinez/"
  }}
}}
</script>"""
    return f"""<!DOCTYPE html>
<html lang="{T[lang]['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url(lang, page)}">
{alts}

<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{url(lang, page)}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{og_alt}
<meta name="twitter:card" content="summary">
{schema}
<link rel="stylesheet" href="{asset('style.css')}">
<script data-goatcounter="{GOATCOUNTER}" async src="//gc.zgo.at/count.js"></script>
</head>"""


def header(lang, page):
    nav = T[lang]["nav"]
    links = "\n      ".join(
        f'<a href="{href(lang, p)}"{" aria-current=\"page\"" if p == page else ""}>{nav[p]}</a>'
        for p in ["services", "about", "contact"]
    )
    switch = " ".join(
        (f'<a href="{href(l, page)}" hreflang="{l}" lang="{l}" title="{LANG_NAME[l]}" aria-current="true">{FLAGS[l]}{LANG_LABEL[l]}</a>'
         if l == lang else
         f'<a href="{href(l, page)}" hreflang="{l}" lang="{l}" title="{LANG_NAME[l]}">{FLAGS[l]}{LANG_LABEL[l]}</a>')
        for l in LANGS
    )
    return f"""<body>

<header>
  <div class="nav-wrap">
    <a href="{href(lang, 'home')}" class="logo">aemartinez</a>
    <div class="nav-right">
      <nav aria-label="{T[lang]['nav_label']}">
      {links}
      </nav>
      <div class="lang" role="group" aria-label="{T[lang]['lang_label']}">{switch}</div>
    </div>
  </div>
</header>
"""


def footer(lang):
    return f"""
<footer>
  &copy; 2026 Adrián Martínez — {T[lang]['footer']}
</footer>

</body>
</html>
"""


def body_home(lang):
    h = T[lang]["home"]
    chips = "\n    ".join(f'<span class="chip">{c}</span>' for c in CHIPS)
    return f"""
<section class="hero">
  <h1>{h['h1']}</h1>
  <p class="lead">{h['lead']}</p>
  <div class="chips">
    {chips}
  </div>
  <a href="{href(lang, 'contact')}" class="btn">{h['cta']}</a>
</section>

<section class="tight">
  <h2 class="section-title">{h['intro_title']}</h2>
  <p class="section-sub">
    {h['intro']}
  </p>
  <a href="{href(lang, 'services')}" class="btn-outline">{h['intro_btn']}</a>
</section>
"""


def body_services(lang):
    s = T[lang]["services"]
    blocks = []
    for i, (fw, h3, p, ideal) in enumerate(s["items"], 1):
        blocks.append(f"""
  <div class="service">
    <div>
      <span class="num">{i:02d}</span>
    </div>
    <div>
      <span class="frameworks">{fw}</span>
      <h3>{h3}</h3>
      <p>{p}</p>
      <p class="ideal"><strong>{s['ideal']}</strong> {ideal}</p>
    </div>
  </div>""")
    return f"""
<section>
  <h2 class="section-title">{s['h2']}</h2>
  <p class="section-sub">{s['sub']}</p>
{''.join(blocks)}

  <div style="margin-top:48px;">
    <a href="{href(lang, 'contact')}" class="btn">{s['cta']}</a>
  </div>
</section>
"""


def body_about(lang):
    a = T[lang]["about"]
    tl = "\n".join(
        f'  <div class="timeline-item">\n    <h3>{h}</h3>\n    <p>{p}</p>\n  </div>\n'
        for h, p in a["timeline"]
    )
    certs = "\n".join(
        f'    <div class="cert-card"><span class="label">{l}</span><p>{p}</p></div>'
        for l, p in a["certs"]
    )
    return f"""
<section>
  <h2 class="section-title">{a['h2']}</h2>
  <p class="section-sub">
    {a['intro']}
  </p>

{tl}</section>

<section class="tight">
  <h2 class="section-title">{a['certs_title']}</h2>
  <div class="certs">
{certs}
  </div>
</section>
"""


def body_contact(lang):
    c = T[lang]["contact"]
    return f"""
<section>
  <h2 class="section-title">{c['h2']}</h2>
  <p class="section-sub">{c['sub']}</p>

  <form action="{FORMSPREE}" method="POST">
    <input type="hidden" name="_language" value="{lang}">
    <div>
      <label for="nombre">{c['name']}</label>
      <input type="text" id="nombre" name="nombre" required>
    </div>
    <div>
      <label for="empresa">{c['company']}</label>
      <input type="text" id="empresa" name="empresa">
    </div>
    <div>
      <label for="email">{c['email']}</label>
      <input type="email" id="email" name="email" required>
    </div>
    <div>
      <label for="mensaje">{c['message']}</label>
      <textarea id="mensaje" name="mensaje" rows="5" required></textarea>
    </div>
    <button type="submit" class="btn" style="border:none; cursor:pointer;">{c['send']}</button>
  </form>

  <div class="contact-info">
    <div>
      <span class="label">{c['email']}</span>
      {EMAIL}
    </div>
    <div>
      <span class="label">{c['linkedin']}</span>
      {LINKEDIN}
    </div>
  </div>
</section>
"""


BODIES = {"home": body_home, "services": body_services, "about": body_about, "contact": body_contact}

LANG_CSS = """
/* Selector de idioma */
.nav-right { display: flex; align-items: center; gap: 28px; }
.nav-right nav a { margin-left: 0; margin-right: 28px; }
.nav-right nav a:last-child { margin-right: 0; }
nav a[aria-current="page"] { color: var(--gold); }
.lang { display: flex; gap: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.lang a {
  display: inline-flex; align-items: center; gap: 6px;
  text-decoration: none; color: var(--gray); padding: 4px 8px;
  border: 1px solid transparent; border-radius: var(--radius);
}
.lang .flag {
  width: 18px; height: 12px; flex: none; border-radius: 2px;
  box-shadow: 0 0 0 1px rgba(11, 37, 69, 0.18);
}
.lang a:hover { color: var(--gold); }
.lang a[aria-current="true"] { color: var(--navy); border-color: var(--gold); background: var(--gold-bg); }
@media (max-width: 640px) {
  .nav-wrap { flex-wrap: wrap; gap: 12px; }
  .nav-right { gap: 14px; flex-wrap: wrap; }
  .nav-right nav a { margin-right: 16px; }
}
"""


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    prio = {"home": "1.0", "services": "0.9", "contact": "0.8", "about": "0.7"}
    for page in PAGES:
        for lang in LANGS:
            out.append("  <url>")
            out.append(f"    <loc>{url(lang, page)}</loc>")
            for l in LANGS:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l, page)}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("es", page)}"/>')
            out.append(f"    <priority>{prio[page]}</priority>")
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        for page in PAGES:
            rel = PATHS[lang][page] or "index.html"
            if rel.endswith("/"):
                rel += "index.html"
            f = out / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            _CUR["lang"], _CUR["page"] = lang, page
            f.write_text(head(lang, page) + "\n" + header(lang, page) + BODIES[page](lang) + footer(lang), encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    css = out / "style.css"
    if css.exists():
        txt = css.read_text(encoding="utf-8")
        if "Selector de idioma" not in txt:
            css.write_text(txt.rstrip() + "\n" + LANG_CSS, encoding="utf-8")
    else:
        print("AVISO: no hay style.css en la carpeta de salida; copialo antes de ejecutar.")
    print("OK:", sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "site")
