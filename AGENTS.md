# Instructions for anyone writing or editing these docs

This repo is the Sendspark Help Center, published at help.sendspark.com by
Mintlify. These instructions apply to people and AI agents alike.

## Use the docs-authoring skill

Before you create, update or review any page, follow the **docs-authoring**
skill: `.claude/skills/docs-authoring/SKILL.md` and its `references/` folder.

- Claude Code loads it automatically from this repo.
- Other agents (Codex, Cursor, Mintlify's agent): read `SKILL.md` and the
  reference file for the step you are on before you write anything.
- People: read `SKILL.md` once. If you edit in the Mintlify dashboard, run its
  "Editing in the Mintlify dashboard" checklist before every publish.

## Rules that are never optional

1. **Ground truth, never guesses.** Plan names, limits, prices and UI labels
   come from the product, the public pricing page (sendspark.com/pricing) or an
   existing docs page. If you can't confirm a fact, ask the feature owner. Don't
   hedge it ("may require...") and don't make it up.
2. **Answer first.** Open with a 40–60 word direct answer, then
   `## Key takeaways`, then question-shaped headings, then an FAQ.
3. **Frontmatter on every page:** `title`, `description`, `keywords`.
4. **Steps live in text.** Videos and screenshots support the steps; they never
   replace them. Every image needs descriptive alt text.
5. **No placeholders on `main`.** `main` deploys straight to production. Nothing
   like `[Insert ...]`, `TODO`, `📸`, `🎥` or `MEDIA ` may be merged or published.
6. **Navigation and links.** Every page must be in a `docs.json` navigation
   group, next to its related pages, and at least one related page must link to
   it. Use relative links (`/slug`), not full URLs. Renaming a page means a
   redirect in `docs.json`.
7. **MDX trap:** a bare `<` before a digit breaks the build. Write `&lt;`.

## Checks that run on every PR and push to `main`

`.github/workflows/docs-checks.yml` runs `mint validate`, `mint broken-links`,
the page-graph check (navigation coverage and the orphan ratchet) and the prose
and alt-text check. Run them locally before opening a PR:

```bash
mint validate && mint broken-links
python3 .github/scripts/check_docs_graph.py
python3 .github/scripts/check_prose_defects.py
```

Dashboard edits commit straight to `main`, so these checks only run after the
page is already live. That is why the dashboard checklist exists.
