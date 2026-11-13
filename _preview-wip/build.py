#!/usr/bin/env python3
"""Generates the static CS/EN pages of the Mazlusek website into the given output directory."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])
BASE = "https://mazlusek.com"
EMAIL = "info@mazlusek.com"
PHONE_TEL, PHONE = "+420702118089", "+420 702 118 089"

ICONS = {
 "arch": '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 5 9-5"/>',
 "code": '<path d="m8 8-5 4 5 4"/><path d="m16 8 5 4-5 4"/><path d="m14 5-4 14"/>',
 "mobile": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
 "ai": '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l2.8 2.8M16.2 16.2 19 19M19 5l-2.8 2.8M7.8 16.2 5 19"/>',
 "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.6-8.96A6 6 0 0 1 18 10a4 4 0 0 1 0 8H7Z"/>',
 "refresh": '<path d="M20 11a8 8 0 0 0-14-4.5L4 9"/><path d="M4 4v5h5"/><path d="M4 13a8 8 0 0 0 14 4.5L20 15"/><path d="M20 20v-5h-5"/>',
 "review": '<path d="M9 11l2 2 4-4"/><rect x="3.5" y="3.5" width="17" height="17" rx="3"/>',
 "team": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17.5" cy="9" r="2.4"/><path d="M17 14.6c2.4.2 4 1.9 4 4.4"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>',
 "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
}

def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'

SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' + "".join(
    f'<symbol id="i-{k}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
    for k, v in ICONS.items()) + "</svg>"

KOTLIN = """<span class="a">@RestController</span>
<span class="k">class</span> <span class="t">OrderHandler</span>(<span class="k">private val</span> service: <span class="t">OrderService</span>) {

    <span class="a">@GetMapping</span>(<span class="s">"/orders/{id}"</span>)
    <span class="k">suspend fun</span> <span class="f">get</span>(<span class="a">@PathVariable</span> id: <span class="t">String</span>): <span class="t">ResponseEntity</span>&lt;<span class="t">OrderDto</span>&gt; =
        service.<span class="f">find</span>(id)
            ?.<span class="f">let</span> { <span class="t">ResponseEntity</span>.<span class="f">ok</span>(it.<span class="f">toDto</span>()) }
            ?: <span class="t">ResponseEntity</span>.<span class="f">notFound</span>().<span class="f">build</span>()

    <span class="a">@GetMapping</span>(<span class="s">"/orders/stream"</span>, produces = [<span class="s">"application/x-ndjson"</span>])
    <span class="k">fun</span> <span class="f">stream</span>(): <span class="t">Flow</span>&lt;<span class="t">OrderDto</span>&gt; =
        service.<span class="f">updates</span>()
            .<span class="f">map</span> { it.<span class="f">toDto</span>() }
            .<span class="f">buffer</span>(<span class="n">64</span>)
}"""

YAML = """<span class="k">apiVersion</span>: apps/v1
<span class="k">kind</span>: <span class="t">Deployment</span>
<span class="k">metadata</span>:
  <span class="k">name</span>: <span class="s">orders-api</span>
<span class="k">spec</span>:
  <span class="k">replicas</span>: <span class="n">3</span>
  <span class="k">selector</span>:
    <span class="k">matchLabels</span>: { app: <span class="s">orders-api</span> }
  <span class="k">template</span>:
    <span class="k">metadata</span>:
      <span class="k">labels</span>: { app: <span class="s">orders-api</span> }
    <span class="k">spec</span>:
      <span class="k">containers</span>:
        - <span class="k">name</span>: <span class="s">app</span>
          <span class="k">image</span>: <span class="s">registry.example/orders-api:1.0.0</span>
          <span class="k">readinessProbe</span>:
            <span class="k">httpGet</span>: { path: <span class="s">/actuator/health</span>, port: <span class="n">8080</span> }
          <span class="k">resources</span>:
            <span class="k">limits</span>: { cpu: <span class="s">"1"</span>, memory: <span class="s">512Mi</span> }"""

L = {
 "cs": dict(
  lang="cs", root="/", other="/en/", other_label="English", other_lang="en", pol="/privacy/",
  title="Mazlušek s.r.o. – IT outsourcing a softwarová architektura",
  desc="Mazlušek s.r.o. – IT outsourcing a softwarová architektura. Backend v Javě a Kotlinu, mikroslužby, Kubernetes, AI integrace. Spolupráce na dálku, B2B.",
  nav=[("services","Služby"),("experience","Reference"),("code","Ukázky kódu"),("career","Kariéra"),("tech","Technologie"),("contact","Kontakt")],
  nav_privacy="Ochrana soukromí", menu="Menu", skip="Přeskočit na obsah",
  eyebrow="IT outsourcing &amp; softwarová architektura",
  h1='Architektura a backend, <span class="grad">které obstojí v provozu</span>',
  lead="Mazlušek s.r.o. dodává seniorní softwarovou architekturu a hands-on vývoj pro banky, státní správu i technologické firmy. Java a Kotlin backend, mikroslužby, Kubernetes a AI integrace – na dálku a na bázi B2B kontraktu.",
  cta1="Napsat nám", cta2="Zobrazit reference",
  badges=["25+ let zkušeností","100 % remote","B2B kontrakt"],
  hero_card_h="Jan Damek", hero_card_r="CEO &amp; Senior Software Architect",
  hero_card_p="Java &amp; Kotlin backend, návrh systémů, vedení týmů. Krátkodobé i střednědobé spolupráce.",
  s_services="Služby", s_services_p="Od návrhu architektury po provoz v Kubernetes – jedním partnerem.",
  services=[("arch","Architektura a návrh systémů","Mikroslužby, vysoce propustné systémy, dlouhodobé plány architektury a vývoje."),
   ("code","Backend na zakázku","Kotlin/Spring Boot včetně WebFlux, Java a Python. Čisté API, testovatelný kód."),
   ("mobile","Mobilní a cross-platform vývoj","iOS, Android a Kotlin Multiplatform – sdílená logika, nativní dojem."),
   ("ai","Integrace AI a LLM","RAG, embeddingy a napojení jazykových modelů do existujících systémů."),
   ("cloud","DevOps a Kubernetes","Kubernetes, CI/CD, kontejnerizace, nasazení v cloudu i on-premises."),
   ("refresh","Modernizace a migrace","Převod legacy systémů na moderní platformy bez zbytečného rizika."),
   ("review","Code review a konzultace","Nezávislý pohled na architekturu a kvalitu kódu, mentoring vývojářů."),
   ("team","Vedení týmu","Scrum, plánování, technické vedení a předávání znalostí.")],
  s_exp="Reference", s_exp_p="Anonymizované zkušenosti z reálných projektů. Zákazníky z diskrétnosti nejmenujeme.",
  lbl_role="Role", lbl_sit="Zadání", lbl_stack="Technologie",
  refs=[
   dict(period="2023–2026", title="Softwarový architekt – významná česká banka",
        sit="Architektura a backend bankovních systémů (úvěrové a kampaňové systémy, iniciativa podnikové architektury). Dlouhodobé plány architektury a vývoje, posuzování požadavků a dopadů s businessem a analytiky, technické řízení dodávky, kvalita kódu a konzultace pro ostatní vývojáře.",
        tags=["Java","Kotlin","Spring Boot","WebFlux","Mikroslužby","REST","MongoDB","PostgreSQL","Kubernetes","Jenkins","Git"]),
   dict(period="od 2018", title="Senior Architect Developer – velké banky a státní instituce",
        sit="Migrace podnikových systémů z WebSphere / Java EE 6 na mikroslužby ve Spring Bootu (AWS i on-premises). Migrace uživatelských rozhraní ze Struts na Angular, React, React Native a Vaadin. Výkon PostgreSQL a integrita dat, CI/CD v Jenkinsu. Role Scrum Mastera, vedení týmu a mentoring.",
        tags=["Spring Boot","Java EE","PostgreSQL","Angular","React","React Native","Vaadin","Jenkins","AWS","Google Cloud","Scrum"]),
   dict(period="2023–2024", title="Solution Architect – AI startup",
        sit="Vedoucí architektury a backendu AI platformy, která automaticky překládá vzdělávací videa do více jazyků. Spolupráce s datovými vědci na nasazení neuronových sítí, s frontendem v Reactu, automatizované testy a CI.",
        tags=["Kotlin","Spring Boot","Apache Kafka","MongoDB","PostgreSQL","Redis","React","CI"]),
  ],
  s_code="Ukázky kódu", s_code_p="Obecné syntetické ukázky stylu, jakým pracujeme. Nejde o kód žádného zákazníka.",
  code_note="Syntetická ukázka",
  s_career="Kariérní vývoj", s_career_p="Od roku 1993 napříč telekomunikacemi, e-commerce, ERP, mobilem a bankovnictvím.",
  tl=[("2023–2026","Softwarový architekt","Významná česká banka"),
      ("2023–2024","Solution Architect","AI startup"),
      ("od 2018","Senior Architect Developer","Mazlušek s.r.o. – banky a státní instituce"),
      ("2014–2018","Senior vývojář","Velká IT společnost – Java EE / Spring Boot, JSF, Oracle / PostgreSQL, Spring Security"),
      ("2011–2014","Vývojář","Výrobce ERP softwaru – ERP systém a mobilní aplikace (iOS / Android)"),
      ("2010","Vývojář","Webové portály – PHP / MySQL"),
      ("2006–2010","Vývojář","Interní systémy společností v zahraničí (Španělsko)"),
      ("2003–2006","Vývojář","Pokladní systémy a e-commerce"),
      ("1998–2003","Vývojář","Telekomunikace a VoIP"),
      ("1993","Začátek kariéry","První profesionální zkušenosti v IT")],
  s_tech="Technologie", s_tech_p="Nástroje, se kterými denně pracujeme.",
  tech=["Java (SE/EE)","Kotlin","Spring / Spring Boot / WebFlux","Hibernate / JPA","PostgreSQL","MySQL","Oracle","MongoDB","Redis","Kafka","React","Angular","TypeScript","Docker","Kubernetes","AWS","Google Cloud","Jenkins","Git","Python / FastAPI","AI / LLM integrace"],
  s_edu="Vzdělání a jazyky", edu_h="Vzdělání", lang_h="Jazyky",
  edu=["Střední průmyslová škola Ostrava – elektrotechnika (1989–1993)","Vyšší odborná škola Kunovice – informatika (1993–1996)","Stanford Online – strojové učení (2014–2015, certifikace 2023)","Průběžné distanční studium na Stanford University (LLM, strojové učení)"],
  langs=[("Čeština","rodilý mluvčí"),("Angličtina",""),("Španělština","pokročilá"),("Polština","pokročilá"),("Slovenština",""),("Ruština","")],
  s_work="Jak spolupracujeme", s_work_p="Jednoduché podmínky, přímá komunikace.",
  work=[("Krátkodobé i střednědobé kontrakty","Spolupráce na dobu, která dává smysl vám i nám."),("Fakturace B2B (IČO)","Dodávka na základě smlouvy mezi firmami."),("Plně na dálku","Pracujeme na 100 % remote, s pravidelnou komunikací."),("Architektura i hands-on","Navrhneme řešení a sami ho s vámi postavíme.")],
  s_own="Vlastní produkty", own_p="Vedle zakázek vyvíjíme vlastní mobilní aplikace pro Android a iOS a cloudový backend k nim.",
  s_contact="Kontakt", contact_p="Máte projekt nebo dotaz? Napište nám, odpovíme co nejdříve.",
  idh="Identifikační údaje",
  ident=[("Obchodní firma","Mazlušek s.r.o."),("IČO","07656980"),("DIČ","CZ07656980"),("D-U-N-S","496244894"),("Spisová značka","C 76691, Krajský soud v Ostravě"),("Sídlo","Vršovců 2120/1a, 709 00 Ostrava, Česká republika")],
  lbl_email="E-mail", lbl_phone="Telefon",
  foot="© Mazlušek s.r.o. Všechna práva vyhrazena.", foot_reg="Zapsána v obchodním rejstříku vedeném Krajským soudem v Ostravě, sp. zn. C 76691.",
  og_loc="cs_CZ", jsonld_desc="IT outsourcing a softwarová architektura",
 ),
 "en": dict(
  lang="en", root="/en/", other="/", other_label="Česky", other_lang="cs", pol="/en/privacy/",
  title="Mazlušek s.r.o. – IT outsourcing and software architecture",
  desc="Mazlušek s.r.o. – IT outsourcing and software architecture. Java and Kotlin backend, microservices, Kubernetes, AI integration. Remote, B2B contracts.",
  nav=[("services","Services"),("experience","References"),("code","Code samples"),("career","Career"),("tech","Technology"),("contact","Contact")],
  nav_privacy="Privacy", menu="Menu", skip="Skip to content",
  eyebrow="IT outsourcing &amp; software architecture",
  h1='Architecture and backend <span class="grad">built to last in production</span>',
  lead="Mazlušek s.r.o. delivers senior software architecture and hands-on engineering for banks, public agencies and technology companies. Java and Kotlin backend, microservices, Kubernetes and AI integration – remote and on a B2B contract basis.",
  cta1="Get in touch", cta2="See references",
  badges=["25+ years of experience","100% remote","B2B contracts"],
  hero_card_h="Jan Damek", hero_card_r="CEO &amp; Senior Software Architect",
  hero_card_p="Java &amp; Kotlin backend, system design, team leadership. Short and mid-term engagements.",
  s_services="Services", s_services_p="From architecture design to running on Kubernetes – with a single partner.",
  services=[("arch","Architecture &amp; system design","Microservices, high-throughput systems, long-term architecture and development plans."),
   ("code","Custom backend","Kotlin/Spring Boot including WebFlux, Java and Python. Clean APIs, testable code."),
   ("mobile","Mobile &amp; cross-platform","iOS, Android and Kotlin Multiplatform – shared logic, native feel."),
   ("ai","AI &amp; LLM integration","RAG, embeddings and language models wired into existing systems."),
   ("cloud","DevOps &amp; Kubernetes","Kubernetes, CI/CD, containerisation, cloud and on-premises delivery."),
   ("refresh","Legacy modernisation","Moving legacy systems to modern platforms without unnecessary risk."),
   ("review","Code review &amp; consulting","An independent view on architecture and code quality, developer mentoring."),
   ("team","Team leadership","Scrum, planning, technical leadership and knowledge transfer.")],
  s_exp="References", s_exp_p="Anonymised experience from real projects. For discretion, we do not name customers.",
  lbl_role="Role", lbl_sit="Situation", lbl_stack="Technologies",
  refs=[
   dict(period="2023–2026", title="Software Architect – major Czech bank",
        sit="Architecture and backend for banking systems (lending and campaign systems, an enterprise architecture initiative). Long-term architecture and development plans, requirement and impact review with business and analysts, technical delivery, code quality and consulting for other developers.",
        tags=["Java","Kotlin","Spring Boot","WebFlux","Microservices","REST","MongoDB","PostgreSQL","Kubernetes","Jenkins","Git"]),
   dict(period="since 2018", title="Senior Architect Developer – large banks and government agencies",
        sit="Migration of enterprise systems from WebSphere / Java EE 6 to Spring Boot microservices (AWS and on-premises). UI migrations from Struts to Angular, React, React Native and Vaadin. PostgreSQL performance and data integrity, Jenkins CI/CD. Scrum Master, team leadership and mentoring.",
        tags=["Spring Boot","Java EE","PostgreSQL","Angular","React","React Native","Vaadin","Jenkins","AWS","Google Cloud","Scrum"]),
   dict(period="2023–2024", title="Solution Architect – AI startup",
        sit="Architecture and backend lead for an AI platform that automatically translates educational videos into multiple languages. Worked with data scientists on neural-network deployment and with the React frontend team; automated testing and CI.",
        tags=["Kotlin","Spring Boot","Apache Kafka","MongoDB","PostgreSQL","Redis","React","CI"]),
  ],
  s_code="Code samples", s_code_p="Generic, synthetic examples of the style we work in. Not code of any customer.",
  code_note="Synthetic sample",
  s_career="Career timeline", s_career_p="Since 1993 across telecommunications, e-commerce, ERP, mobile and banking.",
  tl=[("2023–2026","Software Architect","Major Czech bank"),
      ("2023–2024","Solution Architect","AI startup"),
      ("since 2018","Senior Architect Developer","Mazlušek s.r.o. – banks and government agencies"),
      ("2014–2018","Senior Developer","Large IT services company – Java EE / Spring Boot, JSF, Oracle / PostgreSQL, Spring Security"),
      ("2011–2014","Developer","ERP software vendor – ERP system and mobile apps (iOS / Android)"),
      ("2010","Developer","Web portals – PHP / MySQL"),
      ("2006–2010","Developer","In-house systems for companies abroad (Spain)"),
      ("2003–2006","Developer","POS systems and e-commerce"),
      ("1998–2003","Developer","Telecommunications and VoIP"),
      ("1993","Career start","First professional experience in IT")],
  s_tech="Technology", s_tech_p="The tools we work with every day.",
  tech=["Java (SE/EE)","Kotlin","Spring / Spring Boot / WebFlux","Hibernate / JPA","PostgreSQL","MySQL","Oracle","MongoDB","Redis","Kafka","React","Angular","TypeScript","Docker","Kubernetes","AWS","Google Cloud","Jenkins","Git","Python / FastAPI","AI / LLM integration"],
  s_edu="Education &amp; languages", edu_h="Education", lang_h="Languages",
  edu=["Technical high school SPS Ostrava – electrical engineering (1989–1993)","Higher vocational school Kunovice – IT (1993–1996)","Stanford Online – machine learning (2014–2015, certification 2023)","Ongoing distance study at Stanford University (LLM, machine learning)"],
  langs=[("Czech","native"),("English",""),("Spanish","advanced"),("Polish","advanced"),("Slovak",""),("Russian","")],
  s_work="How we work", s_work_p="Simple terms, direct communication.",
  work=[("Short and mid-term contracts","Engagements for as long as makes sense for both sides."),("B2B invoicing","Delivery under a contract between companies."),("Fully remote","We work 100% remotely with regular communication."),("Architecture and hands-on","We design the solution and build it with you.")],
  s_own="Own products", own_p="Alongside client work we develop our own mobile apps for Android and iOS and the cloud backend behind them.",
  s_contact="Contact", contact_p="Have a project or a question? Write to us and we will reply as soon as possible.",
  idh="Company details",
  ident=[("Legal name","Mazlušek s.r.o."),("Company ID (IČO)","07656980"),("VAT ID (DIČ)","CZ07656980"),("D-U-N-S","496244894"),("Registry file number","C 76691, Regional Court in Ostrava"),("Registered office","Vršovců 2120/1a, 709 00 Ostrava, Czech Republic")],
  lbl_email="E-mail", lbl_phone="Phone",
  foot="© Mazlušek s.r.o. All rights reserved.", foot_reg="Registered in the Commercial Register kept by the Regional Court in Ostrava, file number C 76691.",
  og_loc="en_US", jsonld_desc="IT outsourcing and software architecture",
 ),
}

def head(c, title, desc, path_cs, path_en, robots="index,follow", og=True, jsonld=""):
    own = path_cs if c["lang"] == "cs" else path_en
    other_lang = c["other_lang"]
    og_tags = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="Mazlušek s.r.o.">'
               f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
               f'<meta property="og:url" content="{BASE}{own}"><meta property="og:locale" content="{c["og_loc"]}">'
               f'<meta name="twitter:card" content="summary">') if og else ""
    return (f'<!DOCTYPE html>\n<html lang="{c["lang"]}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><meta name="description" content="{desc}">'
            f'<meta name="robots" content="{robots}"><meta name="theme-color" content="#0B1020">'
            f'<link rel="canonical" href="{BASE}{own}">'
            f'<link rel="alternate" hreflang="cs" href="{BASE}{path_cs}"><link rel="alternate" hreflang="en" href="{BASE}{path_en}">'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{path_cs}">'
            f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">{og_tags}'
            f'<link rel="stylesheet" href="/style.css"><script src="/app.js"></script>{jsonld}</head><body>')

def header(c):
    r = c["root"]
    links = "".join(f'<a href="{r}#{k}">{v}</a>' for k, v in c["nav"])
    return (f'{SPRITE}<a class="skip" href="#main">{c["skip"]}</a><header class="site-header"><div class="wrap bar">'
            f'<a class="logo" href="{r}"><svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><use href="#logo"/></svg>Mazlušek <span>s.r.o.</span></a>'
            f'<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">{c["menu"]}</button>'
            f'<nav id="site-nav" class="site-nav" aria-label="Main">{links}<a href="{c["pol"]}">{c["nav_privacy"]}</a>'
            f'<a class="lang" href="{c["other"]}" hreflang="{c["other_lang"]}" lang="{c["other_lang"]}">{c["other_label"]}</a></nav></div></header>')

LOGO_SYMBOL = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="logo" viewBox="0 0 32 32">'
  '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#8B5CF6"/></linearGradient></defs>'
  '<rect width="32" height="32" rx="8" fill="url(#lg)"/><path d="M7 23V9l9 9 9-9v14" fill="none" stroke="#0B1020" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></symbol></svg>')

def footer(c):
    return (f'<footer class="site-footer"><div class="wrap"><p>{c["foot"]}</p><p class="muted">{c["foot_reg"]}</p>'
            f'<p><a href="{c["pol"]}">{c["nav_privacy"]}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></footer></body></html>\n')

def pills(tags, cls="pill"):
    return "".join(f'<li class="{cls} c{i % 6}">{t}</li>' for i, t in enumerate(tags))

def section(sid, cls, title, sub, body):
    return (f'<section id="{sid}" class="sec {cls}"><div class="wrap"><div class="sec-head"><h2>{title}</h2>'
            f'<p class="sub">{sub}</p></div>{body}</div></section>')

def home(c):
    cs, en = "/", "/en/"
    jsonld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization",'
              f'"name":"Mazlušek s.r.o.","legalName":"Mazlušek s.r.o.","url":"{BASE}{c["root"]}","description":"{c["jsonld_desc"]}",'
              f'"email":"{EMAIL}","telephone":"{PHONE_TEL}","vatID":"CZ07656980","taxID":"07656980",'
              '"address":{"@type":"PostalAddress","streetAddress":"Vršovců 2120/1a","postalCode":"709 00","addressLocality":"Ostrava","addressCountry":"CZ"},'
              '"founder":{"@type":"Person","name":"Jan Damek","jobTitle":"CEO, Senior Software Architect"}}</script>')
    h = head(c, c["title"], c["desc"], cs, en, jsonld=jsonld) + LOGO_SYMBOL + header(c) + '<main id="main">'
    badges = "".join(f'<li>{b}</li>' for b in c["badges"])
    h += (f'<section class="hero"><div class="hero-grid" aria-hidden="true"></div><div class="wrap hero-in"><div class="hero-copy">'
          f'<p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1><p class="lead">{c["lead"]}</p>'
          f'<div class="actions"><a class="btn btn-primary" href="mailto:{EMAIL}">{c["cta1"]}</a><a class="btn btn-ghost" href="#experience">{c["cta2"]}</a></div>'
          f'<ul class="badges">{badges}</ul></div>'
          f'<aside class="hero-card glass"><div class="avatar" aria-hidden="true">JD</div><h2>{c["hero_card_h"]}</h2>'
          f'<p class="role">{c["hero_card_r"]}</p><p>{c["hero_card_p"]}</p>'
          f'<ul class="pills">{pills(["Java","Kotlin","Spring Boot","Kubernetes"])}</ul></aside></div></section>')
    cards = "".join(f'<article class="card">{icon(i)}<h3>{t}</h3><p>{d}</p></article>' for i, t, d in c["services"])
    h += section("services", "light", c["s_services"], c["s_services_p"], f'<div class="grid cards">{cards}</div>')
    refs = ""
    for r in c["refs"]:
        refs += (f'<article class="ref glass"><p class="period">{r["period"]}</p><h3>{r["title"]}</h3>'
                 f'<p>{r["sit"]}</p><p class="lbl">{c["lbl_stack"]}</p><ul class="pills">{pills(r["tags"])}</ul></article>')
    h += section("experience", "dark", c["s_exp"], c["s_exp_p"], f'<div class="grid refs">{refs}</div>')
    def win(name, lang, code):
        return (f'<figure class="editor"><figcaption><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
                f'<span class="fname">{name}</span><span class="note">{c["code_note"]}</span></figcaption>'
                f'<pre><code>{code}</code></pre></figure>')
    h += section("code", "light", c["s_code"], c["s_code_p"],
                 f'<div class="grid code">{win("OrderHandler.kt","kotlin",KOTLIN)}{win("deployment.yaml","yaml",YAML)}</div>')
    tl = "".join(f'<li><span class="when">{w}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for w, t, d in c["tl"])
    h += section("career", "dark", c["s_career"], c["s_career_p"], f'<ol class="timeline">{tl}</ol>')
    h += section("tech", "light", c["s_tech"], c["s_tech_p"], f'<ul class="pills big">{pills(c["tech"])}</ul>')
    edu = "".join(f'<li>{e}</li>' for e in c["edu"])
    langs = "".join(f'<li><strong>{n}</strong>{(" – " + d) if d else ""}</li>' for n, d in c["langs"])
    h += section("education", "dark", c["s_edu"], "",
                 f'<div class="grid two"><div class="glass pad"><h3>{c["edu_h"]}</h3><ul class="plain">{edu}</ul></div>'
                 f'<div class="glass pad"><h3>{c["lang_h"]}</h3><ul class="plain">{langs}</ul></div></div>')
    work = "".join(f'<article class="card"><h3>{t}</h3><p>{d}</p></article>' for t, d in c["work"])
    h += section("work", "light", c["s_work"], c["s_work_p"], f'<div class="grid four">{work}</div>')
    h += section("products", "dark", c["s_own"], "", f'<p class="own glass pad">{c["own_p"]}</p>')
    ident = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in c["ident"])
    contact = (f'<div class="grid two"><div class="card"><h3>{c["s_contact"]}</h3><ul class="contact">'
               f'<li>{icon("mail")}<span><span class="muted">{c["lbl_email"]}</span><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>'
               f'<li>{icon("phone")}<span><span class="muted">{c["lbl_phone"]}</span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>'
               f'<li>{icon("pin")}<span><span class="muted">{c["ident"][5][0]}</span>{c["ident"][5][1]}</span></li></ul>'
               f'<a class="btn btn-primary" href="mailto:{EMAIL}">{c["cta1"]}</a></div>'
               f'<div class="card"><h3>{c["idh"]}</h3><dl>{ident}</dl></div></div>')
    h += section("contact", "light", c["s_contact"], c["contact_p"], contact)
    return h + "</main>" + footer(c)

PRIV = {
 "cs": [("Správce","Správcem je Mazlušek s.r.o., IČO 07656980, Vršovců 2120/1a, 709 00 Ostrava, e-mail info@mazlusek.com."),
  ("Co web zpracovává","Tento web je statický. Nepoužívá cookies, analytické ani reklamní nástroje, nemá přihlášení ani formuláře a nesbírá žádné osobní údaje."),
  ("Provozní logy","Při zobrazení stránky může poskytovatel hostingu (Netlify, Inc.) technicky zpracovat IP adresu a údaje o požadavku v serverových logech za účelem provozu a zabezpečení služby. Mazlušek s.r.o. k těmto logům nemá přístup."),
  ("Komunikace e-mailem","Pokud nám napíšete, zpracujeme vaši e-mailovou adresu a obsah zprávy výhradně za účelem vyřízení dotazu a uchováme je po nezbytnou dobu."),
  ("Vaše práva","Máte právo na přístup, opravu, výmaz a omezení zpracování svých údajů a právo podat stížnost u Úřadu pro ochranu osobních údajů (uoou.gov.cz). Uplatnit je můžete na info@mazlusek.com."),
  ("Zásady aplikací","Zásady ochrany soukromí jednotlivých aplikací jsou uvedeny u příslušné aplikace v obchodech Google Play a App Store."),
  ("Účinnost","Platné od 12. 11. 2026.")],
 "en": [("Controller","The controller is Mazlušek s.r.o., company ID 07656980, Vršovců 2120/1a, 709 00 Ostrava, Czech Republic, e-mail info@mazlusek.com."),
  ("What this website processes","This website is static. It uses no cookies, no analytics or advertising tools, has no login or forms and collects no personal data."),
  ("Server logs","When a page is requested, the hosting provider (Netlify, Inc.) may technically process the IP address and request data in server logs to operate and secure the service. Mazlušek s.r.o. has no access to these logs."),
  ("E-mail communication","If you write to us, we process your e-mail address and the content of your message solely to handle your enquiry and keep them for as long as necessary."),
  ("Your rights","You have the right of access, rectification, erasure and restriction of processing, and the right to lodge a complaint with the Czech Office for Personal Data Protection (uoou.gov.cz). Contact us at info@mazlusek.com."),
  ("App policies","The privacy policy of each app is linked on its Google Play and App Store listing."),
  ("Effective","Effective from 12 November 2026.")],
}

def privacy(c):
    t = {"cs": "Zásady ochrany soukromí webu", "en": "Website privacy policy"}[c["lang"]]
    h = head(c, f"{t} – Mazlušek s.r.o.", t, "/privacy/", "/en/privacy/", og=False) + LOGO_SYMBOL + header(c)
    h += f'<main id="main"><section class="page-hero"><div class="wrap"><h1>{t}</h1></div></section><section class="sec light"><div class="wrap prose">'
    h += "".join(f'<h2>{a}</h2><p>{b}</p>' for a, b in PRIV[c["lang"]])
    return h + "</div></section></main>" + footer(c)

def not_found(c):
    h = head(c, "404 – Mazlušek s.r.o.", "404", "/", "/en/", robots="noindex", og=False) + LOGO_SYMBOL + header(c)
    return h + (f'<main id="main"><section class="page-hero"><div class="wrap"><h1>404</h1></div></section><section class="sec light"><div class="wrap prose">'
                f'<p><a href="/">Mazlušek s.r.o.</a> · <a href="/en/">English</a></p></div></section></main>') + footer(c)

def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

write("index.html", home(L["cs"]))
write("en/index.html", home(L["en"]))
write("privacy/index.html", privacy(L["cs"]))
write("en/privacy/index.html", privacy(L["en"]))
write("404.html", not_found(L["cs"]))
