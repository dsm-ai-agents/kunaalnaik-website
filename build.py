#!/usr/bin/env python3
"""Build the dependency-free static KunaalNaik.com site."""
from pathlib import Path
import html
import json

from pages_structural import STRUCTURAL

ROOT = Path(__file__).parent
SITE = "https://kunaalnaik.com"
EMAIL = "me@kunaalnaik.com"

# Leadsy / vtag visitor-identification pixel. Third-party script: it resolves
# anonymous visitors to company/contact data, so the privacy page must say so.
VISITOR_TAG_SRC = "https://r2.leadsy.ai/tag.js"
VISITOR_TAG_PID = "pbfdcrcFAjyErfW8"
VISITOR_TAG_VERSION = "062024"

# Consent gate. EU/UK/EEA/Swiss visitors get the script deferred until they
# accept; everyone else loads it immediately with no banner.
#
# ponytail: region detected from the browser's IANA timezone, not IP geo. A
# European on a US VPN is misclassified (shown no banner) and a traveller in
# Europe sees one unnecessarily. That is the accepted ceiling for a static site
# with zero backend. Upgrade path if EU volume grows: read Vercel's
# x-vercel-ip-country header in middleware and render the decision server-side.
VISITOR_TAG = f'''<script>(function(){{
var EU=/^(Europe\\/|Atlantic\\/(Azores|Madeira|Canary|Faeroe|Reykjavik)$|Arctic\\/Longyearbyen$)/;
var KEY="vtag-consent";
function load(){{var s=document.createElement("script");s.id="vtag-ai-js";s.async=true;
s.src="{VISITOR_TAG_SRC}";s.setAttribute("data-pid","{VISITOR_TAG_PID}");
s.setAttribute("data-version","{VISITOR_TAG_VERSION}");document.head.appendChild(s);}}
var tz="";try{{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||"";}}catch(e){{}}
var stored=null;try{{stored=localStorage.getItem(KEY);}}catch(e){{}}
if(!EU.test(tz)||stored==="yes"){{if(stored!=="no")load();return;}}
if(stored==="no")return;
document.addEventListener("DOMContentLoaded",function(){{
var b=document.createElement("div");b.className="consent";b.setAttribute("role","dialog");
b.setAttribute("aria-label","Visitor identification consent");
b.innerHTML='<p>This site can identify visiting organisations so business enquiries can be followed up. It is not advertising. <a href="/privacy/">How it works</a>.</p><div class="consent-actions"><button type="button" data-consent="no">Decline</button><button type="button" data-consent="yes" class="consent-yes">Allow</button></div>';
b.addEventListener("click",function(e){{var t=e.target.closest("[data-consent]");if(!t)return;
try{{localStorage.setItem(KEY,t.dataset.consent);}}catch(err){{}}
if(t.dataset.consent==="yes")load();b.remove();}});
document.body.appendChild(b);}});
}})();</script>'''

SOCIALS = {
    "LinkedIn": "https://www.linkedin.com/in/kunaal-naik/",
    "YouTube": "https://www.youtube.com/KunaalNaik",
    "Instagram": "https://www.instagram.com/coachkunaal/",
    "GitHub": "https://github.com/KunaalNaik",
}

# Entity corroboration for Google and LLM citation. Verified reachable 2026-08-10.
# Only add a URL here after confirming it is Kunaal's own profile.
SAME_AS = list(SOCIALS.values()) + ["https://datasciencemasterminds.com/"]

# Minimum engagement, stated publicly to filter low-ticket enquiries.
ENGAGEMENT_FLOOR = "Engagements start at a one-day executive briefing or a two-week workflow sprint. Kunaal does not take one-off hourly tool demos."

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#kunaal-naik",
    "name": "Kunaal Naik",
    "url": f"{SITE}/",
    "image": f"{SITE}/assets/kunaal-naik.webp",
    "jobTitle": "Corporate AI Trainer and AI Workflow Consultant",
    "description": "Kunaal Naik helps professionals, business owners, and teams turn AI tools into practical, governed workflows.",
    "sameAs": SAME_AS,
    "founder": {"@type": "Organization", "name": "Data Science Masterminds", "url": "https://datasciencemasterminds.com/"},
}

# Primary nav. Grouped by how a buyer actually shops: what they need, who they
# are, what they're evaluating. A flat list cannot carry 37 pages.
# (label, url) = plain link. (label, None, [(label,url,blurb)...]) = dropdown.
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
        ("What it costs", "/corporate-ai-training-cost-india/", "The six drivers of the fee"),
        ("Choosing a trainer", "/how-to-choose-a-corporate-ai-trainer/", "Criteria, and red flags"),
        ("RFP template", "/corporate-ai-training-rfp-template/", "Free, ungated, provider-neutral"),
        ("Measuring ROI", "/ai-training-roi-measurement/", "Baselines before delivery"),
        ("Case studies", "/case-studies/", "Inspectable proof"),
    ]),
    ("About", "/about-kunaal-naik/"),
]


def esc(value):
    return html.escape(str(value), quote=True)


def mailto(subject):
    return f"mailto:{EMAIL}?subject={esc(subject).replace(' ', '%20')}"


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
    items = [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Kunaal Naik"}, PERSON, webpage]
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
    data = json.dumps(schemas(kind, title, description, path, faqs), ensure_ascii=False, separators=(",", ":"))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kunaal Naik"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/og-kunaal-naik.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SITE}/assets/og-kunaal-naik.jpg">
<link rel="stylesheet" href="/assets/site.css"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{data}</script>{VISITOR_TAG}</head><body>{header()}<main id="main">{body}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>'''


def page_hero(kicker, title, lede, current):
    return f'''<section class="page-hero"><div class="page-hero-inner"><div class="breadcrumbs"><a href="/">Home</a> / {esc(current)}</div><p class="eyebrow">{esc(kicker)}</p><h1>{title}</h1><p class="lede">{lede}</p></div></section>'''


def cta(title, text, subject):
    return f'''<section class="section cta-band"><div class="section-inner"><div><p class="eyebrow">Start a useful conversation</p><h2>{title}</h2><p>{text}</p></div><div class="cta-actions"><a class="button button-light" href="{mailto(subject)}">Email {EMAIL}</a></div></div></section>'''


def sidebar(label, text, subject):
    return f'''<aside class="sidebar"><div class="panel panel-accent"><span class="tag">{label}</span><h3>Start with the outcome.</h3><p>{text}</p><a class="button" href="{mailto(subject)}">Email Kunaal</a></div></aside>'''


home = f'''<section class="hero"><div class="hero-grid"><div class="hero-copy"><p class="eyebrow">Corporate AI training · Workflow consulting</p><h1>Move from AI experiments to <em>working systems.</em></h1><p class="lede">Kunaal Naik helps leaders, teams, SMBs, and MSMEs identify one valuable workflow, train the people doing the work, implement the right AI approach, and measure whether it improved.</p><div class="hero-actions"><a class="button button-primary" href="{mailto('AI training or consulting enquiry')}">Discuss your AI priority</a><a class="button button-light" href="/corporate-ai-training/">Explore training</a></div><div class="proof-strip"><div><strong>Trainer + implementer</strong><span>Capability, not tool theatre</span></div><div><strong>Enterprise-aware</strong><span>Governance and approval gates</span></div><div><strong>Global delivery</strong><span>Onsite, remote, and hybrid</span></div></div></div><div class="hero-portrait"><div class="portrait-frame"><img src="/assets/kunaal-naik.webp" width="719" height="720" alt="Kunaal Naik, corporate AI trainer and consultant"></div><div class="portrait-note">Founder · Data Science Masterminds<br>TEDx speaker</div></div></div></section>
<section class="section section-white"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Where Kunaal helps</p><h2>AI enablement for work that matters.</h2></div><p class="section-intro">The offer is deliberately practical: identify a valuable workflow, equip the people closest to it, implement safely, and prove whether it improved the work.</p></div><div class="service-grid">
<a class="service-card" href="/corporate-ai-training/"><span class="number">01 / TRAIN</span><h3>Corporate AI training</h3><p>Role-based workshops for leaders and functional teams, designed around real work rather than generic demos.</p><span class="arrow">→</span></a>
<a class="service-card" href="/ai-automation-consulting/"><span class="number">02 / IMPLEMENT</span><h3>AI workflow consulting</h3><p>A focused path from workflow inventory to a governed pilot and internal operating capability.</p><span class="arrow">→</span></a>
<a class="service-card" href="/claude-cowork-training/"><span class="number">03 / ENABLE</span><h3>Claude Cowork enablement</h3><p>Teach knowledge-work teams to brief, supervise, verify, and reuse multi-step AI work.</p><span class="arrow">→</span></a>
<a class="service-card" href="/hermes-agent-training/"><span class="number">04 / OPERATE</span><h3>Hermes Agent setup</h3><p>Persistent memory, skills, tools, schedules, and guardrails for a reusable AI operating layer.</p><span class="arrow">→</span></a>
<a class="service-card" href="/ai-agents-for-professionals/"><span class="number">05 / UPSKILL</span><h3>AI agents for professionals & founders</h3><p>Move beyond prompting into business problems, workflow design, delegation, verification, and responsible implementation.</p><span class="arrow">→</span></a>
<a class="service-card" href="/speaking-and-workshops/"><span class="number">06 / ALIGN</span><h3>Executive sessions & workshops</h3><p>Create a shared language for opportunity, risk, governance, and the next 90 days.</p><span class="arrow">→</span></a></div></div></section>
<section class="section"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Ways to start</p><h2>One workflow before a transformation.</h2></div><p class="section-intro">Choose the smallest engagement that can create a useful decision, a working artifact, or measurable adoption. Expand only after evidence exists.</p></div><div class="fit-grid"><div class="fit-card"><span class="tag">01 / ALIGN</span><strong>AI adoption briefing</strong><p>Executive alignment, live demonstrations, opportunity framing, and clear next decisions.</p></div><div class="fit-card"><span class="tag">02 / APPLY</span><strong>Hands-on workflow lab</strong><p>Use real artifacts to design two or three role-specific workflows with review boundaries.</p></div><div class="fit-card"><span class="tag">03 / IMPLEMENT</span><strong>AI Workflow Sprint</strong><p>A focused 2–4 week build: one workflow, the right agent or automation, guardrails, team training, and a measurement plan.</p></div><div class="fit-card"><span class="tag">04 / ADOPT</span><strong>90-day adoption partner</strong><p>Office hours, champions, workflow refinement, governance, and outcome reporting after launch.</p></div></div></div></section>
<section class="section"><div class="section-inner"><div class="split"><div><p class="eyebrow">Two buying realities</p><h2>Enterprise discipline. Owner-led speed.</h2><p class="section-intro">Large organizations and growing businesses have different constraints. The method adapts without lowering the standard.</p></div><div class="fit-grid"><div class="fit-card"><strong>Enterprise teams</strong><p>Role-based adoption, governance, data boundaries, champions, and repeatable learning paths.</p></div><div class="fit-card"><strong>SMBs & MSMEs</strong><p>One high-value workflow first, a visible owner, a lean tool stack, and a practical handover.</p></div></div></div></div></section>
<section class="section section-dark"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">The operating model</p><h2>Brief. Build. Verify. Transfer.</h2></div><p class="section-intro">AI fluency is not prompt volume. It is the ability to delegate responsibly, describe the work clearly, discern quality, and remain diligent about impact.</p></div><div class="process"><article><h3>Frame</h3><p>Define the outcome, user, constraints, source material, and what “done” means.</p></article><article><h3>Prototype</h3><p>Build the smallest workflow that can demonstrate value and expose risk.</p></article><article><h3>Verify</h3><p>Check facts, decisions, data handling, failure modes, and human approvals.</p></article><article><h3>Transfer</h3><p>Document the method, train the owner, and measure adoption and outcomes.</p></article></div></div></section>
<section class="section section-white"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Mission</p><h2>Make AI accessible, practical, and useful.</h2></div><p class="section-intro">The goal is not more tool knowledge. It is helping people understand the work, build useful capability, make better decisions, and keep human judgment accountable as AI scales.</p></div><div class="fit-grid"><div class="fit-card"><strong>Business first</strong><p>Start with the problem, user, decision, data, and metric before choosing technology.</p></div><div class="fit-card"><strong>Practical over perfect</strong><p>Build the smallest useful version, expose risk early, and improve after evidence exists.</p></div><div class="fit-card"><strong>Accessible, not careless</strong><p>Non-technical people can begin without removing verification, governance, or ownership.</p></div><div class="fit-card"><strong>Capability that stays</strong><p>Document the method, train the owner, and avoid permanent black-box dependency.</p></div></div></div></section>
{cta('What should AI improve in your organization?', 'Share the team, workflow, friction, and desired outcome. You will get a direct response by email.', 'AI training or workflow consulting enquiry')}'''


SERVICES = {
"corporate-ai-training": {
    "title": "Corporate AI Training for Leaders and Teams | Kunaal Naik",
    "description": "Hands-on corporate AI training that connects business problems, role-based workflows, verification, and responsible adoption.",
    "kicker": "Corporate AI training",
    "h1": "Build AI capability around <em>real work.</em>",
    "lede": "Practical workshops for leadership, operations, marketing, sales, HR, and cross-functional teams. Participants begin with business outcomes and real work, then learn the appropriate AI methods without needing a technical background.",
    "problem": "Most AI workshops create excitement but little operating change. Teams see impressive demos, then return to unclear policies, weak context, scattered prompts, and no shared method for deciding what to trust.",
    "outcomes": ["A business problem and measurable outcome defined before tool selection", "Role-specific workflows participants can apply immediately", "A repeatable method for briefing, supervising, and checking AI work", "A prioritized 30/60/90-day adoption backlog", "Clear human-approval and data-handling boundaries"],
    "formats": ["Executive AI briefing — strategy, governance, and portfolio decisions", "Direct trainer-led discovery and programme design", "Role-based workshop — hands-on workflows for one function", "AI workflow lab — teams redesign a live process", "Enablement programme — workshops, office hours, champions, and measurement"],
    "fit": "CHRO, L&D, transformation, business-unit, and functional leaders who need adoption—not another inspirational keynote.",
    "subject": "Corporate AI training enquiry",
},
"ai-automation-consulting": {
    "title": "AI Automation Consulting for Enterprises, SMBs and MSMEs | Kunaal Naik",
    "description": "Practical AI workflow consulting: identify high-value work, prototype safely, implement with owners, and measure business outcomes.",
    "kicker": "AI workflow consulting",
    "h1": "Automate the right work—<em>not everything.</em>",
    "lede": "A focused consulting path for enterprises, SMBs, and MSMEs: understand the business problem, data, people, and approvals first, then implement the smallest useful AI workflow without a bloated transformation programme.",
    "problem": "The usual failure mode is tool-first automation: buy software, automate an unstable process, discover missing data and approvals, then leave the team with a fragile workflow nobody owns.",
    "outcomes": ["A workflow inventory scored by value, feasibility, risk, and proof", "One bounded pilot with a named human owner", "Documented inputs, decisions, approvals, exceptions, and fallback", "A practical handover and team enablement plan", "Baseline and after-state measures for time, quality, rework, and risk"],
    "formats": ["AI workflow opportunity audit", "Fixed-scope workflow sprint", "Team implementation and handover", "Fractional AI enablement advisory"],
    "fit": "Owner-led businesses, functional leaders, and transformation teams that want a useful first win and a method they can reuse.",
    "subject": "AI workflow consulting enquiry",
},
"claude-cowork-training": {
    "title": "Claude Cowork Training and Enablement for Teams | Kunaal Naik",
    "description": "Claude Cowork training for teams: projects, files, multi-step work, supervision, verification, connectors, and safe reusable workflows.",
    "kicker": "Claude Cowork training",
    "h1": "Make Claude Cowork a <em>supervised teammate.</em>",
    "lede": "Help knowledge-work teams use Claude Cowork for multi-step work across files, research, analysis, documents, spreadsheets, and recurring tasks—without confusing fluent output with reliable work.",
    "problem": "Cowork can coordinate complex work, but capability alone does not create adoption. Teams need outcome contracts, context packs, reusable project instructions, decision boundaries, and disciplined checks.",
    "outcomes": ["A clear Cowork task loop: brief, plan, act, review, revise", "Role-specific examples using real-but-safe work", "Project instructions and reusable workflow patterns", "Verification checklists for research, documents, and analysis", "Governance guidance for files, connectors, approvals, and sensitive work"],
    "formats": ["Claude Cowork executive demonstration", "Hands-on team workshop", "Role-based workflow design lab", "Project and instruction setup sprint"],
    "fit": "Consulting, operations, marketing, research, finance, and leadership teams on Claude paid, Team, or Enterprise plans.",
    "subject": "Claude Cowork training enquiry",
},
"hermes-agent-training": {
    "title": "Hermes Agent Training, Setup and Business Workflows | Kunaal Naik",
    "description": "Hermes Agent setup and training for persistent memory, reusable skills, tools, schedules, channels, and governed business workflows.",
    "kicker": "Hermes Agent consulting",
    "h1": "Build an AI operating layer that <em>remembers.</em>",
    "lede": "Setup, training, and workflow design for teams and professionals who want a persistent AI agent with memory, reusable skills, tools, scheduled jobs, and cross-channel operation.",
    "problem": "A persistent agent is more powerful than a disposable chat—and more demanding. Poor memory, oversized instructions, unsafe tools, noisy schedules, and missing approval gates create operational debt quickly.",
    "outcomes": ["A clean Hermes profile, identity, memory, and model configuration", "Reusable skills for stable business procedures", "Approved tools and integrations with explicit boundaries", "Useful scheduled workflows that stay quiet when nothing changes", "A maintenance and review method your team can own"],
    "formats": ["Hermes setup and architecture session", "Personal AI operating system build", "Team skills and workflow workshop", "Persistent automation implementation sprint"],
    "fit": "Founders, consultants, operators, and technical teams ready to move beyond disposable chat into a governed, extensible agent.",
    "subject": "Hermes Agent setup and training enquiry",
},
"ai-agents-for-professionals": {
    "title": "AI Agents for Professionals and Founders | Kunaal Naik",
    "description": "Practical AI agent training for professionals and founders: business problems, workflows, delegation, verification, automation, and ethical services.",
    "kicker": "AI agents for professionals and founders",
    "h1": "Stop collecting prompts. Start <em>operating AI.</em>",
    "lede": "A practical learning path for professionals and founders who want to build useful AI workflows, delegate meaningful work, and keep judgment, quality, and accountability in human hands—without needing to begin as a programmer.",
    "problem": "Tool tutorials expire. Prompt libraries become clutter. The durable advantage is learning to choose outcomes, assemble context, decompose work, supervise execution, verify results, and preserve successful methods.",
    "outcomes": ["A portfolio of bounded AI workflows tied to real business or career problems", "The D4–LOOP method for delegation and supervision", "A reusable context and verification discipline", "A clear boundary between assistance and accountable judgment", "A roadmap from manual use to stable automation", "For founders, a responsible path from a proven workflow to a clearly scoped service—without income guarantees"],
    "formats": ["Professional AI fluency workshop", "AI operator cohort for teams", "Personal workflow portfolio sprint", "Founder workflow-to-service lab", "Leadership-to-operator alignment session"],
    "fit": "Mid-career professionals, managers, consultants, founders, solopreneurs, coaches, and operators who need working capability rather than another tools overview.",
    "subject": "AI agents for professionals enquiry",
},
}


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

about = f'''{page_hero('About Kunaal Naik', 'Making advanced AI <em>useful in everyday work.</em>', 'Kunaal Naik is the founder of Data Science Masterminds, a corporate AI trainer, practical AI adoption consultant, AI automation coach, and TEDx speaker.', 'About')}<section class="section"><div class="section-inner content-grid"><article class="prose"><h2>The bridge between knowing and doing</h2><p>Kunaal works at the intersection of data, learning, business operations, automation, and entrepreneurship. The through-line is helping people understand complex capability, connect it to meaningful work, and build enough confidence and discipline to use it repeatedly.</p><p>His focus is not a particular tool. It is the operating system around useful AI: the people, business context, data, instructions, approval boundaries, reusable procedures, and measurement that turn an experiment into a working capability.</p><h2>Vision and mission</h2><p><strong>Vision:</strong> make AI accessible, practical, and useful for professionals, founders, and business teams regardless of technical background.</p><p><strong>Mission:</strong> train and equip people to understand, build, supervise, and improve AI workflows that solve real business problems.</p><h2>How Kunaal works</h2><ul><li><strong>Business problem before technology:</strong> understand the work, decision, customer, data, and metric before choosing AI, automation, or code.</li><li><strong>Practical over perfect:</strong> build the smallest version that can expose value, risk, and missing information.</li><li><strong>Build, do not merely consume:</strong> leave with an artifact, workflow, decision, or implementation plan—not only notes.</li><li><strong>Accessibility without carelessness:</strong> make complex ideas understandable while preserving verification and governance.</li><li><strong>Human accountability:</strong> keep sensitive data, consequential decisions, approvals, and published outcomes under human judgment.</li><li><strong>Capability transfer:</strong> document the method, train the owner, and avoid permanent black-box dependency.</li></ul><h2>Who he helps</h2><p>Kunaal works with enterprise leaders and teams seeking governed adoption; SMBs and MSMEs choosing their first valuable workflow; professionals building an AI workflow portfolio; and founders using agents for operations or developing an ethical service around a proven business problem.</p><h2>Tools are a means, not the offer</h2><p>Claude Cowork and Hermes Agent make multi-step, agentic work tangible. Kunaal also works with AI agents, no-code and low-code automation, n8n, data workflows, and the surrounding practices required for responsible adoption.</p><h2>Public profiles</h2><ul><li><a href="https://www.linkedin.com/in/kunaal-naik/">LinkedIn</a></li><li><a href="https://www.youtube.com/KunaalNaik">YouTube</a></li><li><a href="https://www.instagram.com/coachkunaal/">Instagram</a></li><li><a href="https://www.youtube.com/watch?v=JTNNR9uvKPo">TEDxBBAU: The Invisible Work Behind Visible Luck</a></li><li><a href="https://datasciencemasterminds.com/">Data Science Masterminds</a></li></ul></article>{sidebar('Direct practitioner access', 'Kunaal personally leads discovery, facilitation, and workflow design for scoped engagements.', 'Work with Kunaal')}</div></section>{cta('What capability should your team build?', 'Share the audience, work, friction, and desired outcome. The first response will identify the smallest useful starting point.', 'Work with Kunaal')}'''

speaking = f'''{page_hero('Speaking and workshops', 'A talk should change the <em>next decision.</em>', 'Executive briefings, leadership sessions, hands-on workshops, panels, and practical demonstrations on AI adoption, AI agents, Claude Cowork, Hermes Agent, and the future of knowledge work.', 'Speaking & workshops')}<section class="section"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Formats</p><h2>Built for the room.</h2></div><p class="section-intro">Every session starts with the audience, business context, existing AI maturity, and the action participants should take next.</p></div><div class="fit-grid"><div class="fit-card"><strong>Executive briefing</strong><p>Opportunity portfolio, governance, workforce implications, and near-term decisions.</p></div><div class="fit-card"><strong>Role-based workshop</strong><p>Hands-on practice with workflows, context, supervision, and verification.</p></div><div class="fit-card"><strong>Workflow lab</strong><p>Redesign a real process and leave with a bounded pilot and named owner.</p></div><div class="fit-card"><strong>Keynote or panel</strong><p>A grounded point of view on agents, automation, and responsible AI adoption.</p></div></div></div></section><section class="section section-white"><div class="section-inner split"><div><p class="eyebrow">Sample topics</p><h2>From chat user to AI operator.</h2></div><ul class="list-clean"><li>The D4–LOOP AI Operator OS</li><li>Claude Cowork for business teams: capability, failure modes, and governance</li><li>Hermes Agent: memory, skills, tools, and persistent workflows</li><li>How to choose the first enterprise or MSME AI workflow</li><li>Why polished AI output is dangerous without verification</li><li>The invisible work behind visible AI adoption</li></ul></div></section>{cta('Planning a leadership session or team workshop?', 'Include the audience, approximate group size, location or online format, desired date, and the decision or capability the session should create.', 'Speaking or workshop enquiry')}'''

cases = f'''{page_hero('Case studies', 'Proof should be <em>inspectable.</em>', 'Approved training and workflow case studies with context, implementation decisions, limitations, and a clear distinction between demonstrations and production outcomes.', 'Case studies')}<section class="section"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Training case study</p><h2>Claude workflow training for a GCC consulting firm.</h2></div><p class="section-intro">A claim-safe record of hands-on demonstrations spanning documents, spreadsheets, presentations, dashboards, SQL, project memory, and scheduled workflows.</p></div><div class="service-grid"><a class="service-card" href="/case-studies/gcc-consulting-firm-claude-cowork-training/"><span class="number">GCC CONSULTING FIRM</span><h3>From business files to supervised AI workflows</h3><p>Invoice-document processing, parallel executive reporting, browser-ready dashboards, natural-language data analysis, CLAUDE.md memory, and reusable project structure.</p><span class="arrow">Read case study →</span></a></div></div></section><section class="section section-white"><div class="section-inner split"><div><p class="eyebrow">Evidence standard</p><h2>Demonstration is not deployment.</h2></div><p class="section-intro">Public case studies state what was demonstrated, what controls were discussed, and what production would still require. Quantified outcomes remain unpublished until records and permission support them.</p></div></section>{cta('Have a workflow worth documenting?', 'Kunaal can help define a bounded pilot and an evidence plan before implementation begins.', 'AI workflow pilot enquiry')}'''

gcc_case = f'''{page_hero('GCC consulting firm · Training case study', 'From business files to <em>supervised AI workflows.</em>', 'Hands-on Claude Cowork and Claude Code training covering document processing, parallel reporting, dashboards, SQL analysis, project memory, reusable code, and scheduled workflows.', 'GCC consulting firm case study')}<section class="section"><div class="section-inner content-grid"><article class="prose"><h2>Context</h2><p>During hands-on training for a GCC consulting firm, participants explored how documents, spreadsheets, databases, reusable code, project instructions, and scheduled agents can become supervised business workflows.</p><blockquote>This is a training and prototype case study—not a claim of production deployment, audited savings, guaranteed accuracy, or client-endorsed results.</blockquote><h2>What the sessions demonstrated</h2><h3>1. Invoice-document processing</h3><p>Sample invoice PDFs moved through a clear input-to-output workflow: document vision extracted reviewable fields such as supplier, date, amount, and line items; structured results could then be validated before database or spreadsheet entry. Exceptions remained visible for human review.</p><h3>2. Parallel executive reporting</h3><p>An orchestrator divided department-level hiring data between independent agents. One created an executive KPI summary while another produced a department-focused presentation. Once reviewed, reusable code could handle later datasets without rebuilding the workflow from scratch.</p><h3>3. Browser-ready HTML dashboards</h3><p>Fictitious CSV data became a self-contained HTML report with KPI cards, charts, and department views. A <code>DESIGN.md</code> file supplied approved visual rules so outputs remained consistent and portable.</p><h3>4. Natural-language SQL analysis</h3><p>In a controlled environment, business questions were translated into inspectable SQL against Supabase. Examples progressed from simple filters to joins, common table expressions, and window functions. Production use would require least-privilege access, query review, auditability, and safe handling of consequential outputs.</p><h3>5. Durable context with CLAUDE.md</h3><p>A project-level <code>CLAUDE.md</code> recorded completed work, decisions, gotchas, files, checks, limitations, and next steps. It gave the agent useful context when work resumed. The correct filename is <code>CLAUDE.md</code>—not cloud.md.</p><h3>6. Safe multi-agent folder boundaries</h3><ul><li><code>input/</code> for raw files and approved source material</li><li><code>output/</code> for reviewed deliverables</li><li><code>code/</code> for reusable scripts</li><li><code>temp/</code> for work in progress</li><li><code>archive/</code> for superseded files retained safely</li><li><code>CLAUDE.md</code> for project context and decisions</li><li><code>DESIGN.md</code> for visual and brand rules</li></ul><p>Bounded folders helped parallel agents avoid overwriting each other and made ownership easier to inspect.</p><h3>7. Scheduled reporting</h3><p>The sessions connected stable steps into a scheduled reporting pattern: collect approved inputs, analyse them, generate a presentation or HTML report, route it for review or approved delivery, and record exceptions. Human approval remains necessary for sensitive data, consequential decisions, and external communication.</p><h3>8. Retrieval and reconciliation</h3><p>Advanced discussion covered semantic retrieval, document versions, reranking, and reconciliation. The central lesson was that retrieval quality must be evaluated; adding a vector database does not by itself create a reliable knowledge system.</p><h2>What participants could take away</h2><ul><li>A repeatable input → process → review → output pattern</li><li>Clear separation between source files, temporary work, code, and approved deliverables</li><li>A method for delegating independent work in parallel</li><li>Reusable project memory and visual rules</li><li>Explicit human-review and production-readiness questions</li></ul><h2>What production would still require</h2><ul><li>Approved data access and least-privilege credentials</li><li>Representative test data and exception coverage</li><li>Accuracy, cost, latency, and failure measurements</li><li>Logging, ownership, fallback procedures, and incident handling</li><li>Security, privacy, legal, and records-retention review</li><li>Written approval before publishing organization-specific outcomes</li></ul></article>{sidebar('Training case study', 'This page documents the GCC Consulting Firm training. Quantified claims remain withheld pending evidence and permission.', 'GCC workflow training enquiry')}</div></section>{cta('Want a workflow lab for your team?', 'Bring one representative document, spreadsheet, report, or data question. The session will define a safe demonstration and the evidence needed for a pilot.', 'GCC workflow training enquiry')}'''

insights = f'''{page_hero('Insights', 'Original operating notes—not <em>AI content volume.</em>', 'A focused library on AI fluency, enterprise adoption, Claude Cowork, Hermes Agent, workflow design, verification, and measurable business use.', 'Insights')}<section class="section"><div class="section-inner"><div class="section-head"><div><p class="eyebrow">Publishing roadmap</p><h2>The first evidence-rich guides.</h2></div><p class="section-intro">The base site establishes the topics. Each article will add screenshots, worked examples, decisions, failures, sources, and reusable artifacts before publication.</p></div><div class="service-grid"><article class="service-card"><span class="number">DECISION GUIDE</span><h3>Claude Cowork vs Hermes Agent</h3><p>Managed knowledge-work agent or persistent customizable operating layer?</p></article><article class="service-card"><span class="number">TRAINING</span><h3>Corporate AI training in India</h3><p>A role-based curriculum for leadership and functional teams.</p></article><article class="service-card"><span class="number">MEASUREMENT</span><h3>How to measure AI workshop ROI</h3><p>Adoption, time, quality, rework, risk, and review burden.</p></article><article class="service-card"><span class="number">CLAUDE COWORK</span><h3>A safe Cowork setup</h3><p>Projects, instructions, connectors, approvals, and verification.</p></article><article class="service-card"><span class="number">HERMES AGENT</span><h3>Weekly market-intelligence agent</h3><p>Workflow, sources, checks, failure modes, and cost.</p></article><article class="service-card"><span class="number">AI FLUENCY</span><h3>The D4–LOOP framework</h3><p>Delegate, describe, discern, and stay diligent through execution.</p></article></div></div></section>{cta('Want a specific guide or internal briefing?', 'Email the business question and intended audience. Useful questions become prioritized research, not generic posts.', 'AI research or briefing request')}'''

CONTACT_FAQS = [
    ("What is the minimum engagement?",
     "Engagements start at a one-day executive briefing or a two-week workflow sprint. Kunaal does not take one-off hourly tool demonstrations or single-session ChatGPT walkthroughs."),
    ("Who is this for?",
     "Enterprise L&D and transformation teams, functional leaders with a budget, and owner-led businesses committing to implementation. Work is scoped per organisation, not sold as seats."),
    ("Do you deliver outside India?",
     "Yes. Delivery runs onsite, remote, and hybrid across Indian, Gulf, European, UK, and US timezone bands, contracted in INR or USD."),
    ("Is this training or implementation?",
     "Both, and that is the point. Training alone rarely changes the work. Engagements pair role-based training with one implemented, governed workflow and a measurement plan."),
    ("What do we need before starting?",
     "One valuable workflow worth improving, the people who own it, and an approver for data and tool access. A named business priority matters more than existing AI maturity."),
]

contact = f'''{page_hero('Contact', 'Start with the work—not a <em>sales form.</em>', 'Email Kunaal directly about corporate AI training, AI workflow consulting, Claude Cowork, Hermes Agent, speaking, or partnerships.', 'Contact')}<section class="section"><div class="section-inner split"><div><p class="eyebrow">Email</p><h2><a href="mailto:{EMAIL}">{EMAIL}</a></h2><p class="section-intro">{ENGAGEMENT_FLOOR}</p><p class="section-intro">So the first reply is useful rather than a discovery call, include these five things:</p><ol class="list-clean"><li><strong>Organisation</strong> and your role</li><li><strong>Team size</strong> and the function involved</li><li><strong>Business priority or workflow</strong> you want improved</li><li><strong>Budget band</strong> and approval status</li><li><strong>Timeline</strong> and what success would look like</li></ol><a class="button button-primary" href="{mailto('Corporate AI training or consulting enquiry')}">Email with these details</a></div><div class="panel"><h3>Suggested subject lines</h3><ul class="list-clean"><li>Corporate AI training enquiry</li><li>AI workflow assessment for our business</li><li>Claude Cowork workshop for our team</li><li>Hermes Agent setup and training</li><li>Speaking or partnership enquiry</li></ul><h3>Not a fit</h3><ul class="list-clean"><li>Hourly tool demonstrations</li><li>Single-session ChatGPT walkthroughs</li><li>Certificate-only programmes</li><li>Unpaid pilots or spec work</li></ul><h3>Elsewhere</h3><div class="socials">{''.join(f'<a href="{u}">{n}</a>' for n,u in SOCIALS.items())}</div></div></div></section>{faq_section(CONTACT_FAQS)}'''

privacy = f'''{page_hero('Privacy', 'What this site <em>collects, and why.</em>', 'This website has no contact form, account system, advertising network, or newsletter signup. It does run one third-party visitor-identification script, described below.', 'Privacy')}<section class="section"><div class="section-inner"><article class="prose"><h2>Information you choose to send</h2><p>If you email {EMAIL}, your email provider and Kunaal’s email provider process the message and associated metadata. Use email only for information you are comfortable sharing for the purpose of the enquiry.</p><h2>Website hosting</h2><p>The site is hosted on Vercel. Hosting infrastructure may process standard request information such as IP address, user agent, requested URL, and timestamps for security and service operation.</p><h2>Visitor identification</h2><p>This site loads a third-party script from Leadsy (<code>r2.leadsy.ai</code>) on every page. It is used to understand which organisations are visiting so that business enquiries can be followed up. Depending on the provider’s data sources, it may process your IP address, pages viewed, referrer, device and browser information, and attempt to associate that activity with a company or professional profile.</p><p>This is business-visitor identification, not an advertising network, and the data is not sold on from here. If you do not want to be identified this way, use a browser that blocks third-party scripts, an ad or tracker blocker, or a VPN. You can also email {EMAIL} to ask that any record associated with your visit be deleted.</p><p>Because this processing can involve personal data, it is treated as non-essential for visitors in the EU, UK, EEA, and Switzerland. If your browser reports a European timezone, the script does <strong>not</strong> load until you choose “Allow” on the consent notice, and your choice is remembered in your browser’s local storage. Choosing “Decline” means it never loads. Outside those regions the script loads on page view, as described above.</p><h2>Analytics and cookies</h2><p>No separate analytics or advertising cookies are intentionally set beyond what the visitor-identification script above requires. This policy will be updated before any further analytics or third-party embeds are added.</p><h2>External links</h2><p>Links to LinkedIn, YouTube, Instagram, GitHub, Data Science Masterminds, and other websites are governed by those services’ own policies.</p><h2>Questions or removal requests</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></article></div></section>'''

terms = f'''{page_hero('Terms', 'Clear boundaries for an <em>informational website.</em>', 'These terms cover use of the public KunaalNaik.com website. Separate written terms apply to paid engagements.', 'Terms')}<section class="section"><div class="section-inner"><article class="prose"><h2>Informational content</h2><p>Website content is general educational and marketing information. It is not legal, financial, security, employment, or investment advice and does not create a client relationship.</p><h2>No guaranteed outcome</h2><p>AI training and consulting outcomes depend on the organization, participants, data, systems, implementation, and ongoing use. No ranking, revenue, productivity, automation, or adoption result is guaranteed.</p><h2>Intellectual property</h2><p>Unless otherwise stated, original site copy, frameworks, and design are owned by Kunaal Naik. You may link to public pages and quote short excerpts with attribution.</p><h2>External tools</h2><p>Claude Cowork, Hermes Agent, n8n, and other product names belong to their respective owners. Mention does not imply endorsement or partnership.</p><h2>Engagements</h2><p>Scope, deliverables, confidentiality, data handling, fees, and commercial terms for any engagement must be agreed separately in writing.</p><h2>Contact</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></article></div></section>'''

not_found = f'''<section class="not-found"><div><strong>404</strong><h1>This page does not exist.</h1><p>The link may be outdated, or the page may have moved.</p><a class="button button-primary" href="/">Return home</a></div></section>'''

PAGES = {
    "index.html": ("Corporate AI Trainer & AI Workflow Consultant | Kunaal Naik", "Corporate AI training and practical AI workflow consulting for enterprise teams, SMBs and MSMEs using Claude Cowork, Hermes Agent, AI agents and automation.", "/", home, "WebPage"),
    "about-kunaal-naik/index.html": ("About Kunaal Naik | Corporate AI Trainer and Consultant", "Kunaal Naik is the founder of Data Science Masterminds, an AI trainer, consultant, automation coach and TEDx speaker.", "/about-kunaal-naik/", about, "ProfilePage"),
    "speaking-and-workshops/index.html": ("AI Speaker and Corporate Workshops | Kunaal Naik", "Executive briefings, leadership sessions and hands-on workshops on AI adoption, AI agents, Claude Cowork, Hermes Agent and knowledge work.", "/speaking-and-workshops/", speaking, "Service"),
    "case-studies/index.html": ("AI Training and Workflow Case Studies | Kunaal Naik", "Evidence-backed AI training and workflow case studies with context, implementation decisions, limitations and measurable outcomes.", "/case-studies/", cases, "WebPage"),
    "case-studies/gcc-consulting-firm-claude-cowork-training/index.html": ("Claude Cowork Training Case Study | GCC Consulting Firm", "A GCC consulting firm training case study covering document processing, parallel reporting, dashboards, SQL, CLAUDE.md memory, and scheduled AI workflows.", "/case-studies/gcc-consulting-firm-claude-cowork-training/", gcc_case, "WebPage"),
    "insights/index.html": ("AI Adoption, Claude Cowork and Hermes Agent Insights | Kunaal Naik", "Practical guides on AI fluency, corporate adoption, Claude Cowork, Hermes Agent, workflow design, verification and business outcomes.", "/insights/", insights, "WebPage"),
    "contact/index.html": ("Contact Kunaal Naik | AI Training and Consulting", "Email Kunaal Naik about corporate AI training, workflow consulting, Claude Cowork, Hermes Agent, speaking or partnerships.", "/contact/", contact, "WebPage", CONTACT_FAQS),
    "privacy/index.html": ("Privacy | Kunaal Naik", "Privacy information for KunaalNaik.com.", "/privacy/", privacy, "WebPage"),
    "terms/index.html": ("Terms | Kunaal Naik", "Website terms for KunaalNaik.com.", "/terms/", terms, "WebPage"),
    "404.html": ("Page Not Found | Kunaal Naik", "The requested page does not exist.", "/404.html", not_found, "WebPage"),
}

for slug, item in SERVICES.items():
    PAGES[f"{slug}/index.html"] = (item["title"], item["description"], f"/{slug}/", service_body(item), "Service")

# The 23 structural pages (competitor teardown, axes 1-4). Same renderer, same
# schema path — FAQs flow into FAQPage markup via page()'s faqs kwarg.
for slug, item in STRUCTURAL.items():
    PAGES[f"{slug}/index.html"] = (item["title"], item["description"], f"/{slug}/",
                                   service_body(item), "Service", item.get("faqs"))

for filename, entry in PAGES.items():
    title, description, path, body, kind = entry[:5]
    faqs = entry[5] if len(entry) > 5 else None
    destination = ROOT / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page(title, description, path, body, kind, faqs), encoding="utf-8")

public_paths = sorted(path for filename, entry in PAGES.items() if filename != "404.html" for path in [entry[2]])
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in public_paths:
    sitemap.append(f"  <url><loc>{SITE}{path}</loc><lastmod>2026-08-08</lastmod></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

robots = f'''User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

Sitemap: {SITE}/sitemap.xml
'''
(ROOT / "robots.txt").write_text(robots, encoding="utf-8")
print(f"Built {len(PAGES)} HTML pages and {len(public_paths)} sitemap URLs")
