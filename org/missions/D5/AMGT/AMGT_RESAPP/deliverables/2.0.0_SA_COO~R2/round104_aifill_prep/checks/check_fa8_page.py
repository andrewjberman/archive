"""check_fa8_page.py -- acceptance for AMGT-fa-8 (the page renders the AI fill: five blocks, source class, citations, machine-written chip).

  python check_fa8_page.py --portal <nested portal worktree> --base <ref>
Runs the cell's own harness `src/pages/SecurityAnalysis/__harness__/aiFill.harness.cjs` (node, from the portal root), requires each named
arm below to print `ARM <name> PASS` and the final line `AIFILL PAGE HARNESS: YES (N of N arms)`, and confirms the branch changed only files
under `src/pages/SecurityAnalysis/` (never package.json, bun.lock or another page) and that the harness is a NEW file.
Prints `AIFILL FA-8 ARMS: YES|NO (k of n)`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

REQUIRED_ARMS = (
    "bio_web_renders_text_chip_links",
    "recent_opal_renders_plain_refs",
    "bio_none_prints_reason",
    "fill_absent_prints_fixed_sentence",
    "fill_invalid_prints_fixed_sentence",
    "fill_missing_prints_fixed_sentence",
    "team_view_beside_gap_only",
    "pillars_beside_gap_only",
    "header_fill_when_empty",
    "header_unchanged_when_held",
    "no_raw_codes_in_visible_text",
)
PAGE_DIR = "src/pages/SecurityAnalysis/"
HARNESS = PAGE_DIR + "__harness__/aiFill.harness.cjs"


def git(portal, *args):
    return subprocess.run(["git", "-C", portal] + list(args), capture_output=True, text=True, timeout=60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal", required=True)
    ap.add_argument("--base", required=True)
    args = ap.parse_args()
    rows = []

    def arm(name, ok, detail=""):
        rows.append((name, ok))
        print("ARM %-52s %s %s" % (name, "PASS" if ok else "FAIL", str(detail)[:200]))

    harness = subprocess.run(["node", HARNESS], cwd=args.portal, capture_output=True, text=True, timeout=300)
    out = harness.stdout
    passed = set(re.findall(r"^ARM (\S+)\s+PASS", out, re.M))
    for name in REQUIRED_ARMS:
        arm("harness arm " + name, name in passed, "" if name in passed else (out[-300:] or harness.stderr[-300:]))
    final = re.findall(r"^AIFILL PAGE HARNESS: YES \((\d+) of (\d+) arms\)", out, re.M)
    arm("harness final line YES with all arms", bool(final) and final[0][0] == final[0][1] and int(final[0][1]) >= len(REQUIRED_ARMS) and harness.returncode == 0, (harness.returncode, out[-120:]))

    diff = git(args.portal, "diff", "--name-status", args.base, "HEAD")
    changed = [ln.split("\t") for ln in diff.stdout.splitlines() if ln.strip()]
    outside = [c[-1] for c in changed if not c[-1].startswith(PAGE_DIR)]
    arm("every changed file is under src/pages/SecurityAnalysis/", diff.returncode == 0 and bool(changed) and not outside, outside or diff.stderr[-120:])
    forbidden = [c[-1] for c in changed if c[-1].endswith(("package.json", "bun.lock", "firmAccess.ts"))]
    arm("no package.json, bun.lock or firmAccess.ts", not forbidden, forbidden)
    added = [c[-1] for c in changed if c[0] == "A"]
    arm("the harness is a new file", HARNESS in added, added)
    deleted = [c[-1] for c in changed if c[0] == "D"]
    arm("no existing file deleted", not deleted, deleted)

    ok = sum(1 for _, v in rows if v)
    print("AIFILL FA-8 ARMS: %s (%d of %d)" % ("YES" if ok == len(rows) else "NO", ok, len(rows)))
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
