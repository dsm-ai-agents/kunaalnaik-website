#!/usr/bin/env python3
"""Guards the scorecard: the embedded JSON matches scorecard_content.py, and the
browser scorer agrees with the Python scorer on every answer combination tested.

Drift between the two scorers would silently show visitors a different score
than the one stored against their lead, so this is the check that matters.

Run: python3 test_scorecard.py   (after python3 build.py; needs node)
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

import scorecard_content as sc

ROOT = Path(__file__).parent
PAGE = ROOT / "ai-readiness-scorecard/index.html"

# Runs the REAL assets/scorecard.js in a minimal DOM shim, so this test
# exercises the file the browser loads rather than a copy of its logic.
JS_HARNESS = """
const fs = require('fs');
const D = %(data)s;
const cases = %(cases)s;
const src = fs.readFileSync(%(script)s, 'utf8');

// Extract the score() function from the real file and evaluate it against D.
const m = src.match(/function score\\(\\)\\s*\\{[\\s\\S]*?\\n  \\}/);
if (!m) { console.error('could not find score() in scorecard.js'); process.exit(2); }

const results = cases.map(function (answers) {
  const fn = new Function('D', 'Q', 'answers', m[0] + '; return score();');
  const r = fn(D, D.questions, answers);
  return { total: r.total, dims: r.dims, band: r.band.label, gaps: r.gaps };
});
console.log(JSON.stringify(results));
"""


def embedded_payload():
    html = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<script id="sc-data" type="application/json">(.*?)</script>', html, re.S)
    assert m, "embedded scorecard JSON not found in built page"
    return json.loads(m.group(1))


def main():
    assert PAGE.exists(), "run python3 build.py first"
    data = embedded_payload()

    # 1. embedded content must equal the Python source
    assert len(data["questions"]) == len(sc.QUESTIONS) == 10, "question count mismatch"
    for src, emb in zip(sc.QUESTIONS, data["questions"]):
        assert src["id"] == emb["id"], f"id drift: {src['id']} vs {emb['id']}"
        assert src["text"] == emb["text"], f"text drift on {src['id']}"
        assert [p for _, p in src["options"]] == [o["points"] for o in emb["options"]], \
            f"points drift on {src['id']}"
    assert data["dimensions"] == sc.DIMENSIONS, "dimension text drift"
    assert len(data["bands"]) == len(sc.BANDS), "band count drift"

    # 2. build the case list: edges, all-same, and random spreads
    cases = [
        {q["id"]: len(q["options"]) - 1 for q in sc.QUESTIONS},   # all best
        {q["id"]: 0 for q in sc.QUESTIONS},                       # all worst
        {q["id"]: 1 for q in sc.QUESTIONS},
        {q["id"]: 2 for q in sc.QUESTIONS},
        {},                                                        # nothing answered
    ]
    rng = random.Random(7)
    for _ in range(40):
        cases.append({q["id"]: rng.randrange(len(q["options"])) for q in sc.QUESTIONS})

    # 3. run the JS scorer straight out of assets/scorecard.js
    src = JS_HARNESS % {"data": json.dumps(data), "cases": json.dumps(cases),
                        "script": json.dumps(str(ROOT / "assets/scorecard.js"))}
    proc = subprocess.run([_node(), "-e", src], capture_output=True, text=True)
    assert proc.returncode == 0, f"node failed: {proc.stderr[:400]}"
    js_results = json.loads(proc.stdout)

    # 4. compare against Python for every case
    for case, js in zip(cases, js_results):
        py = sc.score(case)
        assert py["total"] == js["total"], \
            f"TOTAL drift: py={py['total']} js={js['total']} for {case}"
        assert py["band"][2] == js["band"], \
            f"BAND drift: py={py['band'][2]} js={js['band']} at total {py['total']}"
        assert py["dimensions"] == js["dims"], \
            f"DIMENSION drift: py={py['dimensions']} js={js['dims']}"
        assert py["gaps"] == js["gaps"], f"GAP drift at total {py['total']}"

    # 5. the promise the page makes: score is free, only the report is gated
    html = PAGE.read_text(encoding="utf-8")
    assert "sc-total" in html and "sc-band-label" in html, "score display missing"
    assert 'id="sc-form"' in html, "gated form missing"
    assert "optional" in html.lower(), "phone/budget must be marked optional"
    assert "No automated calls" in html, "the no-cold-call promise must be on the page"
    assert "<noscript>" in html, "no-JS visitors need a fallback path"
    # phone must not be a required field
    m = re.search(r'id="sc-phone"[^>]*>', html)
    assert m and "required" not in m.group(0), "phone must never be required"

    # 6. VISIBILITY: a lead tool nobody can find is worthless. It must be
    #    promoted in visible body content, not only buried in a nav dropdown.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "sc-promo" in home, "homepage has no visible scorecard prompt"
    assert "/ai-readiness-scorecard/" in home, "homepage missing scorecard link"
    assert "scorecard" in home.lower(), "homepage never mentions the scorecard"

    contact = (ROOT / "contact/index.html").read_text(encoding="utf-8")
    assert "sc-promo" in contact, "contact page has no scorecard prompt"

    # every service page sidebar must offer it
    service_pages = [p for p in ROOT.glob("*/index.html")
                     if 'class="sidebar"' in p.read_text(encoding="utf-8")]
    assert len(service_pages) >= 20, f"expected 20+ sidebar pages, found {len(service_pages)}"
    for p in service_pages:
        h = p.read_text(encoding="utf-8")
        assert "sc-side" in h, f"{p.parent.name}: sidebar missing scorecard panel"

    # the scorecard page must not promote itself
    assert "sc-promo" not in html, "scorecard page should not link to itself"

    print(f"PASS: embedded content matches source, JS and Python scorers agree on "
          f"{len(cases)} answer sets, score ungated, phone optional, promoted on home "
          f"+ contact + {len(service_pages)} sidebars")


def _node():
    for c in ("node", "nodejs"):
        if subprocess.run(["which", c], capture_output=True).returncode == 0:
            return c
    print("SKIP: node not available, cannot cross-check the browser scorer")
    sys.exit(0)


if __name__ == "__main__":
    main()
