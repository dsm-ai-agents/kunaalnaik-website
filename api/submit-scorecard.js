// AI Readiness Scorecard — submission endpoint.
//
// Zero npm dependencies: global fetch + the standard Vercel (req, res) pair.
// Every credential comes from process.env and is never echoed back to the client.
//
// TRUST NOTE: total_score, dimension_scores, answers and gaps arrive from the
// visitor's browser. They are advisory only and could be forged — they are
// stored and shown back, nothing more. lead_score is computed here, server-side,
// from the submitted fields and is the figure to trust for follow-up.

const FREE_EMAIL_DOMAINS = [
  'gmail', 'yahoo', 'hotmail', 'outlook', 'icloud', 'proton', 'rediffmail',
];

const DISPOSABLE_DOMAINS = [
  'mailinator', 'guerrillamail', '10minutemail', 'tempmail', 'throwaway', 'yopmail',
];

const SENIORITY = [
  'cxo', 'chief', 'head', 'director', 'vp', 'president', 'founder', 'owner', 'partner',
];

const clean = (v) => (typeof v === 'string' ? v.trim() : '');
const orNull = (v) => (clean(v) === '' ? null : clean(v));
const domainOf = (email) => clean(email).toLowerCase().split('@')[1] || '';
const nums = (s) => (clean(s).match(/\d+/g) || []).map(Number);

const isFreeEmail = (email) => {
  const d = domainOf(email);
  return FREE_EMAIL_DOMAINS.some((f) => d.startsWith(`${f}.`) || d === f);
};

// "50-200", "500+", "50 or more" -> true. "1-9", "10-49" -> false.
const teamAtLeast50 = (t) => nums(t).some((n) => n >= 50);

// "1-9", "under 10", "5" -> true. Unknown/blank -> false.
const teamUnder10 = (t) => {
  const n = nums(t);
  return n.length > 0 && Math.max(...n) < 10;
};

const isSenior = (role) => {
  const r = clean(role).toLowerCase();
  return SENIORITY.some((k) => new RegExp(`\\b${k}\\b`).test(r));
};

// "immediately", "this quarter", "0-3 months", "under 3 months", "6 weeks" -> true.
const timelineUnder3Months = (t) => {
  const s = clean(t).toLowerCase();
  if (!s) return false;
  if (/immediat|asap|right away|already|this quarter|current quarter|next month/.test(s)) return true;
  if (/\b(day|days|week|weeks)\b/.test(s)) return true;
  const n = nums(s);
  return n.length > 0 && Math.max(...n) <= 3;
};

/**
 * Pure, testable lead scoring rubric. Returns an integer clamped to 0..100.
 * See test_lead_score.mjs.
 */
export function computeLeadScore(data = {}) {
  const {
    email, team_size, role, budget_band, timeline, phone, total_score,
  } = data;

  const free = isFreeEmail(email);
  const total = Number.isFinite(Number(total_score)) ? Number(total_score) : null;

  let score = 0;
  if (!free && domainOf(email)) score += 25;         // work email
  if (teamAtLeast50(team_size)) score += 20;         // 50+ people
  if (isSenior(role)) score += 20;                   // decision-making seniority
  if (clean(budget_band) !== '') score += 15;        // budget indicated
  if (timelineUnder3Months(timeline)) score += 15;   // near-term need
  if (clean(phone) !== '') score += 15;              // volunteered a phone number
  if (total !== null && total >= 40 && total <= 70) score += 20; // real gap, real capacity
  if (total !== null && total >= 85) score -= 10;    // already mature, less to do
  if (free && teamUnder10(team_size)) score -= 25;   // hobbyist signal

  return Math.max(0, Math.min(100, score));
}

const plausibleEmail = (email) => /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/.test(clean(email));
const isDisposable = (email) => {
  const d = domainOf(email);
  return DISPOSABLE_DOMAINS.some((bad) => d.includes(bad));
};

const esc = (s) => String(s ?? '')
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function reportHtml(d, leadScore) {
  const dims = Object.entries(d.dimension_scores || {})
    .map(([k, v]) => `<li><strong>${esc(k)}</strong>: ${esc(v)}</li>`).join('');
  const gaps = (Array.isArray(d.gaps) ? d.gaps : [])
    .map((g) => `<li>${esc(typeof g === 'string' ? g : g.title || JSON.stringify(g))}</li>`).join('');

  return `<!doctype html>
<html lang="en-GB"><body style="font-family:Georgia,serif;font-size:16px;line-height:1.6;color:#1a1a1a;max-width:640px">
<p>Hello ${esc(d.name)},</p>
<p>Here is your AI readiness scorecard for ${esc(d.organisation)}, as requested.</p>
<p><strong>Overall readiness score: ${esc(d.total_score)}/100</strong></p>
${dims ? `<p><strong>By dimension</strong></p><ul>${dims}</ul>` : ''}
${gaps ? `<p><strong>Where the gaps are</strong></p><ul>${gaps}</ul>` : ''}
<p>How to read this: the score is a snapshot, not a verdict. The gaps above are
the places where a small amount of structure usually produces the largest
change — normally clearer usage policy, a few worked examples per team, and one
named owner per workflow.</p>
<p>If you want a second opinion on the gaps, reply to this email and it comes
straight to me. One reply, from me. No newsletter, no automated calls.</p>
<p>Kunaal Naik<br>Corporate AI trainer and AI workflow consultant<br>me@kunaalnaik.com</p>
</body></html>`;
}

function alertHtml(d, leadScore) {
  const gaps = (Array.isArray(d.gaps) ? d.gaps : []).slice(0, 3)
    .map((g) => `<li>${esc(typeof g === 'string' ? g : g.title || JSON.stringify(g))}</li>`).join('');
  return `<html><body style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.5">
<p><strong>Qualified scorecard lead (lead score ${leadScore})</strong></p>
<ul>
<li>Name: ${esc(d.name)}</li>
<li>Organisation: ${esc(d.organisation)}</li>
<li>Role: ${esc(d.role) || '—'}</li>
<li>Team size: ${esc(d.team_size) || '—'}</li>
<li>Email: ${esc(d.email)}</li>
${d.phone ? `<li>Phone: ${esc(d.phone)}</li>` : ''}
<li>Readiness score (client-reported): ${esc(d.total_score)}</li>
<li>Lead score (server-computed): ${leadScore}</li>
</ul>
${gaps ? `<p>Top gaps</p><ul>${gaps}</ul>` : ''}
</body></html>`;
}

async function sendEmail({ to, subject, html }) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ from: process.env.RESEND_FROM, to: [to], subject, html }),
  });
  if (!res.ok) throw new Error(`Resend responded ${res.status}: ${await res.text()}`);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = null; }
  }
  if (!body || typeof body !== 'object') {
    return res.status(400).json({ error: 'Expected a JSON body.' });
  }

  const name = clean(body.name);
  const email = clean(body.email);
  const organisation = clean(body.organisation);

  const missing = [
    !name && 'name',
    !email && 'email',
    !organisation && 'organisation',
  ].filter(Boolean);
  if (missing.length) {
    return res.status(400).json({ error: `Please provide: ${missing.join(', ')}.` });
  }
  if (!plausibleEmail(email)) {
    return res.status(400).json({ error: 'That email address does not look valid.' });
  }
  if (isDisposable(email)) {
    return res.status(400).json({ error: 'Please use your work email address — disposable addresses are not accepted.' });
  }

  const data = {
    name,
    email,
    organisation,
    role: orNull(body.role),
    team_size: orNull(body.team_size),
    phone: orNull(body.phone),          // optional by design: no cold-call funnel
    budget_band: orNull(body.budget_band),
    timeline: orNull(body.timeline),
    total_score: Number.isFinite(Number(body.total_score)) ? Number(body.total_score) : null,
    dimension_scores: body.dimension_scores ?? null,
    answers: body.answers ?? null,
    gaps: body.gaps ?? null,
    consent: body.consent === true,
    user_agent: req.headers['user-agent'] || null,
    referrer: req.headers.referer || req.headers.referrer || null,
  };

  const leadScore = computeLeadScore(data);

  let stored = false;
  try {
    const url = `${process.env.SUPABASE_URL}/rest/v1/scorecard_submissions`;
    const r = await fetch(url, {
      method: 'POST',
      headers: {
        apikey: process.env.SUPABASE_ANON_KEY,
        Authorization: `Bearer ${process.env.SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal',
      },
      body: JSON.stringify({ ...data, lead_score: leadScore }),
    });
    if (!r.ok) throw new Error(`Supabase responded ${r.status}: ${await r.text()}`);
    stored = true;
  } catch (err) {
    console.error('scorecard: Supabase insert failed', err);
  }

  let emailed = false;
  try {
    await sendEmail({
      to: email,
      subject: `Your AI readiness scorecard — ${organisation}`,
      html: reportHtml(data, leadScore),
    });
    emailed = true;
  } catch (err) {
    console.error('scorecard: visitor report email failed', err);
  }

  if (leadScore >= 80) {
    try {
      await sendEmail({
        to: process.env.KUNAAL_EMAIL,
        subject: `Scorecard lead ${leadScore}: ${name} — ${organisation}`,
        html: alertHtml(data, leadScore),
      });
    } catch (err) {
      console.error('scorecard: lead alert email failed', err);
    }
  }

  // Always 200 once validation has passed: the visitor already has their result
  // on screen and must never lose it to an infrastructure failure.
  return res.status(200).json({ ok: true, stored, emailed });
}
