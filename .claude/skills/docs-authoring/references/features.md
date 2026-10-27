# Mintlify features that enhance docs

These are the config-level features that make a Mintlify site feel complete and
convert/perform better. All are cheap to add; several have non-obvious gotchas
that this file exists to warn about. Verify every field against the schema first
(see `configuration.md`).

## Contents
- Contextual menu (copy / open in AI)
- Navbar CTAs
- Footer
- Feedback widget (NOT docs.json — read this)
- Integrations / analytics (GA4, PostHog, Intercom Messenger)
- API reference (OpenAPI) — including the public-surface trap
- Freshness, alt text, internal linking

## Contextual menu (copy page / open in AI)

```json
"contextual": { "options": ["copy", "view", "chatgpt", "claude", "perplexity"] }
```

Adds the per-page menu to copy the page as Markdown or open it in an AI
assistant. This is a real **AEO/citation lever** — it makes the page trivially
ingestible by the assistants your users already ask — and it's free. Valid
options include `copy`, `view`, `chatgpt`, `claude`, `perplexity`, `mcp`,
`cursor`, `vscode`, and more. Optional `display: "header" | "toc"`.

## Navbar CTAs

```json
"navbar": {
  "links": [{ "label": "Sign in", "href": "https://app.example.com" }],
  "primary": { "type": "button", "label": "Start free", "href": "https://www.example.com" }
}
```

High-traffic docs with no link back to the app leak a funnel. A secondary
"Sign in" link + a primary CTA button is the standard pattern. Link `type` for
`links[]`: omit for a plain link, `"github"` for a repo star count, `"discord"`
for online count. `primary.type` is `button` / `github` / `discord`. Verify the
CTA destinations actually resolve (don't ship a 404 in the navbar).

## Footer

```json
"footer": {
  "socials": { "linkedin": "https://www.linkedin.com/company/example/" },
  "links": [{ "header": "Product", "items": [{ "label": "Pricing", "href": "..." }] }]
}
```

Valid social keys are a fixed set (`x`, `linkedin`, `github`, `youtube`,
`slack`, `discord`, `website`, …). Match footer socials to the org's real
profiles (the `seo.organization.sameAs` list is a good source of truth).

## Feedback widget — this is NOT a docs.json block in v4

The single biggest config gotcha. The old v3 shape:

```json
"feedback": { "thumbsRating": true, "suggestEdit": true, "raiseIssue": true }   // ❌ v3 — silently ignored in v4
```

…is **not a valid v4 key**. `mint validate` passes (it drops the unknown key),
but nothing renders. In **Mintlify v4 the feedback widget is a dashboard
Add-ons toggle** (app.mintlify.com/products/addons):
- **Thumbs rating** — available on all plans.
- **Edit suggestions** and **Raise issues** — work **only for a public GitHub
  repo** (they open a PR / issue). If the docs repo is public, enable them.
- **Contextual free-form feedback** — Enterprise only.

So: don't put `feedback` in `docs.json`. Tell the owner to toggle it in the
dashboard, and note the public-repo requirement for the last two.

## Integrations / analytics

```json
"integrations": {
  "ga4": { "measurementId": "G-XXXXXXXXXX" },
  "posthog": { "apiKey": "phc_xxx", "apiHost": "https://us.posthog.com" },
  "intercom": { "appId": "xxxxxxx" }
}
```

- Keys here are **public client-side IDs** — safe in `docs.json`, not secrets.
  You can usually pull the real IDs from the org's live marketing site (they're
  already in its client HTML). Confirm the sub-field name against the schema:
  `ga4.measurementId`, `intercom.appId` — both required, both
  `additionalProperties: false`.
- **Reuse vs. dedicated property:** pointing docs at the existing GA4/PostHog
  property mixes docs traffic into the main dashboards. Fine for a quick start;
  flag it so the owner can spin up a dedicated property later if they want
  segmentation.
- **Intercom Messenger** (`integrations.intercom`) is the chat-bubble
  **Messenger** — a *separate product* from Intercom **Articles** (the KB you may
  have just migrated off). Adding the Messenger does **not** undo the migration
  or affect indexing. It's the free alternative to a paid Mintlify AI assistant —
  **don't run both** (two chat bubbles). Pick one.

## API reference (OpenAPI) — and the public-surface trap

Add a tab with `"openapi": "api-reference/openapi.json"`. Requirements + the trap:

- **OpenAPI 3.0/3.1 required.** If the source is Swagger 2.0, convert
  (body params → `requestBody`, `#/definitions/` → `#/components/schemas/`,
  responses `schema` → `content`).
- **Filter the public surface by AUTH STRATEGY, not by tag/group.** This is the
  expensive lesson. A spec filtered by Swagger tag/group will expose endpoints
  that are *not actually callable by an external API key* — internal
  session-only routes, `auth:false` webhook receivers, OAuth callbacks, billing
  internals. Group membership is a *different axis* from "is this reachable via
  the public gateway with an API key." The objective test is whether the route
  declares the public auth strategy (e.g. an `x-api-key` + `x-api-secret` scheme
  / a `public-api-strategy` in the API's route config). Only those belong in the
  public reference. Determining that requires the API's route configs (or a
  developer who knows them) — the Swagger alone usually can't tell you, so this
  is a developer/security sign-off, not something to infer.
- **Publishing an endpoint is a security decision, not a typo.** When unsure
  whether an endpoint (especially a destructive `DELETE`, key-management, or
  billing route) should be public, do not include it on your own judgment — get
  a developer to confirm against the code. Sourcing endpoint definitions from an
  internal/undocumented spec and publishing them is exactly the thing to pause on.
- **Prune ruthlessly:** drop schemas not referenced by the kept operations and
  any orphaned `x-alt-definitions`; the result should be valid OpenAPI 3.x with
  **0 dangling `$refs`**. (A real cut went 198→23 ops and 744→93 schemas.)
- **Durable fix:** rather than hand-filtering each release, have the API emit a
  dedicated public spec (tag public routes at the source, e.g. `x-public: true`,
  serve a filtered spec, point `docs.json` at its URL). Hand-filtering drifts and
  risks re-leaking internal endpoints.
- Interactive playground: configure under `api.playground`.

## Freshness, alt text, internal linking

- **Freshness is a verified AEO lever** — AI-cited content skews ~25% fresher,
  and assistants favor recently-updated pages. But **cosmetic date bumps don't
  work** (Google penalized date-only edits in Dec 2025). Refreshes must be
  substantive (a new example, data point, or FAQ per major section). Automate as
  a monthly routine over the top-N pages by impressions.
- **Alt text on every image** — accessibility *and* AEO (assistants extract from
  alt text; facts shouldn't live only inside screenshots). If images are
  committed locally, write alt vision-accurately by reading the actual file.
- **Internal "related articles" links** — findability + crawl. Additive,
  sibling-based; avoid spammy/irrelevant links. Cuts orphan pages.
