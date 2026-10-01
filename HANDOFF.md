# Cohen & McMullen, P.A. — launch handoff

Live preview: https://cohenandmcmullen.burademirung.workers.dev · Repository: https://github.com/burademirung/cohenandmcmullen-site · Status as of 2026-09-30: deployed, awaiting the firm's decisions below.
Repository layout and commands: see `README.md`.

## Review completed (2026-09-30)
Three independent audits (content accuracy + Florida Bar advertising, technical SEO/AEO/GEO, accessibility + code) were run and their findings applied:
- Copy checked line by line against the firm's current site; invented or overstated claims removed; attorneys listed only on practices their bios support.
- Florida Bar / NY advertising: "Leaders" tagline replaced, client quote removed (client named factually), award years restored, "Prior results do not guarantee a similar outcome" added, full attorney-advertising footer with office address.
- Recognition badges removed (they implied firm-wide honors; Best Lawyers was a nomination). Replaced by a typographic line of outlets where Bradford M. Cohen has given commentary.
- Discover settlement page rewritten as a closed-claim status page (see decision 2).
- SEO: VideoObject markup removed (films are decorative), schema types corrected, page types, breadcrumbs, OG/Twitter images, favicons, self-hosted fonts, responsive posters, heading order, related-practice linking, content-based lastmod, `llms-full.txt`, legacy redirects.
- Performance: films re-encoded with bitrate caps (≈104 MB → ≈44 MB total, ≤2.8 MB per desktop film, ≤0.6 MB mobile), fonts self-hosted, header logo 320px WebP.
- Custom cursor and page-transition screen removed at the client's request.
- Client feedback rounds applied: readable FAQ panels and footer motto, always-visible evaluation CTA, tighter layout with a sticky consultation rail on practice pages, attorney cards rebuilt (full colour, aligned, credentials visible), press wall with real CNN / Fox News / NBC / CNBC logos, menu redesigned, full mobile pass.
- Eight films that read as synthetic (including the courthouse flag glitch) were regenerated image-first for photoreal results; see README "Film pipeline".

## Decisions needed before pointing the real domain
0. **Network logos.** The press wall shows CNN, Fox News, NBC and CNBC marks (from Wikimedia Commons) to reference Bradford M. Cohen's commentary appearances. Confirm the firm is comfortable with nominative use; Law&Crime, The Dan Abrams Show, Nancy Grace and Celebrity Justice appear as text.
1. **Contact form endpoint.** The form has `data-endpoint=""`; until set, submitting opens the visitor's email app to info@floridajusticefirm.com. Provide a form service / CRM webhook (or approve a Cloudflare Worker that emails the firm).
2. **Discover settlement page.** The firm's page states claims closed May 18, 2026, yet the live Wix page still takes sign-ups. Confirm whether the deadline was extended and who handles claims (the old page used ostrow@kolawyers.com). If still open, the eligibility form can be rebuilt; it collects EINs, so it needs a secure endpoint.
3. **Robinhood class action.** The old site had `/robinhood-class-action`; it now redirects to `/practice-areas/`. Provide content if that page should return.
4. **Los Angeles office.** Stated as "being opened" on the old site (last updated 2020). Confirm it is still planned or remove.
5. **Florida Bar review.** Have counsel confirm the "What we handle" lists, the "What to know in Florida" facts, the awards list, and naming President Trump as a client.
6. **Andrew B. Courtney's D.C. Bar admission** appears in his old sidebar but not his bio. Confirm.
7. **Headshots.** Three are only ~400px wide on the old site; request originals.
8. **Email domain.** The firm's email is @floridajusticefirm.com while the site is cohenandmcmullen.com. Use a matching mailbox if one exists, and keep NAP identical to the Google Business Profiles.

## When moving to the real domain (Cloudflare dashboard)
- Add the custom domain `www.cohenandmcmullen.com` to the Worker; redirect the apex to `https://www.` (301).
- Turn **off** "Block AI bots" / AI-crawler managed robots.txt, **Email Address Obfuscation**, and **Rocket Loader**, or they undo the AEO/GEO work and script order.
- Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools; check the rendered screenshot in URL Inspection.
