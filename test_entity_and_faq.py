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

    # --- visitor tag: config on every page, gate in an EXTERNAL file ---
    # An inline gate is silently blocked by the CSP in vercel.json
    # (script-src 'self', no 'unsafe-inline'), so the tag would never load.
    pages = list(ROOT.glob("*.html")) + list(ROOT.glob("*/index.html")) + list(ROOT.glob("*/*/index.html"))
    for needle in ('name="vtag-src"', 'name="vtag-pid"'):
        missing = [str(p.relative_to(ROOT)) for p in pages
                   if needle not in p.read_text(encoding="utf-8")]
        assert not missing, f"{needle!r} missing from: {missing}"

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "r2.leadsy.ai/tag.js" in home, "tag source missing from page config"
    # the gate must NOT be inline
    assert "localStorage.getItem" not in home, \
        "consent gate is inline; CSP script-src 'self' will block it silently"
    assert '<script id="vtag-ai-js" async src=' not in home, "unconditional tag bypasses consent gate"

    site_js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    for needle in ("vtag-consent", "Europe", "vtag-ai-js", "localStorage"):
        assert needle in site_js, f"gate logic missing {needle!r} from assets/site.js"

    # CSP must permit the external tag domain, or the gate loads a blocked script
    csp = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    header = next(h["value"] for block in csp["headers"] for h in block["headers"]
                  if h["key"] == "Content-Security-Policy")
    assert "r2.leadsy.ai" in header, "CSP does not allow the visitor-tag domain"
    assert "'unsafe-inline'" not in header, "CSP weakened to unsafe-inline; fix the script instead"

    privacy = (ROOT / "privacy/index.html").read_text(encoding="utf-8")
    assert "leadsy" in privacy.lower(), "visitor tag runs but /privacy/ does not disclose it"
    assert "Visitor identification" in privacy, "/privacy/ missing visitor-identification section"
    assert "advertising pixel, or newsletter" not in privacy, "/privacy/ still claims no pixel"
    assert "consent" in privacy.lower(), "/privacy/ does not mention the consent gate"

    print(f"PASS: {len(same_as)} sameAs links, {len(questions)} FAQs in schema + visible, "
          f"engagement floor present, external CSP-safe visitor tag on {len(pages)} pages + disclosed")


if __name__ == "__main__":
    main()
