#!/usr/bin/env python3
"""Guards the two SEO changes that are easy to silently break:
entity sameAs links, and FAQPage schema staying in sync with visible FAQ text.

Run: python3 test_entity_and_faq.py   (after python3 build.py)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent


def graph(html):
    raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
    return json.loads(raw)["@graph"]


def node(g, t):
    return next((n for n in g if n.get("@type") == t), None)


def main():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    contact = (ROOT / "contact/index.html").read_text(encoding="utf-8")

    # --- entity: sameAs must be present and plural on every page ---
    person = node(graph(home), "Person")
    assert person, "Person schema missing from homepage"
    same_as = person.get("sameAs", [])
    assert len(same_as) >= 4, f"sameAs too thin ({len(same_as)}); entity signal is the point"
    assert all(u.startswith("https://") for u in same_as), f"non-https sameAs: {same_as}"
    assert len(same_as) == len(set(same_as)), f"duplicate sameAs entries: {same_as}"

    # --- FAQ: schema must exist AND match the visible copy (no cloaking) ---
    g = graph(contact)
    faq = node(g, "FAQPage")
    assert faq, "FAQPage schema missing from /contact/"
    questions = [q["name"] for q in faq["mainEntity"]]
    assert len(questions) >= 3, f"only {len(questions)} FAQ entries"

    for q in questions:
        # visible <summary> text is html-escaped; compare on a normalised form
        needle = q.replace("&", "&amp;").replace("<", "&lt;")
        assert needle in contact, f"FAQ in schema but not visible on page: {q!r}"

    for a in (x["acceptedAnswer"]["text"] for x in faq["mainEntity"]):
        assert a.strip(), "empty FAQ answer"

    # --- low-ticket filter must actually be on the page ---
    assert "minimum engagement" in contact.lower(), "engagement floor missing from /contact/"
    assert "Not a fit" in contact, "'Not a fit' exclusion list missing from /contact/"

    # --- visitor tag: present on every page, and disclosed on /privacy/ ---
    tag = 'id="vtag-ai-js"'
    pages = list(ROOT.glob("*.html")) + list(ROOT.glob("*/index.html")) + list(ROOT.glob("*/*/index.html"))
    missing = [str(p.relative_to(ROOT)) for p in pages if tag not in p.read_text(encoding="utf-8")]
    assert not missing, f"visitor tag missing from: {missing}"

    privacy = (ROOT / "privacy/index.html").read_text(encoding="utf-8")
    assert "leadsy" in privacy.lower(), "visitor tag runs but /privacy/ does not disclose it"
    assert "Visitor identification" in privacy, "/privacy/ missing visitor-identification section"
    assert "advertising pixel, or newsletter" not in privacy, "/privacy/ still claims no pixel"

    print(f"PASS: {len(same_as)} sameAs links, {len(questions)} FAQs in schema + visible, "
          f"engagement floor present, visitor tag on {len(pages)} pages + disclosed")


if __name__ == "__main__":
    main()
