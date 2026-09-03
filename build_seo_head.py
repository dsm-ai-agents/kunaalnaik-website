#!/usr/bin/env python3
"""Build the dependency-free static KunaalNaik.com site."""
from pathlib import Path
from datetime import datetime, timezone
import html
import json
import subprocess

from pages_structural import STRUCTURAL
import scorecard_page

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
