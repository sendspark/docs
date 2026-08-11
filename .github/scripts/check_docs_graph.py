#!/usr/bin/env python3
"""Link-graph checks that `mint validate` does not perform.

Two failures this catches, both of which reached production before it existed:

1. A page file that no navigation group references. It still deploys and still
   answers on its URL, but nothing in the sidebar leads to it. `untitled-page`
   sat live this way, indexable, holding a video and no text.

2. A page nothing links to. `mint broken-links` only checks that links point
   somewhere real, never that a page is reachable, so a new guide can ship with
   no route in except the sidebar.

Check 2 runs as a ratchet against orphan-baseline.txt: the known backlog is
allowed, anything new fails. Fixing a baseline entry is reported, not punished,
so the baseline shrinks over time and never silently grows.
"""

import json
import os
import re
import sys

DOCS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = os.path.join(DOCS, ".github", "orphan-baseline.txt")

# Pages that are legitimately unreachable from a navigation group.
NAV_EXEMPT = {"index"}  # the site root, rendered by the landing tab itself

# Pages that cannot meaningfully carry inbound content links. The site root is
# reached through the logo and the navigation chrome, never through prose, so
# counting it as an orphan is noise rather than a finding.
ORPHAN_EXEMPT = {"index"}

# ]( /slug ) — internal links only, ignoring anchors, queries and externals.
LINK = re.compile(r"\]\(/([a-z0-9][a-z0-9\-]*)")


def slugs():
    return {f[:-4] for f in os.listdir(DOCS) if f.endswith(".mdx")}


def nav_pages(node, found):
    """Collect every string in the navigation subtree. Structure varies by
    Mintlify version (tabs, groups, dropdowns, nested groups), so recurse over
    everything rather than assuming a shape."""
    if isinstance(node, str):
        found.add(node.lstrip("/"))
    elif isinstance(node, list):
        for item in node:
            nav_pages(item, found)
    elif isinstance(node, dict):
        for value in node.values():
            nav_pages(value, found)
    return found


def inbound_counts(all_slugs):
    counts = {s: 0 for s in all_slugs}
    for f in os.listdir(DOCS):
        if not f.endswith(".mdx"):
            continue
        src = f[:-4]
        with open(os.path.join(DOCS, f), encoding="utf-8") as fh:
            for target in LINK.findall(fh.read()):
                # Self-links do not make a page reachable.
                if target in counts and target != src:
                    counts[target] += 1
    return counts


def main():
    all_slugs = slugs()
    with open(os.path.join(DOCS, "docs.json"), encoding="utf-8") as fh:
        config = json.load(fh)
    in_nav = nav_pages(config.get("navigation", {}), set()) & all_slugs

    failures = []

    missing_from_nav = sorted(all_slugs - in_nav - NAV_EXEMPT)
    if missing_from_nav:
        failures.append(
            "These page files are in the repo but no navigation group references them.\n"
            "They will deploy and be reachable by URL while being invisible in the sidebar.\n"
            "Add each to docs.json, or delete the file and add a redirect:\n"
            + "\n".join(f"  - {s}" for s in missing_from_nav)
        )

    counts = inbound_counts(all_slugs)
    orphans = {s for s in in_nav if counts[s] == 0} - ORPHAN_EXEMPT

    baseline = set()
    if os.path.exists(BASELINE):
        with open(BASELINE, encoding="utf-8") as fh:
            baseline = {
                line.strip()
                for line in fh
                if line.strip() and not line.startswith("#")
            }

    new_orphans = sorted(orphans - baseline)
    if new_orphans:
        failures.append(
            "These pages have no inbound internal links, so nothing routes to them.\n"
            "Add a contextual link from a topically adjacent page, or a Related articles entry:\n"
            + "\n".join(f"  - {s}" for s in new_orphans)
        )

    fixed = sorted(baseline - orphans - (baseline - all_slugs))
    stale = sorted(baseline - all_slugs)

    print(f"pages: {len(all_slugs)}   in nav: {len(in_nav)}   orphans: {len(orphans)}")
    print(f"baseline: {len(baseline)}   new orphans: {len(new_orphans)}")
    if fixed:
        print(f"\nNo longer orphaned ({len(fixed)}). Remove from orphan-baseline.txt:")
        for s in fixed:
            print(f"  - {s}")
    if stale:
        print(f"\nIn baseline but no longer a page ({len(stale)}). Remove these too:")
        for s in stale:
            print(f"  - {s}")

    if failures:
        print("\n" + "\n\n".join(failures), file=sys.stderr)
        return 1

    print("\nOK: every page is in navigation, and no new orphans.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
