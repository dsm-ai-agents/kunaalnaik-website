-- ---------------------------------------------------------------------------
-- AI Readiness Scorecard — submission storage
-- Paste this whole file into the Supabase SQL editor and run it once.
--
-- SECURITY MODEL (read this before changing anything)
--
--   The website is a static site on Vercel. The serverless function writes to
--   this table using the *publishable* anon key. That key is low-trust: treat
--   it as public. Row Level Security is therefore enabled and the anon role is
--   granted exactly one capability — INSERT.
--
--   anon may INSERT.  anon may NEVER SELECT, UPDATE or DELETE.
--
--   Consequence: even if the anon key leaks, nobody can read anybody else's
--   submission, edit a row, or wipe the table. There is deliberately no SELECT
--   policy for anon, so every read is refused by default.
--
--   Kunaal reads submissions in the Supabase dashboard (which authenticates as
--   the service role and bypasses RLS). Do not add a SELECT policy for anon to
--   "make the dashboard easier" — the dashboard already works.
--
--   total_score / dimension_scores / answers / gaps are computed in the
--   visitor's browser and are ADVISORY ONLY: they can be forged. lead_score is
--   computed server-side in api/submit-scorecard.js and is the trustworthy
--   figure for prioritising follow-up.
-- ---------------------------------------------------------------------------

create table if not exists public.scorecard_submissions (
  id               bigserial primary key,
  created_at       timestamptz not null default now(),
  name             text not null,
  email            text not null,
  organisation     text not null,
  role             text,
  team_size        text,
  phone            text,
  budget_band      text,
  timeline         text,
  total_score      int,
  dimension_scores jsonb,
  answers          jsonb,
  gaps             jsonb,
  lead_score       int,
  consent          boolean not null default false,
  user_agent       text,
  referrer         text
);

alter table public.scorecard_submissions enable row level security;

-- Insert-only policy for the public/anon key. No USING clause, so no read.
drop policy if exists "anon can insert submissions" on public.scorecard_submissions;
create policy "anon can insert submissions"
  on public.scorecard_submissions
  for insert
  to anon
  with check (true);

grant insert on public.scorecard_submissions to anon;
grant usage, select on sequence public.scorecard_submissions_id_seq to anon;

create index if not exists scorecard_submissions_created_at_idx
  on public.scorecard_submissions (created_at desc);

create index if not exists scorecard_submissions_lead_score_idx
  on public.scorecard_submissions (lead_score desc);

-- ---------------------------------------------------------------------------
-- For Kunaal: run this in the SQL editor to see the newest qualified leads.
-- ---------------------------------------------------------------------------
-- select created_at,
--        name,
--        organisation,
--        role,
--        team_size,
--        email,
--        phone,
--        total_score,
--        lead_score,
--        gaps
--   from public.scorecard_submissions
--  where lead_score >= 60
--  order by created_at desc
--  limit 50;
