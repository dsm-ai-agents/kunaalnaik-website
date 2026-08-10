#!/usr/bin/env python3
"""Guards the 23 structural pages: they exist, carry Service + FAQPage schema,
are internally linked (not orphans), and are free of placeholder pricing.

Run: python3 test_structural_pages.py   (after python3 build.py)
"""
import json
import re
from pathlib import Path

from pages_structural import STRUCTURAL

ROOT = Path(__file__).parent


def graph(html):
    raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
    return json.loads(raw)["@graph"]


def main():
    assert len(STRUCTURAL) == 23, f"expected 23 structural pages, got {len(STRUCTURAL)}"

    slugs = set(STRUCTURAL)
    all_html = {}

    for slug, item in STRUCTURAL.items():
        f = ROOT / slug / "index.html"
        assert f.exists(), f"{slug}: not built"
        h = f.read_text(encoding="utf-8")
        all_html[slug] = h

        # one h1, correct canonical, Service schema
        assert h.count("<h1>") == 1, f"{slug}: {h.count('<h1>')} h1 tags"
        assert f'href="https://kunaalnaik.com/{slug}/"' in h, f"{slug}: canonical wrong"
        types = [n.get("@type") for n in graph(h)]
        assert "Service" in types, f"{slug}: missing Service schema"

        # FAQs, where declared, must be in schema AND visible
        if item.get("faqs"):
            assert "FAQPage" in types, f"{slug}: has faqs but no FAQPage schema"
            for q, _ in item["faqs"]:
                needle = q.replace("&", "&amp;").replace("<", "&lt;")
                assert needle in h, f"{slug}: FAQ not visible: {q!r}"

        # every related link must point at a real page
        for label, url in item.get("related", []):
            target = url.strip("/")
            built = (ROOT / target / "index.html").exists()
            assert built, f"{slug}: related link -> {url} does not exist"

        # no unresolved pricing placeholder shipped to production
        for bad in ("TODO", "XXX", "₹X", "TBD", "Lorem"):
            assert bad not in h, f"{slug}: placeholder {bad!r} left in page"

    # no structural page may be an orphan: something must link to it
    corpus = "".join(all_html.values())
    footer_and_body = corpus + (ROOT / "index.html").read_text(encoding="utf-8")
    orphans = [s for s in slugs if f'href="/{s}/"' not in footer_and_body]
    assert not orphans, f"orphan pages (nothing links to them): {orphans}"

    faq_count = sum(len(i.get("faqs", [])) for i in STRUCTURAL.values())
    print(f"PASS: 23 structural pages built, Service schema on all, {faq_count} FAQs "
          "in schema + visible, all related links resolve, no orphans, no placeholders")


if __name__ == "__main__":
    main()
