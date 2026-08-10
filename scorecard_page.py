#!/usr/bin/env python3
"""The /ai-readiness-scorecard/ page: quiz UI, client scoring, gated report.

Rendered by build.py. All content and scoring rules come from
scorecard_content.py, serialised to JSON and embedded once, so the browser
scorer cannot drift from the Python source of truth.

ponytail: scoring runs client-side so the score appears instantly with no
round-trip, which is the whole point of showing value before the gate. A
visitor can therefore read or forge their own score. Accepted: the score is
advisory, not a credential. api/submit-scorecard.js recomputes lead_score
server-side, and that is the figure Kunaal acts on.
"""
import json

import scorecard_content as sc

SLUG = "ai-readiness-scorecard"
TITLE = "AI Readiness Scorecard | Kunaal Naik"
DESCRIPTION = ("A 10-question AI readiness scorecard for corporate teams. See your score "
               "and your three highest-value gaps across strategy, capability, governance "
               "and measurement. No email needed for the score.")

FAQS = [
    ("Do I have to give my email to see my score?",
     "No. The score, the four sub-scores, and your band appear on screen as soon as you finish the questions. Contact details are only needed for the full written report, because that report is a personalised analysis of your answers."),
    ("How long does it take?",
     "About three minutes. Ten questions, one screen each, no research required. Answer from what you already know about your organisation."),
    ("Is this a sales funnel?",
     "There is no newsletter, no automated call sequence, and no drip campaign. If your answers suggest Kunaal can help, you get one direct reply from him. If they do not, you still keep the report."),
    ("What happens to my answers?",
     "They are stored so the report can be produced and so Kunaal can follow up usefully. Answers are also used in anonymised, aggregate form to understand where organisations are actually stuck. Nothing is sold on. See the privacy page."),
    ("What if we score badly?",
     "A low score is a diagnosis, not a judgement. Most organisations that need this work score in the middle: enough activity to see the value, not yet enough structure to trust it. The gaps are the useful part."),
]

PAYLOAD = {
    "questions": [
        {"id": q["id"], "dimension": q["dimension"], "text": q["text"],
         "options": [{"label": label, "points": points} for label, points in q["options"]]}
        for q in sc.QUESTIONS
    ],
    "dimensions": sc.DIMENSIONS,
    "bands": [{"min": lo, "max": hi, "label": label, "verdict": verdict}
              for lo, hi, label, verdict in sc.BANDS],
    "gaps": {qid: {str(idx): text for idx, text in opts.items()}
             for qid, opts in sc.GAPS.items()},
    # Gap tiebreak order. Serialised rather than hardcoded in JS so the browser
    # scorer cannot disagree with scorecard_content.score().
    "priority": sc._DIMENSION_PRIORITY,
}

TEAM_SIZES = ["1-9", "10-49", "50-249", "250-999", "1000+"]
BUDGET_BANDS = ["Not yet budgeted", "Under 5 lakh", "5-15 lakh", "15-50 lakh", "Over 50 lakh"]
TIMELINES = ["This quarter", "Next quarter", "Within 6 months", "Exploring only"]


def _options(values):
    return "".join(f'<option value="{v}">{v}</option>' for v in values)


def body(page_hero, faq_section, esc):
    """Built by build.py, which passes in its own helpers to avoid a circular import."""
    data = json.dumps(PAYLOAD, ensure_ascii=False, separators=(",", ":"))
    dim_rows = "".join(
        f'<div class="sc-dim"><span>{esc(name)}</span>'
        f'<div class="sc-bar"><i data-dim-bar="{esc(name)}" style="width:0%"></i></div>'
        f'<b data-dim-val="{esc(name)}">0</b></div>'
        for name in sc.DIMENSIONS)

    return f'''{page_hero('AI readiness scorecard', 'Find out what is actually <em>missing.</em>',
    'Ten questions, about three minutes. You get your score, four sub-scores, and your three highest-value gaps. The score is free and needs no email.', 'AI readiness scorecard')}
<section class="section"><div class="section-inner sc">

<noscript><div class="sc-msg">This scorecard scores your answers in the browser, so it needs JavaScript enabled. If you would rather not enable it, email <a href="mailto:me@kunaalnaik.com">me@kunaalnaik.com</a> with your situation and you will get the same diagnosis by reply.</div></noscript>

<div id="sc-app" hidden>
  <div class="sc-progress"><i id="sc-bar" style="width:0%"></i></div>
  <div id="sc-questions"></div>

  <div class="sc-step" id="sc-result">
    <p class="sc-meta">Your result</p>
    <div class="sc-score"><b id="sc-total">0</b><span>out of 100</span></div>
    <div class="sc-band" id="sc-band-label"></div>
    <p class="lede" id="sc-verdict"></p>

    <div class="sc-dims">{dim_rows}</div>

    <div class="sc-gate">
      <h3>Your three highest-value gaps</h3>
      <p class="note">The score above is yours to keep. The written breakdown below is produced from your specific answers, which is why it needs an address to send to.</p>
      <form id="sc-form" novalidate>
        <div class="sc-fields">
          <div><label for="sc-name">Name</label><input id="sc-name" name="name" autocomplete="name" required></div>
          <div><label for="sc-email">Work email</label><input id="sc-email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="sc-org">Organisation</label><input id="sc-org" name="organisation" autocomplete="organization" required></div>
          <div><label for="sc-role">Your role</label><input id="sc-role" name="role" autocomplete="organization-title"></div>
          <div><label for="sc-team">Team size</label><select id="sc-team" name="team_size"><option value="">Select</option>{_options(TEAM_SIZES)}</select></div>
          <div><label for="sc-phone">Phone <span class="sc-opt-tag">optional</span></label><input id="sc-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div><label for="sc-budget">Budget band <span class="sc-opt-tag">optional</span></label><select id="sc-budget" name="budget_band"><option value="">Prefer not to say</option>{_options(BUDGET_BANDS)}</select></div>
          <div><label for="sc-timeline">Timeline <span class="sc-opt-tag">optional</span></label><select id="sc-timeline" name="timeline"><option value="">Prefer not to say</option>{_options(TIMELINES)}</select></div>
          <label class="sc-consent" id="sc-consent-row" hidden><input type="checkbox" id="sc-consent" name="consent"><span>Send me my report and store my answers so Kunaal can follow up. Answers may be used in anonymised aggregate research. No newsletter, no automated calls.</span></label>
          <div class="full"><button class="button button-primary" type="submit" id="sc-submit">Send my report</button></div>
        </div>
      </form>
      <p class="note" style="margin:16px 0 0">Phone is optional and only used if you want a call. No automated calls, ever. One direct reply from Kunaal.</p>
      <div id="sc-msg"></div>
    </div>

    <div id="sc-gaps-out" hidden>
      <h2 style="font:700 34px/1.1 var(--display);margin:44px 0 0">What to fix first</h2>
      <ul class="sc-gaps" id="sc-gaps"></ul>
      <a class="button button-primary" href="mailto:me@kunaalnaik.com?subject=AI%20readiness%20scorecard%20follow-up">Discuss these gaps with Kunaal</a>
    </div>
  </div>
</div>
</div></section>
{faq_section(FAQS)}
<script id="sc-data" type="application/json">{data}</script>
<script src="/assets/scorecard.js" defer></script>'''
