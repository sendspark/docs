---
name: docs-authoring
description: >-
  Playbook for creating or updating Mintlify documentation when a feature ships
  or changes — the internal "a release just happened, the docs need to catch up"
  workflow. Use this whenever someone needs to document a new feature, update
  existing docs for a change/upgrade, turn a changelog or release note or PR into
  a doc page, write/refresh a help article, or review a help article someone
  else wrote (including one built in the Mintlify dashboard). It produces a correct,
  answer-first page placed in navigation, plus a plan for the screenshots and
  short video the page needs. Trigger on things like "we shipped X, document it",
  "update the docs for the new release", "write a help article for this feature",
  "the docs are out of date after this change", or "turn this changelog into
  docs" — even without the word "Mintlify". For MOVING onto Mintlify from another
  platform use mintlify-migration; for a site-wide best-practices audit of
  existing docs use mintlify-optimization.
---

# Authoring & updating docs for a release

The internal case: a feature launched or changed, and its documentation needs to
be written or brought up to date — following best practices, placed in
navigation, and shipped with a plan for the visuals it needs.

## Start from ground truth, never assumptions

Before writing, pull how the feature *actually* works: the PR/spec/changelog, the
real UI labels and click path, plan/permission gating, and any limits. If a fact
isn't confirmed — a pricing number, which plan includes it, an exact limit —
**flag it for the feature owner; do not guess.** Wrong docs erode trust more than
missing docs. This matters because docs get cited by AI now: a hallucinated
limit or tier becomes a confidently-wrong answer in ChatGPT.

## The workflow

Full detail in `references/authoring-workflow.md`; the short version:

1. **New page or update existing?** Prefer updating in place (preserves the URL
   and ranking). New page only for genuinely new search intent. Also update
   adjacent pages that mention the changed behavior — grep the repo for the
   feature name / old labels.
2. **Write it answer-first** (`references/aeo-content.md`): a 40–60 word direct
   answer up top, `## Key takeaways`, question-shaped H2/H3, self-contained
   sections, tables for settings/plan matrices, a grounded FAQ. Correct
   frontmatter (`title`, `description`, `keywords`).
3. **Place it in nav** (`references/configuration.md`): add the slug to the right
   `docs.json` group. If you renamed a page, that's a slug change — rename the
   file, update nav, **add a redirect**, and repoint internal links + anchor text.
4. **Plan the media** (`references/media-plan.md`): decide which steps need
   screenshots and whether the flow warrants a short (30–60s) video; insert
   greppable placeholders at the exact insertion points; and produce a **capture
   brief** (shot list with file paths + pre-written alt text) for whoever
   records/screenshots the product. You can't capture product media yourself, so
   the deliverable is the plan + placeholders — and every fact stays in text, not
   only in a screenshot or video.
5. **Validate + PR:** `mint validate` (+ `mint broken-links` on link/nav
   changes), PR against `main`, and grep for unfilled media placeholders before
   publishing.

## Editing in the Mintlify dashboard (no repo, no PR)

The dashboard editor commits straight to `main` and publishes. There is no
`mint validate`, no PR review and no placeholder grep, so run this checklist
yourself before clicking Publish:

- [ ] Search the page for `[Insert`, `TODO`, `📸`, `🎥` and `MEDIA `. Fill or
      remove every hit; placeholder text ships to the live page.
- [ ] Frontmatter has `title`, `description` and `keywords`. Without
      `description`, the page falls back to the generic site-wide meta description.
- [ ] The page opens with a 40–60 word direct answer, then `## Key takeaways`.
- [ ] Every step is written in text. A video embed supports the steps; it never
      replaces them.
- [ ] Plan, limit and pricing claims match the public pricing page and the
      existing docs pages. If unsure, ask the feature owner instead of hedging.
- [ ] The page sits next to its related pages in the sidebar, and at least one
      related page links back to it.
- [ ] Links to other help pages are relative (`/slug`), not full URLs.
- [ ] After publishing, open the live page and read it once.

## Why "answer-first + media brief" is the whole job

A feature doc has two jobs: be **extractable** (so search and AI assistants
quote it correctly — hence answer-first, question headings, facts-in-text) and be
**followable** (so a user completes the task — hence the screenshots and the short
video). Text alone is extractable but hard to follow; media alone is followable
but invisible to extraction. Every page needs both, which is why authoring always
ends with a media plan, not just prose.

## Conventions

- **`mint validate` passing ≠ a feature working** — it silently drops unknown
  `docs.json` keys. Verify config fields against
  `https://leaves.mintlify.com/schema/docs.json`; confirm rendering after deploy.
- **Deploy-branch gotcha:** Starter deploys one configured branch, no PR
  previews — rendering is confirmed post-merge.
- **MDX trap:** bare `<` before a digit breaks the build — use `&lt;`.
- **Repo workflow:** clone, branch off `main`, edit, validate, PR against `main`.
- Mintlify components and video embedding are covered in `references/features.md`.
