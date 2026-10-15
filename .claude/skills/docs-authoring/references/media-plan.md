# Planning videos and screenshots for docs

Docs that are pure text underperform — users need visual proof of where to click
and what a screen looks like, and screenshots/videos raise trust and completion.
But **you (the model) cannot record a product video or take a live product
screenshot.** So your job is two-fold:

1. **Place media correctly** in the page (and don't let facts live *only* in
   media — see the AEO caveat below).
2. **Produce a precise capture brief** a human executes — with the exact shot,
   a suggested file path, and **pre-written alt text** — plus greppable
   placeholders in the MDX so nothing ships half-done.

## Deciding what needs media

**Screenshot** — capture the decision points and non-obvious UI, not every
trivial step:
- Any step that names a button, menu, toggle, or field → show where it is.
- Settings/configuration panels, integration connection screens.
- Before/after or empty-vs-filled states; success/confirmation states.
- Anything a user could plausibly get lost on.
- Skip: trivial steps ("click Save"), or repeating a screen already shown.

**Video** — reserve for motion and end-to-end flow:
- Getting-started / setup / integration walkthroughs.
- Flows with more than ~4 UI steps, or where sequence/timing matters.
- Keep each video short and single-purpose (roughly 30–60s, one job). Chapter
  longer ones. A wall of 5-minute videos is worse than none.
- If the org makes video software, dogfood it (e.g. record and embed with the
  product's own share link).

## Placing media in the page

- **Media supports text; it never replaces it.** A number, a setting value, or a
  step that exists *only* inside a screenshot or video is invisible to search and
  AI extraction (bad for AEO and accessibility). Always keep the fact in text and
  use the image/video as reinforcement.
- Put a screenshot **immediately after the step it illustrates.**
- Use the `<Frame>` component for a bordered, optionally captioned image:
  ```mdx
  <Frame caption="The Integrations tab in Workspace settings">
    ![Integrations settings tab with the Connect button highlighted](/images/connect-hubspot/02-integrations-tab.png)
  </Frame>
  ```
- Embed video once recorded via the video embed / `<iframe>` (or the product's
  embed). Add a transcript or captions where possible — the video's words become
  extractable text (AEO).

## The capture brief (shot list)

Produce this as part of your output so a human can execute it without re-deriving
anything. One row per asset:

| ID | Type | Page → insertion point | What to capture | File path | Alt text (pre-written) |
|----|------|------------------------|-----------------|-----------|------------------------|
| M1 | screenshot | `connect-hubspot` → after step 2 | The Integrations tab, "Connect" button highlighted | `/images/connect-hubspot/02-integrations-tab.png` | "Integrations settings tab with the Connect button highlighted" |
| M2 | video | `connect-hubspot` → top, under the intro | 30–45s: full connect flow from Settings → authorize → confirmation | `/images/connect-hubspot/walkthrough.mp4` (or embed URL) | n/a (provide captions/transcript) |

Conventions:
- **File path:** `/images/<page-slug>/NN-short-description.png`, numbered in page
  order so the folder reads top-to-bottom.
- **Alt text written now:** factual description of what's shown (not "screenshot
  of X"). This is what accessibility tools read and what AI extracts, so it's
  worth writing even before the image exists.

## Placeholders that keep the build green

Don't insert a `<Frame>` pointing at a not-yet-existing image — a missing asset
can fail the build or render broken. Instead drop a **greppable MDX comment** at
the exact insertion point, so the page is complete except the binary and a human
(or `grep`) can find every open item:

```mdx
{/* 📸 MEDIA M1 — screenshot: Integrations tab, Connect highlighted → /images/connect-hubspot/02-integrations-tab.png */}
```

```mdx
{/* 🎥 MEDIA M2 — video: 30-45s connect walkthrough → /images/connect-hubspot/walkthrough.mp4 */}
```

When the asset lands, replace the comment with the real `<Frame>`/embed using the
path and alt text from the brief. Before publishing, `grep -rn "MEDIA M"` (or
`📸`/`🎥`) to confirm none remain unfilled.

## Existing images

While you're in a page, check that **every existing image has descriptive alt
text** (`![](...)` with empty alt is an a11y + AEO miss). Fill any blanks —
accurately, by looking at what the image actually shows if it's available locally.
