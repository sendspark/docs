# Sendspark Help Center

Mintlify documentation served at **help.sendspark.com**, migrated from Intercom (419 articles).

- Preview locally: `mint dev`
- Validate build: `mint validate`
- Redirects from old Intercom URLs (`/en/articles/{id}-*`) are configured in `docs.json`.

Tracked in Linear: **Sendspark Docs: Intercom → Mintlify Migration**.

## Writing or editing docs

Read [`AGENTS.md`](AGENTS.md) first. It applies to people and AI agents alike.

Every page is written with the **docs-authoring** skill in
[`.claude/skills/docs-authoring/`](.claude/skills/docs-authoring/SKILL.md):
answer-first structure, facts confirmed against the product and pricing page,
frontmatter, navigation placement and a media plan. Claude Code picks it up
automatically in this repo. It is also shared on claude.ai as an org skill, and
this repo copy is the source of truth: change it here, then re-upload it.

**Editing in the Mintlify dashboard?** The dashboard commits straight to `main`,
which deploys to production with no PR and no checks. Run the "Editing in the
Mintlify dashboard" checklist in the skill before every publish.

Where each tool reads its instructions:

| Tool | Reads |
|---|---|
| Claude Code | `CLAUDE.md` (imports `AGENTS.md`) + `.claude/skills/` |
| Codex, Cursor, other agents | `AGENTS.md` |
| Mintlify agent (Slack/API) | `.mintlify/AGENTS.md` (a copy of `AGENTS.md`; CI fails if they differ) |
| Mintlify dashboard editor AI | Editor settings → AI instructions (set in the dashboard, not in this repo) |
