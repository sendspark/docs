#!/usr/bin/env python3
"""Prose and alt-text checks that no build tool performs.

Every check here exists because the defect it catches was found live, at scale,
by a screenshot-versus-prose audit of the whole corpus. `mint validate` builds
these pages happily, `mint broken-links` finds every link resolvable, and the
page graph is clean. The defects are invisible to all three.

1. Stray '#' before a merge tag. An MDX-migration artifact: 27 runs of three to
   nine '#' sat immediately before merge tags across 10 files, inside snippets
   the docs tell readers to copy. Anyone who copied one sent literal hashes into
   their sequence.

2. Bare CTA lines. Eight pages carried a line reading exactly "Install Chrome
   Extension" -- dead text where a button used to be, with no link and no
   target. It renders as an orphan sentence mid-page.

3. One image, two descriptions. The single most damaged layer in this corpus is
   alt text, because it was written from the adjacent prose rather than from the
   image. The clearest symptom is mechanical and cheap to detect: the same image
   file described differently on different pages, or on the same page. One image
   was used seven times on one page with seven different language claims, while
   containing nothing language-specific at all.

Check 3 runs as a ratchet against alt-conflict-baseline.txt, matching the
convention in check_docs_graph.py: a known backlog is allowed, anything new
fails, and fixing a baseline entry is reported rather than punished.
"""

import collections
import os
import re
import sys

DOCS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = os.path.join(DOCS, ".github", "alt-conflict-baseline.txt")

# Three or more '#' immediately before a merge tag opener, in either the raw or
# the HTML-escaped form MDX leaves behind. A markdown heading is '#' plus a
# space at line start, so it can never match this.
STRAY_HASH = re.compile(r"#{3,}(?=&#123;&#123;|\{\{)")

# A line that is nothing but a call-to-action label. These are all remnants of
# buttons lost in the CMS migration.
BARE_CTA = re.compile(r"^(?:Install(?: the)?(?: Sendspark)? Chrome Extension)\s*$", re.M)

MD_IMAGE = re.compile(r"!\[([^\]]*)\]\((/images/[^)\s]+)\)")
HTML_IMAGE = re.compile(r'<img\s+[^>]*src="(/images/[^"]+)"[^>]*alt="([^"]*)"')


def pages():
    for name in sorted(os.listdir(DOCS)):
        if name.endswith(".mdx"):
            path = os.path.join(DOCS, name)
            with open(path, encoding="utf-8") as fh:
                yield name, fh.read()


def load_baseline():
    if not os.path.exists(BASELINE):
        return set()
    with open(BASELINE, encoding="utf-8") as fh:
        return {
            line.strip()
            for line in fh
            if line.strip() and not line.lstrip().startswith("#")
        }


def main():
    failures = []
    stray, bare = [], []
    alts = collections.defaultdict(set)

    for name, text in pages():
        for match in STRAY_HASH.finditer(text):
            stray.append(f"{name}:{text.count(chr(10), 0, match.start()) + 1}")
        for match in BARE_CTA.finditer(text):
            bare.append(f"{name}:{text.count(chr(10), 0, match.start()) + 1}")
        for alt, src in MD_IMAGE.findall(text):
            alts[src].add(alt.strip())
        for src, alt in HTML_IMAGE.findall(text):
            alts[src].add(alt.strip())

    if stray:
        failures.append(
            "Stray '#' before a merge tag ({}). Readers copy these snippets "
            "verbatim, so the hashes end up in their sequences:\n".format(len(stray))
            + "\n".join(f"  {s}" for s in stray)
        )

    if bare:
        failures.append(
            "Bare CTA line with no link ({}). Renders as dead text mid-page:\n".format(
                len(bare)
            )
            + "\n".join(f"  {s}" for s in bare)
        )

    baseline = load_baseline()
    conflicts = {src for src, seen in alts.items() if len(seen) > 1}
    new = sorted(conflicts - baseline)
    fixed = sorted(baseline - conflicts)

    if new:
        detail = []
        for src in new:
            detail.append(f"  {src}")
            for alt in sorted(alts[src]):
                detail.append(f"      {alt or '(empty)'}")
        failures.append(
            "One image, more than one description ({}). Same pixels, so the "
            "descriptions cannot both be right -- and an alt that disagrees with "
            "another page's is usually one written from the prose rather than "
            "from the image:\n".format(len(new)) + "\n".join(detail)
        )

    print(f"pages: {sum(1 for _ in pages())}   alt-conflict baseline: {len(baseline)}")
    if fixed:
        print(
            f"\nNo longer conflicting ({len(fixed)}). "
            "Remove from alt-conflict-baseline.txt:"
        )
        for src in fixed:
            print(f"  - {src}")

    if failures:
        print("\n" + "\n\n".join(failures), file=sys.stderr)
        return 1

    print("\nOK: no stray merge-tag hashes, no bare CTA lines, no conflicting alt text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
