// AI Readiness Scorecard. Questions, points, bands and gap text all come from
// the embedded JSON, which build.py serialises from scorecard_content.py, so
// this file holds no content and cannot drift from the Python source.
(function () {
  var el = document.getElementById('sc-data');
  var app = document.getElementById('sc-app');
  if (!el || !app) return;

  var D = JSON.parse(el.textContent);
  var Q = D.questions;
  var answers = {};
  var step = 0;
  app.hidden = false;

  // ---- render one screen per question ------------------------------------
  var host = document.getElementById('sc-questions');
  Q.forEach(function (q, qi) {
    var div = document.createElement('div');
    div.className = 'sc-step';
    div.dataset.step = String(qi);
    var opts = q.options.map(function (o, oi) {
      return '<li><label class="sc-opt"><input type="radio" name="' + q.id + '" value="' + oi + '">' +
             escapeHtml(o.label) + '</label></li>';
    }).join('');
    div.innerHTML =
      '<p class="sc-meta">' + (qi + 1) + ' of ' + Q.length + ' &middot; ' + escapeHtml(q.dimension) + '</p>' +
      '<h2 class="sc-q">' + escapeHtml(q.text) + '</h2>' +
      '<ul class="sc-opts">' + opts + '</ul>' +
      '<div class="sc-nav">' + (qi > 0 ? '<button type="button" class="sc-back">Back</button>' : '') + '</div>';
    host.appendChild(div);
  });

  var steps = [].slice.call(document.querySelectorAll('.sc-step'));

  function show(i) {
    step = i;
    steps.forEach(function (s, n) { s.classList.toggle('on', n === i); });
    document.getElementById('sc-bar').style.width = Math.round((i / Q.length) * 100) + '%';
    var h = steps[i].querySelector('.sc-q, .sc-meta');
    if (h) h.setAttribute('tabindex', '-1'), h.focus({ preventScroll: true });
    window.scrollTo({ top: app.offsetTop - 90, behavior: 'smooth' });
  }

  // advance on choice; no Next button needed
  host.addEventListener('change', function (e) {
    var input = e.target;
    if (input.type !== 'radio') return;
    answers[input.name] = Number(input.value);
    var row = input.closest('.sc-opt');
    [].forEach.call(row.parentNode.parentNode.querySelectorAll('.sc-opt'), function (o) {
      o.classList.remove('sel');
    });
    row.classList.add('sel');
    setTimeout(function () { step + 1 < Q.length ? show(step + 1) : finish(); }, 180);
  });

  host.addEventListener('click', function (e) {
    if (e.target.classList.contains('sc-back')) show(Math.max(0, step - 1));
  });

  // ---- scoring: mirrors scorecard_content.score() ------------------------
  // Python normalises each question against its OWN worst option (points-worst)
  // rather than raw points, and breaks gap ties by dimension priority. Both are
  // reproduced here; test_scorecard.py fails the build if they ever disagree.
  function score() {
    var perDim = {}, maxDim = {}, raw = 0, max = 0, gaps = [];
    Object.keys(D.dimensions).forEach(function (d) { perDim[d] = 0; maxDim[d] = 0; });
    Q.forEach(function (q) {
      var pts = q.options.map(function (o) { return o.points; });
      var best = Math.max.apply(null, pts);
      var worst = Math.min.apply(null, pts);
      var idx = answers[q.id];
      var valid = (typeof idx === 'number' && q.options[idx]);
      var got = valid ? q.options[idx].points : worst;
      raw += got - worst; max += best - worst;
      perDim[q.dimension] += got - worst;
      maxDim[q.dimension] += best - worst;
      var g = D.gaps[q.id] && D.gaps[q.id][String(valid ? idx : 0)];
      if (g) gaps.push({ text: g, lost: best - got, pri: D.priority[q.dimension] });
    });
    var dims = {};
    Object.keys(maxDim).forEach(function (k) {
      dims[k] = maxDim[k] ? Math.round((perDim[k] / maxDim[k]) * 100) : 0;
    });
    var total = max ? Math.round((raw / max) * 100) : 0;
    var band = D.bands.filter(function (b) { return total >= b.min && total <= b.max; })[0] || D.bands[0];
    gaps.sort(function (a, b) { return (b.lost - a.lost) || (a.pri - b.pri); });
    return { total: total, dims: dims, band: band, gaps: gaps.slice(0, 3).map(function (g) { return g.text; }) };
  }

  var result = null;

  function finish() {
    result = score();
    document.getElementById('sc-total').textContent = result.total;
    document.getElementById('sc-band-label').textContent = result.band.label;
    document.getElementById('sc-verdict').textContent = result.band.verdict;
    Object.keys(result.dims).forEach(function (name) {
      var bar = document.querySelector('[data-dim-bar="' + name + '"]');
      var val = document.querySelector('[data-dim-val="' + name + '"]');
      if (bar) bar.style.width = result.dims[name] + '%';
      if (val) val.textContent = result.dims[name];
    });
    // EU/UK/EEA visitors get an explicit, unticked consent box. Same timezone
    // heuristic as the visitor tag; see build.py for the accepted limitation.
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      if (/^(Europe\/|Atlantic\/(Azores|Madeira|Canary|Faeroe|Reykjavik)$|Arctic\/Longyearbyen$)/.test(tz)) {
        var row = document.getElementById('sc-consent-row');
        row.hidden = false;
        document.getElementById('sc-consent').required = true;
      }
    } catch (e) {}
    var last = steps[steps.length - 1];
    steps.forEach(function (s) { s.classList.remove('on'); });
    last.classList.add('on');
    document.getElementById('sc-bar').style.width = '100%';
    window.scrollTo({ top: app.offsetTop - 90, behavior: 'smooth' });
  }

  // ---- gated report ------------------------------------------------------
  var form = document.getElementById('sc-form');
  var msg = document.getElementById('sc-msg');
  var btn = document.getElementById('sc-submit');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form);
    var required = ['name', 'email', 'organisation'];
    var missing = required.filter(function (k) { return !String(f.get(k) || '').trim(); });
    if (missing.length) { return say('Please fill in your name, work email, and organisation.'); }
    var consentRow = document.getElementById('sc-consent-row');
    if (!consentRow.hidden && !document.getElementById('sc-consent').checked) {
      return say('Please tick the consent box so the report can be sent.');
    }
    btn.disabled = true; btn.textContent = 'Sending…';
    var payload = {
      name: f.get('name'), email: f.get('email'), organisation: f.get('organisation'),
      role: f.get('role') || null, team_size: f.get('team_size') || null,
      phone: f.get('phone') || null, budget_band: f.get('budget_band') || null,
      timeline: f.get('timeline') || null,
      total_score: result.total, dimension_scores: result.dims,
      answers: answers, gaps: result.gaps,
      consent: consentRow.hidden ? true : document.getElementById('sc-consent').checked,
      referrer: document.referrer || null
    };
    fetch('/api/submit-scorecard', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().then(function (j) { return { ok: r.ok, j: j }; });
    }).then(function (res) {
      if (!res.ok) { btn.disabled = false; btn.textContent = 'Send my report'; return say(res.j.error || 'Something went wrong. Please email me@kunaalnaik.com.'); }
      reveal(res.j);
    }).catch(function () {
      btn.disabled = false; btn.textContent = 'Send my report';
      // Never lose the visitor's result to a network failure.
      reveal({ emailed: false, offline: true });
    });
  });

  function reveal(flags) {
    var out = document.getElementById('sc-gaps-out');
    var list = document.getElementById('sc-gaps');
    list.innerHTML = '';
    (result.gaps.length ? result.gaps : ['No major gaps surfaced. The useful next step is verifying that what works for one team survives handover to another.'])
      .forEach(function (g) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(g));
        list.appendChild(li);
      });
    out.hidden = false;
    form.hidden = true;
    if (flags && flags.emailed === false) {
      say('Your gaps are below. The email could not be sent just now, so take a screenshot or email me@kunaalnaik.com and Kunaal will resend it.');
    } else {
      say('Your gaps are below, and the full report is on its way by email.');
    }
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function say(text) {
    msg.innerHTML = '';
    var p = document.createElement('p');
    p.className = 'sc-msg';
    p.textContent = text;
    msg.appendChild(p);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  show(0);
})();
