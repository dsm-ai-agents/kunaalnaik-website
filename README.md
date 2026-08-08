# KunaalNaik.com

Premium, dependency-free static website for Kunaal Naik’s corporate AI training and practical AI workflow consulting practice.

## Positioning

- Corporate AI training for leaders and functional teams
- Practical AI workflow consulting for enterprises, SMBs, and MSMEs
- Claude Cowork enablement
- Hermes Agent setup, training, and persistent workflows
- AI operator training for professionals

The base release deliberately excludes unsupported testimonials, client logos, statistics, and performance claims.

## Build and verify

```bash
python3 build.py
python3 check_site.py
python3 -m http.server 8765
```

Open http://127.0.0.1:8765/.

## Architecture

- `build.py` — shared stdlib site generator and page content
- `assets/site.css` — responsive design system
- `assets/site.js` — mobile navigation only
- `check_site.py` — metadata, schema, image, sitemap, and internal-link checks
- `docs/` — profile and competitor source material
- Generated multi-page HTML lives at the repository root

## Deployment

Vercel serves the generated static files directly. No framework, package manager, runtime, CMS, database, or client-side rendering is required.

Production URL: https://kunaalnaik-website.vercel.app/

Custom domain: `kunaalnaik.com` should be switched only after the Vercel preview is approved against the current live site.
