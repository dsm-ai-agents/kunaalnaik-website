#!/usr/bin/env python3
"""Guards the grouped nav: every structural page is reachable from the menu,
no dead links, no duplicates, and the mobile/no-JS path still works.

Run: python3 test_nav.py   (after python3 build.py)
"""
import re
from pathlib import Path

from build import NAV
from pages_structural import STRUCTURAL

ROOT = Path(__file__).parent


def nav_urls():
    urls = []
    for entry in NAV:
        if entry[1] is not None:
            urls.append(entry[1])
        else:
            urls.extend(url for _, url, _ in entry[2])
    return urls


def main():
    urls = nav_urls()

    # no duplicate destinations — a link in two menus is a navigation smell
    dupes = {u for u in urls if urls.count(u) > 1}
    assert not dupes, f"duplicate nav destinations: {dupes}"

    # every nav target must be a real built page
    for u in urls:
        target = ROOT / u.strip("/") / "index.html"
        assert target.exists(), f"nav links to missing page: {u}"

    # THE POINT: all 23 structural pages must be reachable from the nav
    missing = sorted(f"/{s}/" for s in STRUCTURAL if f"/{s}/" not in urls)
    assert not missing, f"structural pages not in nav: {missing}"

    home = (ROOT / "index.html").read_text(encoding="utf-8")

    # nav must render as <details> so it works with JS disabled
    assert home.count('<details class="menu">') == sum(1 for e in NAV if e[1] is None), \
        "dropdown count mismatch"
    assert "<summary>" in home, "no summary elements: nav would be unusable without JS"

    # blurbs must be present (they are the reason a 10-item menu is scannable)
    panels = re.findall(r'<div class="menu-panel[^"]*">(.*?)</div>', home, re.S)
    assert panels, "no menu panels rendered"
    for p in panels:
        assert p.count("<strong>") == p.count("<span>"), "menu item missing its blurb"

    # wide panels only where there are enough items to need two columns
    for entry in NAV:
        if entry[1] is None and len(entry[2]) > 5:
            assert "menu-wide" in home, f"{entry[0]}: >5 items but no wide panel class"

    # CSS cascade: the mobile media query must come AFTER the desktop nav rules,
    # or desktop dropdown positioning overrides the mobile accordion at all widths.
    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    mq = css.index("@media(max-width:900px)")
    for key in (".menu{position:relative}", "nth-last-of-type", ".menu-panel{position:absolute"):
        assert css.index(key) < mq, f"{key!r} declared after the mobile media query"
    for key in (".menu{position:static}", "grid-template-columns:1fr"):
        assert css.index(key, mq) > mq, f"mobile override {key!r} missing from media query"

    groups = sum(1 for e in NAV if e[1] is None)
    print(f"PASS: {groups} nav groups, {len(urls)} destinations, all 23 structural "
          "pages reachable, no dupes, no dead links, works without JS, "
          "mobile CSS wins over desktop")


if __name__ == "__main__":
    main()
