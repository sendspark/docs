# AEO / SEO content practices for docs

Mintlify auto-generates `llms.txt`, `llms-full.txt`, a `.md` version of every
page, and a sitemap. But **that plumbing only helps if the content is
citation-shaped.** This file covers how to write and structure docs so they rank
in Google *and* get cited by AI assistants (AEO = Answer Engine Optimization).

## Contents
- The answer-first page pattern
- Structural rules that help extraction
- Auto AEO artifacts to verify
- Indexing vs. pruning (noindex)
- Freshness

## The answer-first page pattern

Every high-value page should open so an assistant can lift the answer verbatim:

1. **Direct answer first** — a 40–60 word opening that fully answers the page's
   core question, before any preamble. This is what gets quoted.
2. **`## Key takeaways`** — a short bulleted summary near the top.
3. **Question-shaped H2/H3** — phrase headings as the real queries users type
   ("How do I send video in HubSpot?"), not noun labels ("HubSpot integration").
4. **A grounded FAQ** at the end (`<AccordionGroup>` of real questions).

This "answer-first + question headings + FAQ" pass is the core AEO upgrade.
Apply it hardest to pages that already rank p5–15 but leak the click to AI
Overviews / featured snippets — capturing the snippet recovers the click.

## Structural rules that help extraction

- **Self-contained sections** — no orphan pronouns ("as mentioned above"). An
  assistant may ingest one section in isolation; it must stand alone.
- **Tables for comparison/settings** — put plan matrices, option comparisons,
  and settings in real Markdown tables, not prose. They extract cleanly.
- **Don't hide facts in images** — a number or steps that exist only inside a
  screenshot are invisible to text extraction. Put them in text; use the image
  as support (with accurate alt text).
- **Keep it additive when fixing existing pages** — an answer-first opener + Key
  takeaways + FAQ can be *added* without rewording the body, which lets you do a
  large pass without introducing regressions. (Flag genuine content errors —
  wrong product names, contradictory numbers — separately for an SME; don't
  silently reword them.)

## Auto AEO artifacts to verify

After a build, confirm these serve correctly (they're free but worth checking):
- `llms.txt` at root — lists the kept pages, **not** the noindexed offenders.
- `llms-full.txt` — contains real page content.
- The `.md` version of a page is fetchable (content negotiation works).
- Per-page `canonical` resolves to the **production** host (not staging). This
  one can only fully pass after DNS cutover.

## Indexing vs. pruning (noindex)

The SEO-recovery payload of a migration is usually *removing* junk, not adding
content. Wrong-traffic pages (high impressions, ~0% CTR, no product intent) drag
sitewide CTR. Set `noindex: true` in frontmatter on those you keep for support
value; `drop` the truly worthless ones. Verify they're excluded from the sitemap
and `llms.txt`. Identify offenders from a Google Search Console export: pages with high
impressions, ~0% CTR, and no product intent.

Leave genuinely branded, product-relevant pages indexed even if their traffic
looks modest — they're the ones AEO lifts.

## Freshness

A verified lever: AI-cited content runs meaningfully fresher, and assistants
favor pages updated recently. **Cosmetic date bumps are counterproductive** —
Google penalized date-only edits (Dec 2025). Make refreshes substantive: add a
new example, a data point, or an FAQ entry per major section. Operationalize as a
monthly routine that picks the top-N pages by GSC impressions and refreshes each
with real content. Mark enhanced pages (e.g. a footer line + a `## Key takeaways`
section) so you can grep which pages have had the treatment.
