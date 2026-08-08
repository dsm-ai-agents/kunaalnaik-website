# SEO/AEO Audit — Kunaal Naik Website

Audit date: 8 August 2026  
Audited build: `https://kunaalnaik-website.vercel.app/`  
Intended canonical domain: `https://kunaalnaik.com/`  
Scope: technical SEO, on-page SEO, structured data, answer-engine readiness, entity/trust, case-study evidence, crawler policy, indexing signals, and page experience.

## Verdict

**Partially compliant. The new static build follows most foundational technical SEO/AEO guidelines, but the public domain configuration prevents it from being fully production-ready.**

The largest problem is not the design or HTML. Every page on the Vercel build declares `kunaalnaik.com` as canonical, while `kunaalnaik.com` still serves the old JavaScript site. Its `/sitemap.xml` still returns HTML with HTTP 200 instead of XML. Search results currently show only the old homepage, and no result was found for the Vercel alias. Until the custom domain is switched to this build—or canonicals are temporarily changed—the new pages are not the authoritative production pages search engines are being asked to index.

Google and Bing both state that ordinary SEO foundations remain the basis for AI answers, citations, and generative search. There is no separate AEO shortcut. The new build has the right foundation, but it still needs domain consolidation, indexing setup, more first-hand evidence, real insight pages, author/date markup, and third-party corroboration.

## Audit summary

| Area | Status | Finding |
|---|---|---|
| Static crawlability | Pass | All 14 public URLs return useful pre-rendered HTML. |
| HTTP status handling | Pass on Vercel | Valid pages return 200; a nonexistent path returns a real 404. |
| Canonicalization | **Fail in production** | Vercel pages canonicalize to a different site that still serves the old build. Apex and `www` also both return 200 without consolidating redirects. |
| XML sitemap | Pass on Vercel; **fail on canonical domain** | Vercel serves valid XML containing 14 URLs; `kunaalnaik.com/sitemap.xml` returns the old HTML shell with 200. |
| Robots/crawler policy | Pass on Vercel | Search/answer crawlers are allowed; GPTBot and ClaudeBot are separately blocked. The sitemap target is ineffective until domain cutover. |
| Titles/descriptions/H1 | Pass | All audited pages have unique titles, descriptions, and exactly one H1. |
| Internal links/navigation | Pass with improvement needed | No broken links or placeholders; Case Studies is visible. Contextual links between services, evidence, and insights remain weak. |
| Structured data | Partial pass | Valid `WebSite`, `Person`, `WebPage`, `ProfilePage`, and `Service` JSON-LD; missing `BreadcrumbList`, standalone `Organization`, and article/case-study authorship and dates. |
| Entity clarity | Partial pass | Kunaal, role, image, founder relationship, and social profiles are consistent; external corroboration and organization markup need strengthening. |
| Answer-ready content | Partial pass | Strong direct positioning and clear headings; too few worked examples, source citations, definitions, comparisons, and independently verifiable artifacts. |
| Case-study credibility | Partial pass | Training-versus-production boundaries are transparent; no screenshots, dates, files, attendee evidence, host reference, or permitted quantified outcomes are published. |
| Insights/content library | **Not complete** | `/insights/` is a roadmap, not a library of independently useful articles. |
| Search measurement | Not verified | Search Console, Bing Webmaster Tools, IndexNow, indexing coverage, and AI-referral analytics were not available for verification. |
| Performance/CWV | Inconclusive | Static payloads are small and no browser errors appeared, but PageSpeed returned HTTP 429; no Lighthouse/Core Web Vitals score is claimed. |

## What passes the researched guidelines

### 1. Technical foundation

- Fourteen descriptive public URLs are available as standalone static HTML.
- Titles, descriptions, H1s, canonical links, body content, and JSON-LD exist in raw HTML and do not depend on client-side rendering.
- The Vercel build returns a real HTTP 404 for a nonexistent path.
- The Vercel sitemap is valid XML and lists the complete public page set.
- Every audited page has one H1 and unique title metadata.
- Internal links use standard crawlable `<a href>` elements; no `#` or JavaScript placeholder links were found.
- The homepage exposes clear primary navigation, a skip link, semantic headings, and labelled navigation.
- The optimized portrait is approximately 10.5 KB; homepage HTML is approximately 12.4 KB and CSS approximately 10.8 KB in the observed transfers.
- No browser console or JavaScript errors were observed.

These implementation choices align with Google’s guidance to maintain crawlable links, textual content, good page experience, and technically accessible pages, and with Bing’s guidance on XML sitemaps, canonical URLs, semantic HTML, accurate statuses, and crawlable internal links.[1][5]

### 2. Crawler policy

The Vercel build allows:

- all normal crawlers
- `OAI-SearchBot`
- `Claude-SearchBot`
- `Claude-User`
- `PerplexityBot`

It separately disallows:

- `GPTBot`
- `ClaudeBot`

That correctly distinguishes answer/search retrieval from potential model-training access. OpenAI explicitly says OAI-SearchBot must not be blocked if content is intended for ChatGPT summaries and snippets, while GPTBot can be blocked independently.[4]

### 3. On-page intent and entity clarity

- Commercial pages target distinct intents instead of duplicating one keyword page: corporate training, automation consulting, Claude Cowork, Hermes Agent, professional/founder enablement, speaking, and contact.
- The homepage states who Kunaal helps, the business outcome, and the mechanisms near the top.
- The About page uses `ProfilePage` with Kunaal as its `mainEntity`, matching Google’s supported structure.[2]
- The Person entity contains a stable name, URL, image, job title, description, social profiles, and founder relationship.
- Contact, privacy, and terms pages are real pages rather than placeholders.
- The case study explicitly distinguishes a training demonstration from audited production results, reducing unsupported-claim risk.

### 4. AEO direction

The copy already uses several answer-friendly patterns:

- direct problem/outcome statements near the top
- focused headings
- a named operating method
- explicit limitations and governance boundaries
- inspectable lists of outputs and engagement formats
- clear entity and product names

This is directionally consistent with Google’s recommendation for unique, valuable, first-hand content and Bing’s recommendation for clear, focused, independently verifiable pages that state key information early.[1][3][5]

## Defects and gaps

### P0 — blocking production discoverability

#### 1. Canonical domain and deployed content disagree

Observed:

- Every new Vercel page declares a canonical URL on `https://kunaalnaik.com/`.
- `https://kunaalnaik.com/` still serves the old 1,859-byte JavaScript shell.
- `https://kunaalnaik.com/sitemap.xml` returns that HTML shell with status 200 and `text/html`.
- Both `https://kunaalnaik.com/` and `https://www.kunaalnaik.com/` return 200 rather than consolidating to one hostname.
- A search for `site:kunaalnaik.com "Kunaal Naik"` returned only the old homepage.
- A search for the Vercel alias returned no pages, which is unsurprising because the alias points canonically elsewhere.

Impact:

Search engines are told that the old custom-domain URLs are authoritative, but those URLs do not contain the new pages. The Vercel build is therefore a strong staging deployment, not a complete SEO production deployment.

Minimal fix:

1. Explicitly approve custom-domain cutover.
2. Attach `kunaalnaik.com` to this Vercel project.
3. Redirect `www` to the chosen apex hostname with HTTP 301.
4. Verify that all 14 canonical URLs serve the new HTML.
5. Verify that `/sitemap.xml`, `/robots.txt`, and a nonexistent URL return the correct content/status on the custom domain.

Do not change canonicals to the Vercel alias unless the alias is intentionally becoming the permanent public brand domain.

#### 2. Search Console and Bing indexing workflow is unverified

No evidence was available that the canonical domain property, sitemap submission, URL inspection, Bing Webmaster Tools, or IndexNow are configured for the new build.

Minimal fix after cutover:

- verify the domain in Google Search Console and Bing Webmaster Tools
- submit the canonical sitemap
- inspect the homepage, About, each primary commercial page, and the case study
- use IndexNow for Bing/Copilot change notification
- monitor indexed-versus-submitted pages and generative-search reporting where available

### P1 — high-value content and trust improvements

#### 3. The Insights page is a publishing roadmap, not an answer library

The six cards do not link to substantive articles. This means the site has commercial pages but little first-hand informational content that Google, Bing/Copilot, ChatGPT, Claude, or Perplexity can cite for non-branded questions.

Minimal next assets:

1. Claude Cowork vs Hermes Agent: a decision framework
2. Corporate AI training curriculum by role
3. How to measure AI workshop ROI
4. Safe Claude Cowork setup and verification checklist
5. One evidence-rich workflow teardown with screenshots and files

Each should have a stable URL, author, dates, sources, worked example, limitations, and contextual links to the relevant service page.

#### 4. The case study is honest but not yet independently inspectable

Strengths:

- clear GCC Consulting Firm context
- accurate `CLAUDE.md` terminology
- distinction between demonstration and deployment
- no unsupported public financial or accuracy result

Missing evidence:

- training date and session format
- agenda or slide excerpt
- screenshots/video clips
- sample input/output files
- explanation of which data was fictitious
- participant or host corroboration
- permission statement
- measured result, if one becomes verifiable

The page is therefore useful first-hand narrative, but still weak as independent proof. Google’s people-first guidance asks whether content provides original information, demonstrates expertise, identifies who created it, and gives readers reasons to trust it.[3]

#### 5. Authorship and freshness are weak

The case-study page and future Insights pages use generic `WebPage` schema and do not show:

- author byline
- `datePublished`
- meaningful `dateModified`
- editorial/source note
- `Article` or `BlogPosting` schema

Minimal fix:

Use `Article` for substantive case studies and articles, connect `author` to the existing Person entity, and show truthful dates visibly. Do not update `dateModified` automatically unless the content materially changed.

#### 6. Structured data is valid but incomplete

Current graph types:

- `WebSite`
- `Person`
- `WebPage`
- `ProfilePage`
- `Service`

Useful additions:

- `BreadcrumbList` on nested pages
- a standalone `Organization` node for Data Science Masterminds with verified URL/logo/contact/sameAs fields
- `Article`/`BlogPosting` for real editorial pages
- article author/date/image properties

Avoid adding schema purely for keywords. Google requires markup to represent visible content and recommends validation and Search Console monitoring.[2]

#### 7. Contextual internal linking is too light

The global header/footer reaches the important pages, but body content rarely links:

- Claude Cowork training → GCC case study
- case study → Claude Cowork training and corporate training
- About → speaking and case studies
- service pages → relevant future guides

Minimal fix: add one or two descriptive contextual links where the reader naturally needs proof or next-step detail. No new linking component is needed.

#### 8. External corroboration is still limited

Search results show Kunaal’s YouTube and LinkedIn activity for Hermes Agent and Claude Cowork, which is useful external evidence. The website currently links only to profile roots rather than matching videos/posts, and no host/client/event page corroborates the GCC case study.

Minimal fix:

- link relevant first-party videos from matching website pages
- obtain legitimate host/event recap or speaker pages
- keep role, bio, headshot, domain, and service descriptors consistent across LinkedIn, YouTube, organization profiles, and event pages
- never manufacture backlinks, reviews, or mentions

### P2 — worthwhile refinements

- Add `og:image:alt` and explicit social-image dimensions.
- Replace the generator’s global hard-coded sitemap `lastmod` with truthful per-page dates before future updates make it inaccurate.
- Consider slightly shortening the 70-character AI Automation Consulting title; this is a presentation refinement, not a compliance failure.
- Add descriptive, human-written question sections to service pages where buyers need direct answers about audience, delivery, prerequisites, data safety, and measurement. FAQ schema is not required.
- Add visible source links on expert guides and comparison pages.
- Test the production custom domain with Google Rich Results Test after cutover.

## Page-experience observation

The observed desktop page has:

- a clear above-the-fold positioning statement
- readable heading hierarchy and contrast
- a visible portrait with dimensions set
- straightforward calls to action
- no visible broken layout or console errors

The PageSpeed Insights API returned HTTP 429 during this audit. Therefore, no Lighthouse, Core Web Vitals, LCP, CLS, or accessibility score is claimed. Small transfer sizes are encouraging but are not a substitute for field or lab performance data.

## Recommended execution order

1. **Approve and perform the `kunaalnaik.com` cutover.**
2. Verify apex/`www` redirect, canonical parity, sitemap XML, robots, and real 404s on the custom domain.
3. Configure Search Console, Bing Webmaster Tools, sitemap submission, and IndexNow.
4. Add authorship/date/article schema and breadcrumb schema in the shared generator.
5. Strengthen the GCC case study with approved screenshots, session facts, sample artifacts, and corroboration.
6. Publish the first three evidence-rich Insights pages.
7. Add contextual links between commercial pages, case studies, and guides.
8. Run Lighthouse/PageSpeed and mobile accessibility checks on the canonical domain.
9. Begin monthly search and answer-engine visibility measurement.

## Bottom line

**The codebase follows the researched SEO/AEO foundation substantially better than the old site. The live search setup does not yet fully follow it because the canonical domain still serves the old website.**

After domain consolidation, the main constraint will shift from technical crawlability to evidence: original guides, inspectable case-study artifacts, authorship, citations, third-party corroboration, and measured indexing/traffic.

## Sources

[1] Google Search Central — Optimizing for generative AI features: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide  
[2] Google Search Central — ProfilePage structured data: https://developers.google.com/search/docs/appearance/structured-data/profile-page  
[3] Google Search Central — Creating helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content  
[4] OpenAI — Publishers and Developers FAQ: https://help.openai.com/en/articles/12627856-publishers-and-developers-faq  
[5] Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a  
[6] Existing research strategy: `/home/kunaal/workspace/marketing-funnels/kunaalnaik-seo-aeo/seo-aeo-and-ai-authority-strategy.md`
