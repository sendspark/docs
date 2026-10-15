# Authoring / updating a doc page for a feature

Reference for the internal case: a feature shipped or changed, and its docs need
to be created or updated. The aim is a page that's correct, follows the
answer-first structure (`aeo-content.md`), is placed in nav, and ships with a
media plan (`media-plan.md`) for the screenshots/video it needs.

## Contents
- Step 0: gather ground truth
- Step 1: new page or update existing?
- Step 2: write the page (structure + frontmatter)
- Step 3: place it in navigation
- Step 4: plan the media
- Step 5: validate + PR

## Step 0: Gather ground truth

Don't write from assumptions about how the feature works. Pull the real
behavior first: the PR / spec / changelog entry, the actual UI (labels, the
exact click path), plan/permission gating, and any limits. If a detail isn't
confirmed (a pricing number, which plan includes it, an exact limit), **flag it
for the feature owner — do not guess.** Wrong docs are worse than missing docs.

## Step 1: New page or update existing?

- **Update existing** when the feature changes or extends something already
  documented — edit in place, keeping the URL. Prefer this; it preserves ranking
  and avoids fragmentation.
- **New page** when it's a genuinely new capability with its own search intent.
- **Renaming/replacing** a page = a slug change, which is multi-step (see Step 3).
- Also update **adjacent pages** that reference the changed behavior (grep the
  repo for the feature name / old UI labels) so the corpus stays consistent — a
  stale mention elsewhere is the usual QA miss.

## Step 2: Write the page

Follow the answer-first pattern from `aeo-content.md`:
1. A 40–60 word **direct answer** to the page's core question, first.
2. `## Key takeaways` bullets.
3. **Question-shaped H2/H3** ("How do I …?") matching real queries.
4. Self-contained sections (no orphan pronouns); **tables** for
   settings/plan/option matrices; a grounded FAQ (`<AccordionGroup>`) at the end.
5. `_Updated <Month Year>._` footer if that's the repo's convention.

Frontmatter:
```yaml
---
title: "Query-shaped title (what the user would search)"
description: "One-line SEO summary."
keywords: ["real", "search", "terms"]
---
```
Use Mintlify components where they help — `<Steps>` for sequences, `<Note>`/
`<Warning>` for callouts, `<CodeGroup>` for multi-language code, `<Frame>` for
images. See `references/features.md` for embedding video and the component set.

MDX build trap: a bare `<` before a digit (`<70 words`) breaks the build — write
`&lt;`.

## Step 3: Place it in navigation

A page not added to `docs.json` `navigation` won't appear in the sidebar. Add
the slug to the right group (create a nested accordion group if the section is
getting long). See `references/configuration.md` for the nav shape and the icon
convention.

**If you renamed/replaced a page (slug change):** (1) rename the file, (2) update
the `docs.json` nav reference, (3) add a **redirect** from the old slug to the new
one so the URL never 404s, (4) repoint internal links **and their anchor text**.
Missing any step leaves a broken or misleading link.

## Step 4: Plan the media

New/updated feature docs almost always need fresh visuals. Follow
`references/media-plan.md`: decide which steps need screenshots and whether the
flow warrants a short video, insert greppable placeholders at the exact points,
and produce a capture brief (shot list with file paths + pre-written alt text)
for whoever records/screenshots the product. Keep every fact in text too — never
only in a screenshot or video.

## Step 5: Validate + PR

Run `mint validate`, and `mint broken-links` if you changed links or nav. Open a
PR against `main`. Remember the deploy-branch gotcha: on Starter there's no PR
preview and only the configured branch deploys, so rendering is confirmed after
merge. Before publishing, `grep` for unfilled media placeholders (`MEDIA `,
`📸`, `🎥`) and any `TODO`.

## Example: documenting a new "Scheduled sends" feature

- Ground truth: read the PR; confirm it's on Growth+ plans (flag if unsure).
- Update existing? There's a `sending-videos` page → add a "Schedule a send"
  section there **and** consider a dedicated `schedule-video-sends` page if it
  has its own search intent. Cross-link both.
- Write answer-first: "To schedule a video send, open the campaign, click
  **Schedule**, pick a date and time in the recipient's time zone, and confirm.
  Scheduled sends are available on Growth, Plus, and Scale plans." + Key
  takeaways + "How do I reschedule or cancel a scheduled send?" H2 + FAQ.
- Nav: add the page to the "Sending" group.
- Media brief: screenshot of the Schedule button (M1), the date/time picker
  (M2); a 30–45s video of the full schedule flow (M3) — placeholders inserted,
  shot list with paths + alt text produced.
