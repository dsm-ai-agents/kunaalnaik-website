"""Nav, header, footer, and page chrome for the KunaalNaik.com generator."""
import json as _json

NAV = [
    ("Training", None, [
        ("Corporate AI training", "/corporate-ai-training/", "The core role-based programme"),
        ("Executive & leadership", "/ai-training-for-executive-teams/", "Portfolio, governance, investment"),
        ("Finance", "/ai-training-for-finance-teams/", "Variance commentary, audit-safe"),
        ("HR & L&D", "/ai-training-for-hr-and-l-and-d/", "Job specs, competencies, onboarding"),
        ("Legal", "/ai-training-for-legal-teams/", "Clause comparison, privilege"),
        ("Operations", "/ai-training-for-operations/", "SOPs, incidents, exceptions"),
        ("Sales", "/ai-training-for-sales-teams/", "Research, preparation, follow-up"),
        ("Marketing", "/ai-training-for-marketing-teams/", "Planning, brand voice, QC"),
        ("Engineering", "/ai-training-for-engineering-teams/", "Beyond coding assistants"),
        ("Global delivery", "/global-ai-training-delivery/", "Timezones, onsite, contracting"),
    ]),
    ("Consulting", None, [
        ("AI workflow consulting", "/ai-automation-consulting/", "Audit, pilot, implement, hand over"),
        ("Agent governance", "/ai-agent-governance-and-guardrails/", "Permissions, approvals, audit trails"),
        ("When not to use an agent", "/when-not-to-use-an-ai-agent/", "Honest selection, shorter list"),
        ("Agentic vs generative AI", "/agentic-ai-vs-generative-ai-for-business/", "What changes when AI acts"),
    ]),
    ("Claude & Hermes", None, [
        ("Claude Cowork training", "/claude-cowork-training/", "Team enablement and governance"),
        ("Cowork for finance", "/claude-cowork-for-finance/", "Reporting, traceable to source"),
        ("Cowork for legal", "/claude-cowork-for-legal/", "Long documents, citations"),
        ("Cowork for marketing", "/claude-cowork-for-marketing/", "Campaigns, on brand"),
        ("Cowork for operations", "/claude-cowork-for-operations/", "SOPs, exceptions included"),
        ("Hermes Agent training", "/hermes-agent-training/", "Memory, skills, tools, schedules"),
        ("Hermes for consultants", "/hermes-agent-for-consultants/", "Per-client context, separated"),
        ("Hermes for executives", "/hermes-agent-for-executives/", "Briefings on a schedule"),
        ("Hermes for founders", "/hermes-agent-for-founders/", "The first workflows worth it"),
    ]),
    ("Before you buy", None, [
        ("AI readiness scorecard", "/ai-readiness-scorecard/", "Free, 3 minutes, no email for the score"),
        ("What it costs", "/corporate-ai-training-cost-india/", "The six drivers of the fee"),
        ("Choosing a trainer", "/how-to-choose-a-corporate-ai-trainer/", "Criteria, and red flags"),
        ("RFP template", "/corporate-ai-training-rfp-template/", "Free, ungated, provider-neutral"),
        ("Measuring ROI", "/ai-training-roi-measurement/", "Baselines before delivery"),
        ("Case studies", "/case-studies/", "Inspectable proof"),
    ]),
    ("About", "/about-kunaal-naik/"),
]


EMAIL = None
SITE = None
PERSON = None
ORGANIZATION = None
VISITOR_TAG = None
SOCIALS = None
_esc = None
_mailto = None


def bind_chrome(*, esc, mailto, EMAIL_VAL, SITE_VAL, PERSON_VAL, ORGANIZATION_VAL,
                VISITOR_TAG_VAL, SOCIALS_VAL):
    global _esc, _mailto, EMAIL, SITE, PERSON, ORGANIZATION, VISITOR_TAG, SOCIALS
    _esc, _mailto = esc, mailto
    EMAIL, SITE = EMAIL_VAL, SITE_VAL
    PERSON, ORGANIZATION = PERSON_VAL, ORGANIZATION_VAL
    VISITOR_TAG, SOCIALS = VISITOR_TAG_VAL, SOCIALS_VAL


def esc(value):
    return _esc(value)


def mailto(subject):
    return _mailto(subject)

def header():
    # <details> gives open/close, keyboard support, and Esc for free — no JS.
    parts = []
    for entry in NAV:
        if entry[1] is not None:
            parts.append(f'<a href="{entry[1]}">{esc(entry[0])}</a>')
            continue
        label, _, children = entry
        items = "".join(
            f'<a href="{url}"><strong>{esc(text)}</strong><span>{esc(blurb)}</span></a>'
            for text, url, blurb in children)
        cols = " menu-wide" if len(children) > 5 else ""
        parts.append(
            f'<details class="menu"><summary>{esc(label)}</summary>'
            f'<div class="menu-panel{cols}">{items}</div></details>')
    links = "".join(parts)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><nav class="nav" aria-label="Primary navigation">
<a class="brand" href="/">Kunaal<span>.</span>Naik</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links">Menu</button>
<div class="nav-links" id="nav-links">{links}<a class="button button-primary" href="mailto:{EMAIL}">Email Kunaal</a></div>
</nav></header>'''


def footer():
    social = "".join(f'<a href="{url}" target="_blank" rel="me noopener">{name}</a>' for name, url in SOCIALS.items())
    return f'''<footer class="footer"><div class="footer-inner"><div class="footer-grid">
<div><h2>Turn AI ambition into operating capability.</h2><p>Training and implementation support for leaders, teams, professionals, founders, SMBs, and MSMEs.</p><div class="socials">{social}</div></div>
<div><h3>Work with Kunaal</h3><div class="footer-links"><a href="/corporate-ai-training/">Corporate AI training</a><a href="/ai-automation-consulting/">AI workflow consulting</a><a href="/ai-training-for-executive-teams/">Executive AI training</a><a href="/global-ai-training-delivery/">Global delivery</a><a href="/speaking-and-workshops/">Speaking & workshops</a><a href="/contact/">Contact</a></div></div>
<div><h3>By function</h3><div class="footer-links"><a href="/ai-training-for-finance-teams/">Finance</a><a href="/ai-training-for-hr-and-l-and-d/">HR & L&D</a><a href="/ai-training-for-legal-teams/">Legal</a><a href="/ai-training-for-operations/">Operations</a><a href="/ai-training-for-sales-teams/">Sales</a><a href="/ai-training-for-marketing-teams/">Marketing</a><a href="/ai-training-for-engineering-teams/">Engineering</a></div></div>
<div><h3>Agents</h3><div class="footer-links"><a href="/claude-cowork-training/">Claude Cowork</a><a href="/hermes-agent-training/">Hermes Agent</a><a href="/hermes-agent-for-consultants/">For consultants</a><a href="/hermes-agent-for-executives/">For executives</a><a href="/hermes-agent-for-founders/">For founders</a><a href="/ai-agent-governance-and-guardrails/">Agent governance</a><a href="/when-not-to-use-an-ai-agent/">When not to use one</a></div></div>
<div><h3>Before you buy</h3><div class="footer-links"><a href="/corporate-ai-training-cost-india/">Training cost</a><a href="/how-to-choose-a-corporate-ai-trainer/">Choosing a trainer</a><a href="/corporate-ai-training-rfp-template/">RFP template</a><a href="/ai-training-roi-measurement/">Measuring ROI</a><a href="/about-kunaal-naik/">About</a><a href="/case-studies/">Case studies</a><a href="/insights/">Insights</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div>
</div><div class="footer-bottom"><span>© 2026 Kunaal Naik</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div></footer>'''

def schemas(kind, title, description, path, faqs=None):
    url = SITE + path
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": description, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": PERSON["@id"]}}
    items = [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Kunaal Naik"}, ORGANIZATION, PERSON, webpage]
    if kind == "ProfilePage":
        webpage["@type"] = "ProfilePage"; webpage["mainEntity"] = {"@id": PERSON["@id"]}
    elif kind == "Service":
        items.append({"@type": "Service", "name": title.split(" | ")[0], "description": description, "url": url, "provider": {"@id": PERSON["@id"]}, "areaServed": ["India", "Worldwide"]})
    if faqs:
        items.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    return {"@context": "https://schema.org", "@graph": items}
def faq_section(faqs):
    """Visible FAQ markup. Must stay in sync with FAQPage schema — same q/a source."""
    rows = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for q, a in faqs)
    return f'''<section class="section"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Common questions</p><h2>Before you enquire.</h2></div></div><div class="faq-list">{rows}</div></div></section>'''


def page(title, description, path, body, kind="WebPage", faqs=None):
    canonical = SITE + path
    data = _json.dumps(schemas(kind, title, description, path, faqs), ensure_ascii=False, separators=(",", ":"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kunaal Naik"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/og-kunaal-naik.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SITE}/assets/og-kunaal-naik.jpg">
<link rel="stylesheet" href="/assets/site.css"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{data}</script>{VISITOR_TAG}</head><body>{header()}<main id="main">{body}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>'''


def page_hero(kicker, title, lede, current):
    return f'''<section class="page-hero"><div class="page-hero-inner"><div class="breadcrumbs"><a href="/">Home</a> / {esc(current)}</div><p class="eyebrow">{esc(kicker)}</p><h1>{title}</h1><p class="lede">{lede}</p></div></section>'''


def cta(title, text, subject):
    return f'''<section class="section cta-band"><div class="section-inner"><div><p class="eyebrow">Start a useful conversation</p><h2>{title}</h2><p>{text}</p></div><div class="cta-actions"><a class="button button-light" href="{mailto(subject)}">Email {EMAIL}</a></div></div></section>'''


def scorecard_cta(text=None):
    """Standout prompt for the free scorecard. Placed where intent is highest:
    the homepage, every service page sidebar, and the contact page."""
    line = text or ("Not sure where you stand? Answer ten questions and see your "
                    "score, four sub-scores, and your three highest-value gaps.")
    return f'''<section class="section section-tight"><div class="section-inner"><div class="sc-promo"><div><span class="tag">Free tool &middot; 3 minutes</span><h2>AI readiness scorecard</h2><p>{line}</p><p class="sc-promo-note">No email needed for the score.</p></div><a class="button button-primary" href="/ai-readiness-scorecard/">Start the scorecard</a></div></div></section>'''


def sidebar(label, text, subject):
    return f'''<aside class="sidebar"><div class="panel panel-accent"><span class="tag">{label}</span><h3>Start with the outcome.</h3><p>{text}</p><a class="button" href="{mailto(subject)}">Email Kunaal</a></div>
<div class="panel sc-side"><span class="tag">Free &middot; 3 min</span><h3>Where do you stand?</h3><p>Ten questions, an instant score, and your three highest-value gaps. No email needed for the score.</p><a class="button" href="/ai-readiness-scorecard/">Run the scorecard</a></div></aside>'''

def related_section(related):
    """Hub-and-spoke internal links. Prevents these pages being orphans."""
    links = "".join(f'<a href="{url}">{esc(label)}</a>' for label, url in related)
    return f'''<section class="section section-tight section-white"><div class="section-inner"><p class="eyebrow">Related</p><div class="footer-links">{links}</div></div></section>'''


def service_body(item):
    outcomes = "".join(f"<li>{esc(x)}</li>" for x in item["outcomes"])
    formats = "".join(f"<li>{esc(x)}</li>" for x in item["formats"])
    extra = related_section(item["related"]) if item.get("related") else ""
    faqs = faq_section(item["faqs"]) if item.get("faqs") else ""
    return f'''{page_hero(item['kicker'], item['h1'], item['lede'], item['kicker'])}<section class="section"><div class="section-inner content-grid"><article class="prose"><h2>The problem this solves</h2><p>{item['problem']}</p><h2>What the engagement should produce</h2><ul>{outcomes}</ul><h2>Ways to work together</h2><ul>{formats}</ul><h2>Who it is for</h2><p>{item['fit']}</p><blockquote>No black-box transformation. The goal is internal capability, explicit ownership, and evidence that the workflow improved the work.</blockquote><h2>How scope is decided</h2><p>Send the audience, workflow or business priority, current tools, constraints, and desired outcome. The first response will identify the smallest useful starting point and any missing information—not force a standard package.</p></article>{sidebar('Email-first scoping', 'Describe the team, priority, and desired outcome. No booking funnel or generic sales deck.', item['subject'])}</div></section>{faqs}{extra}{cta('Bring one real workflow.', 'The best first conversation starts with work that is repetitive, consequential, measurable, or difficult to scale.', item['subject'])}'''
