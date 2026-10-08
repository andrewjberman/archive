"""Check the round-7 fresh-seat run record (TO BF-v-2).

Checks that FRESH_RUN_round7.md has the five `## ` headings in order, that `Final output`
holds a fenced block, and counts outside_writes = entries of `git status --porcelain`
in this worktree outside the deliverables folder. Prints one line:
FRESH-RUN ok=<bool> headings=<n> outside_writes=<n> finished=<yes|no>
"""
import os
import re
import subprocess
import sys

HEADINGS = [
    "Instructions found",
    "Steps run",
    "Final output",
    "Written for the run",
    "Where the instructions fell short",
]
DELIV = "org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~5/"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=here, universal_newlines=True
    ).strip()
    rec = os.path.join(here, "FRESH_RUN_round7.md")
    text = ""
    if os.path.isfile(rec):
        with open(rec, encoding="utf-8") as fh:
            text = fh.read()

    found = re.findall(r"^## (.+?)\s*$", text, flags=re.M)
    # headings present and in order (as a subsequence equal to the five, no extras counted)
    got = [h for h in found if h in HEADINGS]
    headings = len(HEADINGS) if got == HEADINGS else 0

    block = False
    finished = "no"
    m = re.search(r"^## Final output\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if m:
        fm = re.search(r"^```[^\n]*\n(.*?)^```", m.group(1), flags=re.M | re.S)
        if fm:
            block = True
            lines = [ln for ln in fm.group(1).splitlines() if ln.strip()]
            if lines and lines[-1].startswith("ALL-ROOTS ok=True") and "stopped=0" in lines[-1]:
                finished = "yes"

    out = subprocess.check_output(
        ["git", "status", "--porcelain", "-uall"], cwd=root, universal_newlines=True
    )
    outside = 0
    for ln in out.splitlines():
        path = ln[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ")[-1]
        if not path.startswith(DELIV):
            outside += 1

    ok = headings == 5 and block and outside == 0
    print("FRESH-RUN ok=%s headings=%d outside_writes=%d finished=%s" % (ok, headings, outside, finished))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
