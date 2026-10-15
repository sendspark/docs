# Mintlify configuration (docs.json + frontmatter)

Reference for standing up and editing a Mintlify site's config. The governing
principle is in SKILL.md: **verify field names against the real schema
(`https://leaves.mintlify.com/schema/docs.json`) — `mint validate` silently
drops unknown top-level keys**, so a wrong field name "validates" but does
nothing.

## Contents
- Minimum viable docs.json
- Navigation (tabs, groups, nested accordions, icons)
- SEO block
- Page frontmatter
- Verifying a field against the schema

## Minimum viable docs.json

Required keys: `theme`, `name`, `colors.primary`, `navigation`.

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Example Docs",
  "colors": { "primary": "#6140FF", "light": "#AC70FF", "dark": "#432CB2" },
  "favicon": "/favicon.svg",
  "logo": { "light": "/logo/light.svg", "dark": "/logo/dark.svg", "href": "https://example.com" },
  "navigation": { "tabs": [ ... ] }
}
```

Common additions: `background.color` (light/dark), `fonts` (Google font family
names load automatically; custom fonts need a licensed source file — don't ship
a commercial webfont without confirming the license), `appearance.default`.

## Navigation

Structure is `navigation.tabs[] → groups[] → pages[]`. A `pages` entry is either
a page **slug** (string) or a nested **group** object. Nested groups render as
**collapsible accordions** in the sidebar.

```json
"navigation": {
  "tabs": [
    {
      "tab": "Help center",
      "icon": "circle-question",
      "groups": [
        { "group": "Getting started", "icon": "rocket",
          "pages": ["index", "quickstart",
            { "group": "Set up", "pages": ["install", "invite-team"] }] }
      ]
    },
    { "tab": "API reference", "icon": "terminal", "openapi": "api-reference/openapi.json" },
    { "tab": "MCP", "icon": "plug", "groups": [ ... ] }
  ]
}
```

### Icons
- Put an `icon` on each **top-level group** (the sidebar section headings) and on
  each tab. This is the single biggest "looks professional" upgrade and matches
  what strong docs sites (peec.ai, integrate.io) do. Nested accordion groups
  don't need icons — the caret is enough.
- **Icon library gotcha:** Mintlify's default library is **FontAwesome**. If the
  existing tabs use names like `circle-question`, `terminal`, `plug`, you're on
  FontAwesome — use FA-free names (`rocket`, `wand-magic-sparkles`,
  `puzzle-piece`, `gears`, `graduation-cap`, `code`, `life-ring`, `video`,
  `book-open`, `circle-play`, `wrench`). Setting `icons.library: "lucide"`
  switches the whole project and would break FA-only names like
  `circle-question` (Lucide calls it `circle-help`). Pick one library and keep
  names consistent.

### Accordions for large flat lists
If a group has dozens of flat page slugs, break it into themed nested sub-groups.
A 60–80-item flat wall is the thing competitor sites avoid; nested groups make it
scannable. When restructuring nav programmatically, **assert the set of leaf
slugs is unchanged** before/after — dropping a slug silently orphans that page
(it becomes reachable only by URL, not the sidebar).

## SEO block

```json
"seo": {
  "metatags": { "canonical": "https://help.example.com", "description": "..." },
  "indexing": "navigable",
  "organization": { "name": "...", "url": "...", "logo": "...", "sameAs": ["..."] }
}
```

- `indexing: "navigable"` indexes only pages in the nav; `"all"` includes hidden
  pages.
- `seo.organization` enriches the Organization schema Mintlify auto-emits — a
  cheap, high-value structured-data win. Mintlify already auto-emits
  Organization / WebSite / WebPage / ImageObject, so per-page Article JSON-LD is
  usually low ROI.

## Page frontmatter

```yaml
---
title: "Clear, query-shaped title"      # required
description: "One-line SEO summary."
keywords: ["term one", "term two"]
noindex: true          # keep a page reachable but out of the index (offenders)
hidden: true           # remove from sidebar, still reachable by URL
mode: "wide" | "custom" | "center"
---
```

`noindex: true` is the per-page SEO-recovery lever — it keeps a wrong-traffic
page available for support while removing it from search + the sitemap + llms.txt.

## Verifying a field against the schema

Before adding any `docs.json` block you're not 100% sure of:

```bash
curl -s https://leaves.mintlify.com/schema/docs.json > /tmp/mint-schema.json
python3 -c "
import json; s=json.load(open('/tmp/mint-schema.json'))
v=s['anyOf'][0]['properties']              # top-level properties (per-theme variant)
print('top-level keys:', sorted(v.keys()))
print('additionalProperties:', v.get('additionalProperties'))
"
```

The schema is an `anyOf` across themes; inspect the first variant's `properties`.
Sub-objects (`navbar`, `footer`, `integrations.*`) resolve via `$ref` — follow the
pointer to see the exact required sub-fields (e.g. `ga4` requires `measurementId`,
`intercom` requires `appId`). If a key isn't in `properties`, it does not exist —
`mint validate` will still pass, but the feature won't render.
