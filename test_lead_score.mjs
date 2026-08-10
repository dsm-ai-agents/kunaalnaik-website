// Rubric check for computeLeadScore. Run: node test_lead_score.mjs
import assert from 'node:assert/strict';
import { computeLeadScore } from './api/submit-scorecard.js';

const WORK = 'ceo@acme-industries.com';
const FREE = 'someone@gmail.com';

// Baseline: work email only, nothing else. +25 and no other line fires.
const base = { email: WORK, total_score: 0 };
assert.equal(computeLeadScore(base), 25, 'work email = +25');

// Each rubric line, isolated as a delta from the baseline.
assert.equal(computeLeadScore({ ...base, team_size: '50-200' }), 45, 'team 50+ = +20');
assert.equal(computeLeadScore({ ...base, team_size: '500+' }), 45, 'team 500+ = +20');
assert.equal(computeLeadScore({ ...base, role: 'Head of Operations' }), 45, 'seniority = +20');
assert.equal(computeLeadScore({ ...base, role: 'Data Analyst' }), 25, 'non-senior role = +0');
assert.equal(computeLeadScore({ ...base, budget_band: 'INR 5-10 lakh' }), 40, 'budget = +15');
assert.equal(computeLeadScore({ ...base, budget_band: '   ' }), 25, 'blank budget = +0');
assert.equal(computeLeadScore({ ...base, timeline: '0-3 months' }), 40, 'timeline <3mo = +15');
assert.equal(computeLeadScore({ ...base, timeline: 'immediately' }), 40, 'immediate = +15');
assert.equal(computeLeadScore({ ...base, timeline: '6-12 months' }), 25, 'timeline >3mo = +0');
assert.equal(computeLeadScore({ ...base, phone: '+91 98200 00000' }), 40, 'phone = +15');
assert.equal(computeLeadScore({ ...base, phone: '' }), 25, 'no phone is not penalised');

// Readiness band: mid score gains +20, an already-mature score loses 10.
assert.equal(computeLeadScore({ ...base, total_score: 55 }), 45, 'total 40-70 = +20');
assert.equal(computeLeadScore({ ...base, total_score: 40 }), 45, 'band inclusive at 40');
assert.equal(computeLeadScore({ ...base, total_score: 70 }), 45, 'band inclusive at 70');
assert.equal(computeLeadScore({ ...base, total_score: 71 }), 25, 'above band = +0');
assert.equal(computeLeadScore({ ...base, total_score: 90 }), 15, 'total >=85 = -10');

// Free email AND tiny team = -25. Padded so the clamp does not hide the delta.
const pad = { role: 'Director', budget_band: '2-5L', timeline: 'this quarter', phone: '999' };
assert.equal(computeLeadScore({ email: FREE, total_score: 0, team_size: '10-49', ...pad }), 65, 'control');
assert.equal(computeLeadScore({ email: FREE, total_score: 0, team_size: '1-9', ...pad }), 40, 'free + <10 = -25');

// Perfect enterprise lead: 130 raw, clamped to 100.
const enterprise = {
  email: 'priya@globalmanufacturing.co.in',
  organisation: 'Global Manufacturing',
  role: 'Chief Operating Officer',
  team_size: '500+',
  budget_band: 'INR 10-25 lakh',
  timeline: 'Within 3 months',
  phone: '+91 98200 12345',
  total_score: 55,
};
const eScore = computeLeadScore(enterprise);
assert.equal(eScore, 100, 'clamped to 100');
assert.ok(eScore >= 80, 'enterprise lead qualifies for the alert email');

// Gmail hobbyist, tiny team, high self-reported maturity: 0 - 10 - 25, clamped to 0.
const hobbyist = { email: FREE, team_size: '1-9', total_score: 90 };
assert.equal(computeLeadScore(hobbyist), 0, 'clamped to 0');
assert.ok(computeLeadScore({ email: FREE, team_size: '1-9', total_score: 30 }) < 50, 'hobbyist scores low');

// Missing/garbage input must not throw or credit a work email.
assert.equal(computeLeadScore({}), 0, 'empty payload = 0');
assert.equal(computeLeadScore({ email: FREE }), 0, 'free email alone = 0');

console.log('PASS: all lead_score rubric assertions held (24 checks).');
