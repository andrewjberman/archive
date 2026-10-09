"""GS-h-1 AC1 (FWD-8; ROUND_ANALYSIS.round3 ADDENDUM 1): the attribution replay of the census's 26 owned-paths refusals.

Reads `org/missions/D0/NFRA/NFRA_GATSCP/deliverables/0.9.0_WK_NFRA_GATSCP~14/OWNED_PATHS_REPLAY_round4.json`: a list of objects
{"block_line": int, "author": str, "paths": [str], "tie": "OWN-PATH"|"OTHER-ACT"|"UNATTRIBUTED", "commit": hex or null,
 "evidence": str}. Every claim is re-measured here, never trusted:
Arm 1: exactly 26 entries, distinct block lines, each a BLOCK line of org/git-author-override-audit.log naming that author.
Arm 2: every OWN-PATH entry names a commit that exists, is authored by that author, and carries at least one of the entry's paths.
Arm 3: every OTHER-ACT entry names a commit that exists and carries none of the entry's paths; UNATTRIBUTED entries name no commit.
The counts per tie are printed; they are the CTO's to read.
"""
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT  # noqa: E402

REPORT = os.path.join(ROOT, "org/missions/D0/NFRA/NFRA_GATSCP/deliverables/0.9.0_WK_NFRA_GATSCP~14/OWNED_PATHS_REPLAY_round4.json")
LOG = os.path.join(ROOT, "org/git-author-override-audit.log")


def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, encoding="utf-8", errors="replace")


entries = []
if os.path.exists(REPORT):
    try:
        entries = json.load(open(REPORT, encoding="utf-8"))
    except ValueError:
        entries = []
log = open(LOG, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(LOG) else []
ok1 = len(entries) == 26 and len({e.get("block_line") for e in entries}) == 26
bad1 = []
for e in entries:
    n = e.get("block_line")
    line = log[n - 1] if isinstance(n, int) and 0 < n <= len(log) else ""
    if " BLOCK " not in line or str(e.get("author", "")) not in line:
        bad1.append(n)
ok1 = ok1 and not bad1
bad2, bad3, counts = [], [], {}
for e in entries:
    tie, c, paths = e.get("tie"), e.get("commit"), e.get("paths") or []
    counts[tie] = counts.get(tie, 0) + 1
    if tie in ("OWN-PATH", "OTHER-ACT"):
        exists = bool(c) and git("cat-file", "-e", "%s^{commit}" % c).returncode == 0
        files = set(git("show", "--name-only", "--format=", c).stdout.split()) if exists else set()
        author = git("log", "-1", "--format=%an", c).stdout.strip() if exists else ""
        if tie == "OWN-PATH" and not (exists and author == e.get("author") and files & set(paths)):
            bad2.append(e.get("block_line"))
        if tie == "OTHER-ACT" and not (exists and not (files & set(paths))):
            bad3.append(e.get("block_line"))
    elif tie == "UNATTRIBUTED":
        if c:
            bad3.append(e.get("block_line"))
    else:
        bad3.append(e.get("block_line"))
arms = [
    ("26-distinct-block-lines", ok1, "report=%s entries=%d unmatched_lines=%s" % (os.path.exists(REPORT), len(entries), bad1[:5])),
    ("own-path-ties-measured", bool(entries) and not bad2, "bad=%s" % bad2[:5]),
    ("other-act-and-unattributed-honest", bool(entries) and not bad3, "bad=%s counts=%s" % (bad3[:5], counts)),
]
for name, ok, detail in arms:
    print("  %s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
bad = sum(1 for a in arms if not a[1])
print("GS-H1-REPLAY ok=%s arms=%d failed=%d" % (bad == 0, len(arms), bad))
sys.exit(0 if bad == 0 else 1)
