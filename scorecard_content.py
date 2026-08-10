#!/usr/bin/env python3
"""Content and scoring for the AI Readiness Scorecard lead tool.

Data and pure functions only. build.py renders it; nothing here knows about
HTML, requests, or files.

Ten questions, four sub-scores, five bands, and one gap statement per
low-scoring option. The gap statements are the thing the visitor actually
receives, so they name a specific missing artifact or decision rather than
describing a maturity level back at them.

Scoring: every question is worth 0 to 10 points, so ten questions give a raw
maximum of 100. Options are spaced 0 / 4 / 7 / 10 so that a partly-built
capability lands in the 40 to 70 middle rather than at either end.

Run: python3 scorecard_content.py   (assert-based self-check)
"""

DIMENSIONS = {
    "Strategy": "Whether AI work is tied to named business outcomes, owned by a "
                "specific person, and funded from a real budget line.",
    "Capability": "Whether the people doing the work have been trained on their own "
                  "tasks and can produce usable output without help.",
    "Governance": "Whether there are written rules, approval gates, and audit trails "
                  "covering what AI may and may not be used for.",
    "Measurement": "Whether AI use, quality, and business effect are being tracked "
                   "against a baseline rather than described anecdotally.",
}

# ponytail: points spaced 0/4/7/10 on purpose. Binary yes/no options would push
# everyone to 0 or 100 and destroy the middle band this tool is built to find.
QUESTIONS = [
    {
        "id": "q1_mandate",
        "dimension": "Strategy",
        "text": "Who owns AI adoption in your organisation today?",
        "options": [
            ("Nobody in particular, it is happening informally", 0),
            ("A committee or working group with no single accountable owner", 4),
            ("A named leader, alongside their existing full-time role", 7),
            ("A named leader with a defined remit and dedicated time", 10),
        ],
    },
    {
        "id": "q2_budget",
        "dimension": "Strategy",
        "text": "How is AI training and enablement funded this year?",
        "options": [
            ("No budget identified yet", 0),
            ("Absorbed into existing L&D or department spend as needed", 4),
            ("A specific allocation approved for this financial year", 7),
            ("A multi-year allocation with committed spend by function", 10),
        ],
    },
    {
        "id": "q3_use_cases",
        "dimension": "Strategy",
        "text": "How clearly are your priority AI use cases defined?",
        "options": [
            ("We are still exploring what is possible", 0),
            ("Broad themes such as productivity or automation, nothing specific", 4),
            ("A shortlist of named workflows in two or three functions", 7),
            ("Prioritised workflows with named owners and expected outcomes", 10),
        ],
    },
    {
        "id": "q4_training",
        "dimension": "Capability",
        "text": "What AI training have your teams actually completed?",
        "options": [
            ("None, or self-directed learning only", 0),
            ("An awareness session or vendor demonstration", 4),
            ("Hands-on training for one or two functions on their own tasks", 7),
            ("Role-based training across priority functions, with practice on live work", 10),
        ],
    },
    {
        "id": "q5_daily_use",
        "dimension": "Capability",
        "text": "How much of your workforce uses AI in their normal work each week?",
        "options": [
            ("Hard to say, we do not have visibility", 0),
            ("A small group of enthusiasts", 4),
            ("Whole teams in one or two functions", 7),
            ("Most people in the functions we prioritised", 10),
        ],
    },
    {
        "id": "q7_policy",
        "dimension": "Governance",
        "text": "Do you have a written AI use policy that staff have seen?",
        "options": [
            ("No written policy yet", 0),
            ("Verbal guidance or an internal email", 4),
            ("A written policy circulated, though not everyone has read it", 7),
            ("A written policy with acknowledgement, owners, and periodic review", 10),
        ],
    },
    {
        "id": "q8_approval",
        "dimension": "Governance",
        "text": "Before AI-assisted work reaches a client, a regulator, or the board, what happens?",
        "options": [
            ("It depends on the individual", 0),
            ("Informal review by a manager who may not know AI was used", 4),
            ("A defined human review step for most external output", 7),
            ("A named approver, a verification standard, and a record of the check", 10),
        ],
    },
    {
        "id": "q9_data",
        "dimension": "Governance",
        "text": "How confident are you about what data your teams put into AI tools?",
        "options": [
            ("Not confident, we have limited visibility", 0),
            ("We assume people are sensible, nothing is checked", 4),
            ("Approved tools are listed and sensitive categories are named", 7),
            ("Approved tools, data classification rules, and periodic checks", 10),
        ],
    },
    {
        "id": "q10_measure",
        "dimension": "Measurement",
        "text": "How do you currently judge whether AI use is working?",
        "options": [
            ("We have not measured it", 0),
            ("Anecdotes and positive feedback from teams", 4),
            ("Usage or licence data, plus qualitative feedback", 7),
            ("Agreed measures per workflow, compared with a documented baseline", 10),
        ],
    },
    {
        "id": "q11_baseline",
        "dimension": "Measurement",
        "text": "For your priority workflows, do you know the current cost in hours or cycle time?",
        "options": [
            ("No, we would have to estimate", 0),
            ("Rough estimates held by the team leads", 4),
            ("Measured for some workflows", 7),
            ("Measured and recorded before any AI change was introduced", 10),
        ],
    },
]

BANDS = [
    (0, 24, "Early / Exploring",
     "AI use in your organisation is currently individual rather than organisational. "
     "That is a common starting point and it is cheaper to build the structure now than "
     "to retrofit it later. The first useful step is naming an owner and choosing two "
     "workflows to work on, not buying tools."),
    (25, 44, "Activity Without Structure",
     "People are using AI, but the organisation cannot yet see, govern, or repeat what "
     "they do. The risk here is quiet inconsistency in work that leaves the building. "
     "Priority is a written policy, a review step, and hands-on training on real tasks "
     "rather than general awareness."),
    (45, 64, "Pockets of Progress",
     "Some functions are genuinely capable while others have barely started, so results "
     "depend on who is doing the work. This is the point where governance and measurement "
     "usually lag capability. Standardise what already works, document it, and extend it "
     "function by function."),
    (65, 84, "Scaling With Gaps",
     "You have real capability, a mandate, and some controls in place. What typically "
     "remains is proof: a baseline you measured before the change, and an audit trail a "
     "reviewer or regulator would accept. Closing those two gaps is what turns adoption "
     "into a defensible programme."),
    (85, 100, "Governed and Measured",
     "AI work is owned, trained, governed, and measured against a baseline. The remaining "
     "work is depth in specific functions and keeping the controls current as tools change. "
     "Focus on the functions with the highest consequence of error rather than broader rollout."),
]

GAPS = {
    "q1_mandate": {
        0: "No single person is accountable for AI adoption, so decisions on tools, "
           "policy, and training stall between functions. Name one owner with authority "
           "to approve tools and sign off the policy.",
        1: "A committee can advise but cannot be held to a deadline. Appoint one "
           "accountable owner from within the group and give them a written remit.",
        2: "Your AI owner is carrying this on top of a full-time role, which usually "
           "means policy and training slip behind operational work. Protect specific "
           "time for it, or narrow the remit to two functions.",
    },
    "q2_budget": {
        0: "With no identified budget, AI work depends on goodwill and cannot be "
           "scheduled. Size a first-year figure for training and enablement in your "
           "priority functions so it can enter the normal approval cycle.",
        1: "Funding AI enablement from spare departmental budget makes it the first "
           "thing cut. A named allocation, even a modest one, is what lets you plan "
           "sequenced training rather than one-off sessions.",
    },
    "q3_use_cases": {
        0: "Without named use cases, training tends to be generic and adoption fades "
           "once the session ends. Pick two workflows your teams repeat weekly, for "
           "example monthly reporting commentary or candidate screening, and start there.",
        1: "Themes such as productivity cannot be trained against or measured. Convert "
           "each theme into a specific workflow with a named owner and a defined output.",
        2: "You have a shortlist but not an order of work. Rank the shortlist by volume, "
           "consequence of error, and readiness of the team, then fund the top two.",
    },
    "q4_training": {
        0: "Self-directed learning produces very uneven quality, and the gap is usually "
           "invisible until output leaves the building. Start with role-based training on "
           "your own live tasks rather than general tool overviews.",
        1: "Awareness sessions and vendor demonstrations show what is possible but leave "
           "no working method behind. Demonstration is not deployment. The next step is "
           "hands-on work on your own tasks, with a review standard.",
        2: "Two trained functions is real progress, and it also creates a widening gap "
           "with the rest of the organisation. Document what the trained teams now do, "
           "then use it as the template for the next function.",
    },
    "q5_daily_use": {
        0: "Without visibility into who is using AI, you can neither support the users "
           "nor govern the risk. Licence and access data for approved tools gives you a "
           "usable starting picture within a week.",
        1: "Adoption resting on a few enthusiasts does not survive their workload or "
           "departure. Capture what they actually do into a written workflow the rest of "
           "the team can follow.",
        2: "Adoption is concentrated in one or two functions. Identify which remaining "
           "function has the highest repeat volume and extend to it next, rather than "
           "running a broad organisation-wide rollout.",
    },
    "q7_policy": {
        0: "With no written AI policy, every decision about acceptable use is made "
           "individually and cannot be evidenced later. A short policy covering approved "
           "tools, prohibited data, and required human review is enough to start.",
        1: "Verbal guidance cannot be pointed to during an audit or a client question. "
           "Put the same guidance in writing, name its owner, and give it a review date.",
        2: "A circulated policy that people have not read functions as no policy in "
           "practice. Add acknowledgement at team level and a short briefing so managers "
           "can answer questions about it.",
    },
    "q8_approval": {
        0: "External output is reaching clients and regulators without a defined check, "
           "so accuracy depends on who happened to do the work. Define one human review "
           "step for anything that leaves the organisation.",
        1: "A reviewer who does not know AI was involved cannot verify the right things. "
           "Require that AI assistance is disclosed internally, and give reviewers a short "
           "verification checklist for figures, sources, and claims.",
        2: "You have a review step but not a record of it. Name the approver per workflow "
           "and keep a simple log of what was checked, so the control can be demonstrated "
           "rather than asserted.",
    },
    "q9_data": {
        0: "Limited visibility over what data goes into AI tools is the single fastest "
           "route to an incident you find out about from someone outside the organisation. "
           "List approved tools and name the data categories that must never be pasted in.",
        1: "Relying on individual judgement about sensitive data leaves no defensible "
           "position afterwards. Classify your data into what may, may not, and may only "
           "be used in approved tools, and train to that list.",
        2: "Rules exist but nothing verifies them. Add a periodic check, even a quarterly "
           "sample review, so the control is evidenced rather than assumed.",
    },
    "q10_measure": {
        0: "Unmeasured AI use cannot be defended in a budget conversation or extended with "
           "confidence. Agree two measures per priority workflow, for example hours per "
           "cycle and rework rate, before the next phase of spend.",
        1: "Positive feedback tells you people like the tools, not that the work improved. "
           "Pair it with one quantitative measure per workflow so the case survives scrutiny.",
        2: "Usage data shows activity, not effect. Add an outcome measure per workflow, "
           "such as cycle time or error rate, so you can separate use from value.",
    },
    "q11_baseline": {
        0: "Without a baseline, any improvement claim after AI adoption is an estimate "
           "arguing with an estimate. Measure hours or cycle time on your top two workflows "
           "now, before further rollout.",
        1: "Rough estimates held by team leads move whenever the conversation needs them "
           "to. Record the current figure for two workflows in writing so the comparison "
           "later is credible.",
        2: "Some workflows are measured and the priority ones may not be. Confirm a "
           "written baseline exists for each workflow you intend to change this year.",
    },
}

# Gaps are ordered for the report: governance and measurement failures carry the
# most consequence, so they surface first when several gaps tie on points lost.
_DIMENSION_PRIORITY = {"Governance": 0, "Measurement": 1, "Strategy": 2, "Capability": 3}

_BY_ID = {q["id"]: q for q in QUESTIONS}


def _points(question, index):
    """Points for a chosen option index, defaulting to the lowest-scoring option."""
    options = question["options"]
    if isinstance(index, bool) or not isinstance(index, int):
        return min(p for _, p in options), None
    if not 0 <= index < len(options):
        return min(p for _, p in options), None
    return options[index][1], index


def score(answers):
    """Score a set of answers. Unknown, missing, or invalid answers score lowest."""
    if not isinstance(answers, dict):
        answers = {}

    earned = 0
    possible = 0
    dim_earned = {d: 0 for d in DIMENSIONS}
    dim_possible = {d: 0 for d in DIMENSIONS}
    found = []

    for question in QUESTIONS:
        options = question["options"]
        best = max(p for _, p in options)
        worst = min(p for _, p in options)
        points, index = _points(question, answers.get(question["id"]))

        earned += points - worst
        possible += best - worst
        dim = question["dimension"]
        dim_earned[dim] += points - worst
        dim_possible[dim] += best - worst

        gap = GAPS.get(question["id"], {}).get(index if index is not None else 0)
        if gap is None and index is None:
            gap = GAPS.get(question["id"], {}).get(0)
        if gap:
            found.append((best - points, _DIMENSION_PRIORITY[dim], gap))

    total = round(100 * earned / possible) if possible else 0
    dims = {
        d: (round(100 * dim_earned[d] / dim_possible[d]) if dim_possible[d] else 0)
        for d in DIMENSIONS
    }

    found.sort(key=lambda item: (-item[0], item[1]))
    return {
        "total": total,
        "dimensions": dims,
        "band": band_for(total),
        "gaps": [gap for _, _, gap in found[:3]],
    }


def band_for(total):
    """The BANDS entry containing this total."""
    for band in BANDS:
        if band[0] <= total <= band[1]:
            return band
    return BANDS[-1] if total > BANDS[-1][1] else BANDS[0]


def demo():
    assert len(QUESTIONS) == 10, len(QUESTIONS)

    ids = [q["id"] for q in QUESTIONS]
    assert len(set(ids)) == 10, "duplicate question ids"

    counts = {}
    for q in QUESTIONS:
        assert q["dimension"] in DIMENSIONS, q["dimension"]
        assert 3 <= len(q["options"]) <= 4, q["id"]
        assert all(0 <= p <= 10 for _, p in q["options"]), q["id"]
        counts[q["dimension"]] = counts.get(q["dimension"], 0) + 1
    assert set(counts) == set(DIMENSIONS), counts
    assert all(n >= 2 for n in counts.values()), counts

    # bands tile 0..100 exactly once
    assert BANDS[0][0] == 0 and BANDS[-1][1] == 100
    for previous, nxt in zip(BANDS, BANDS[1:]):
        assert previous[1] + 1 == nxt[0], (previous, nxt)
    for lo, hi, label, verdict in BANDS:
        assert lo <= hi and label and len(verdict.split(".")) >= 3

    top = {q["id"]: len(q["options"]) - 1 for q in QUESTIONS}
    bottom = {q["id"]: 0 for q in QUESTIONS}
    assert score(top)["total"] == 100
    assert score(bottom)["total"] == 0
    assert score(top)["gaps"] == []
    assert all(v == 100 for v in score(top)["dimensions"].values())
    assert all(v == 0 for v in score(bottom)["dimensions"].values())

    mid = {q["id"]: 2 for q in QUESTIONS}
    result = score(mid)
    assert 45 <= result["total"] <= 84, result["total"]
    assert result["band"][2] in ("Pockets of Progress", "Scaling With Gaps")
    assert len(result["gaps"]) <= 3

    for qid, entries in GAPS.items():
        assert qid in _BY_ID, qid
        for index in entries:
            assert 0 <= index < len(_BY_ID[qid]["options"]), (qid, index)
            assert entries[index].strip() and "—" not in entries[index], (qid, index)

    for lo, hi, label, verdict in BANDS:
        assert "—" not in verdict and "—" not in label

    # never crashes, always lands in a band
    for junk in ({}, None, [], {"nope": 3}, {ids[0]: 99}, {ids[0]: -1},
                 {ids[0]: "two"}, {ids[0]: None}, {ids[0]: True}, {ids[0]: 1.5}):
        out = score(junk)
        assert 0 <= out["total"] <= 100
        assert out["band"] in BANDS
        assert len(out["gaps"]) <= 3
    assert score({})["total"] == 0

    print("PASS: 10 questions, 4 dimensions, %d bands, %d gap statements."
          % (len(BANDS), sum(len(v) for v in GAPS.values())))


if __name__ == "__main__":
    demo()
