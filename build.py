#!/usr/bin/env python3
"""Build the dependency-free static KunaalNaik.com site."""
from pathlib import Path
from datetime import datetime, timezone
import html
import json
import subprocess

from pages_structural import STRUCTURAL
import scorecard_page
from pages_copy import SERVICES, CONTACT_FAQS, make_bodies
from pages_chrome import NAV, bind_chrome


ROOT = Path(__file__).parent
SITE = "https://kunaalnaik.com"
EMAIL = "me@kunaalnaik.com"

# Leadsy / vtag visitor-identification pixel + EU consent gate.
#
# This MUST stay an external file reference, not an inline <script>. vercel.json
# sets Content-Security-Policy script-src 'self' with no 'unsafe-inline', so an
# inline gate is silently blocked and the tag never loads. That happened once
# already; test_entity_and_faq.py now asserts the external form.
#
# The gate itself lives in assets/site.js (region check, consent, injection).
VISITOR_TAG_SRC = "https://r2.leadsy.ai/tag.js"
VISITOR_TAG_PID = "pbfdcrcFAjyErfW8"
VISITOR_TAG_VERSION = "062024"
VISITOR_TAG = (f'<meta name="vtag-src" content="{VISITOR_TAG_SRC}">'
               f'<meta name="vtag-pid" content="{VISITOR_TAG_PID}">'
               f'<meta name="vtag-version" content="{VISITOR_TAG_VERSION}">')

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

# Person.founder is invalid schema.org. Reciprocal @id refs:
# Person.worksFor -> Organization, Organization.founder -> Person.
ORGANIZATION = {
    "@type": "Organization",
    "@id": "https://datasciencemasterminds.com/#organization",
    "name": "Data Science Masterminds",
    "url": "https://datasciencemasterminds.com/",
    "founder": {"@id": f"{SITE}/#kunaal-naik"},
    "logo": f"{SITE}/assets/favicon.svg",
}

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#kunaal-naik",
    "name": "Kunaal Naik",
    "url": f"{SITE}/",
    "image": f"{SITE}/assets/kunaal-naik.webp",
    "jobTitle": "Corporate AI Trainer and AI Workflow Consultant",
    "description": "Kunaal Naik helps professionals, business owners, and teams turn AI tools into practical, governed workflows.",
    "sameAs": SAME_AS,
    "worksFor": {"@id": ORGANIZATION["@id"]},
}

def esc(value):
    return html.escape(str(value), quote=True)


def lastmod_for(filename):
    """Real lastmod: git last-commit date (YYYY-MM-DD), else file mtime, else today."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", filename],
            cwd=ROOT, stderr=subprocess.DEVNULL, text=True,
        ).strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pass
    path = ROOT / filename
    if path.exists():
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat()
    return datetime.now(timezone.utc).date().isoformat()


def mailto(subject):
    return f"mailto:{EMAIL}?subject={esc(subject).replace(' ', '%20')}"


bind_chrome(
    esc=esc, mailto=mailto, EMAIL_VAL=EMAIL, SITE_VAL=SITE,
    PERSON_VAL=PERSON, ORGANIZATION_VAL=ORGANIZATION,
    VISITOR_TAG_VAL=VISITOR_TAG, SOCIALS_VAL=SOCIALS,
)
from pages_chrome import (
    header, footer, schemas, faq_section, page, page_hero, cta,
    scorecard_cta, sidebar, related_section, service_body,
)

_bodies = make_bodies(
    page_hero=page_hero,
    cta=cta,
    scorecard_cta=scorecard_cta,
    sidebar=sidebar,
    mailto=mailto,
    faq_section=faq_section,
    EMAIL=EMAIL,
    ENGAGEMENT_FLOOR=ENGAGEMENT_FLOOR,
    SOCIALS=SOCIALS,
)
home = _bodies["home"]
about = _bodies["about"]
speaking = _bodies["speaking"]
cases = _bodies["cases"]
gcc_case = _bodies["gcc_case"]
insights = _bodies["insights"]
contact = _bodies["contact"]
privacy = _bodies["privacy"]
terms = _bodies["terms"]
not_found = _bodies["not_found"]

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

# Lead tool. Content and scoring live in scorecard_content.py; the page passes
# build.py's own helpers in so scorecard_page.py stays import-cycle free.
PAGES[f"{scorecard_page.SLUG}/index.html"] = (
    scorecard_page.TITLE, scorecard_page.DESCRIPTION, f"/{scorecard_page.SLUG}/",
    scorecard_page.body(page_hero, faq_section, esc), "WebPage", scorecard_page.FAQS)

for filename, entry in PAGES.items():
    title, description, path, body, kind = entry[:5]
    faqs = entry[5] if len(entry) > 5 else None
    destination = ROOT / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page(title, description, path, body, kind, faqs), encoding="utf-8")

public_pages = sorted(
    (entry[2], filename) for filename, entry in PAGES.items() if filename != "404.html")
public_paths = [path for path, _ in public_pages]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, filename in public_pages:
    sitemap.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{lastmod_for(filename)}</lastmod></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

KEY_LLMS_URLS = [
    "/",
    "/about-kunaal-naik/",
    "/corporate-ai-training/",
    "/ai-automation-consulting/",
    "/claude-cowork-training/",
    "/hermes-agent-training/",
    "/ai-agents-for-professionals/",
    "/speaking-and-workshops/",
    "/ai-readiness-scorecard/",
    "/case-studies/",
    "/insights/",
    "/contact/",
]
llms = [
    "# Kunaal Naik",
    "",
    "> Corporate AI trainer and AI workflow consultant. Founder of Data Science Masterminds. TEDx speaker.",
    "",
    "Kunaal Naik helps professionals, business owners, and teams turn AI tools into practical, governed workflows.",
    "",
    "## Offers",
    "",
    f"- Corporate AI training: {SITE}/corporate-ai-training/",
    f"- AI workflow consulting: {SITE}/ai-automation-consulting/",
    f"- Claude Cowork enablement: {SITE}/claude-cowork-training/",
    f"- Hermes Agent setup: {SITE}/hermes-agent-training/",
    "",
    "## Key URLs",
    "",
]
for path in KEY_LLMS_URLS:
    llms.append(f"- {SITE}{path}")
llms += ["", "## All pages", ""]
for path in public_paths:
    llms.append(f"- {SITE}{path}")
llms += ["", "## Contact", "", EMAIL, ""]
(ROOT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

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
print(f"Built {len(PAGES)} HTML pages, {len(public_paths)} sitemap URLs, and llms.txt")
