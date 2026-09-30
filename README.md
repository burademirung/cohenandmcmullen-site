# Cohen & McMullen, P.A. — website

Premium, motion-led static site for Cohen & McMullen, P.A. (complex litigation and criminal defense, Fort Lauderdale and New York). Every page opens on a full-screen film generated with Runway Gen‑4.5 and upscaled to 4K; the gold crest and lockup were redesigned in Runway (GPT Image 2.5).

**Preview:** https://cohenandmcmullen.burademirung.workers.dev (Cloudflare Workers static assets, temporary domain)

## Layout
| Path | What it is |
| --- | --- |
| `scripts/build.py` | Single source of truth: all copy, attorney data, FAQs, SEO metadata, JSON-LD. Generates every page into `site/`. |
| `site/` | Deployable output + assets (CSS, JS, fonts, films, posters, brand). This folder is what Cloudflare serves. |
| `site/assets/css/site.css`, `site/assets/js/site.js` | Design system and motion layer (GSAP + ScrollTrigger + Lenis, vendored). |
| `site/assets/video/` | Web encodes of the Runway films: `name.mp4` (1920px) and `name-sm.mp4` (960px, mobile). |
| `brand/` | Runway logo masters (crest and lockup, transparent PNG). |
| `scripts/transcode-web.sh` | Re-encodes Runway 4K masters into the web films and posters. |
| `scripts/pagehash.json` | Content hashes so `lastmod` / `dateModified` change only when a page's content changes. |
| `research/source-content.md` | Everything extracted from the firm's current website (the only content source). |
| `wrangler.jsonc` | Cloudflare deploy config (assets directory `site`). |

## Work on it
```bash
python3 scripts/build.py                 # regenerate all pages, sitemap, robots, llms.txt, llms-full.txt
cd site && python3 -m http.server 8765   # preview at http://127.0.0.1:8765
npx wrangler deploy                      # publish to Cloudflare
```
Edit copy in `scripts/build.py` (dicts `PEOPLE`, `PRACTICES`, `FLORIDA`, `HOME_FAQ`, and the `build_*` page functions), never the generated HTML.

## SEO / AEO / GEO
- Unique titles, descriptions (≤160 chars, enforced by the build), canonicals, OG/Twitter cards (1200×630 JPG per page, attorney cards on bios).
- JSON-LD graph per page: Organization (firm), LegalService (each office), Person (each attorney with credentials, alumni, memberships), Service + FAQPage (practice pages), Breadcrumb, typed pages (ProfilePage, AboutPage, ContactPage).
- Direct-answer block and "What to know in Florida" facts on every practice page; FAQ questions are headings inside `<details>`, fully present in HTML.
- `robots.txt` welcomes AI crawlers; `llms.txt` and `llms-full.txt` (plain text of every page); `sitemap.xml` with content-based `lastmod`.
- Legacy Wix URLs preserved or redirected (`site/_redirects`); caching and security headers in `site/_headers`.

## Design rules from the brief
No icons, no numbered markers or stat counters, tiles with real footage, full-screen film on every page, the firm's crest everywhere. Motion respects `prefers-reduced-motion`, data-saver connections skip films, and a static fallback shows all content if animation frames never run.

See `HANDOFF.md` for launch decisions that need the firm's input.
