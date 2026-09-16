"""OG-q-2 probes (NFRA_OPLGTW, TO-OG-q-2, worker 0.9.0_WK_NFRA_OPLGTW~5).

    python og_q2.py AC26 [cut-base]

AC26 (discriminating): the diff of infra/aws/ec2/opal-gateway/app/data_entitlement.py against the cut base
(default 0fc7c71160, the commit the worktree was cut from) must be EXACTLY five added lines and no removed line, each
added line naming one contract tool (org/standards/NFRA_OPLGTW_CONTRACT.json `tools`) once, with an operation class from
the contract's `operations`. The diff is read from git (worktree against the base), never from this worker's account of
what it changed. Prints each tool with the class its added line gives it, the denominator, and one verdict line.
Exit 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
TARGET = "infra/aws/ec2/opal-gateway/app/data_entitlement.py"
CONTRACT = ROOT / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
DEFAULT_BASE = "0fc7c71160"


def ac26(base: str) -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    tools, operations = contract["tools"], contract["operations"]
    out = subprocess.run(["git", "-C", str(ROOT), "diff", "--no-color", "-U0", base, "--", TARGET],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        print("git diff rc=%d: %s" % (out.returncode, out.stderr.strip()[:300]))
        print("VERDICT: FAIL-OGQ2-AC26 the diff could not be read")
        return 1
    added = [ln[1:] for ln in out.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in out.stdout.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    print("diff %s..worktree -- %s: %d added line(s), %d removed line(s)" % (base, TARGET, len(added), len(removed)))
    seen = {}
    reasons = []
    for line in added:
        named = [t for t in tools if re.search(r"[\"']%s[\"']" % re.escape(t), line)]
        classes = [o for o in operations if re.search(r"[\"']%s[\"']" % re.escape(o), line)]
        print("  + %s" % line.strip())
        if len(named) != 1 or len(classes) != 1:
            reasons.append("an added line does not name exactly one contract tool with one contract operation class")
            continue
        if named[0] in seen:
            reasons.append("tool %s is added twice" % named[0])
        seen[named[0]] = classes[0]
    for line in removed:
        print("  - %s" % line.strip())
    for tool in tools:
        print("tool %-26s class %s" % (tool, seen.get(tool, "<no added entry>")))
    print("denominator: %d of %d contract tools carry an added entry; %d added and %d removed lines"
          % (len(seen), len(tools), len(added), len(removed)))
    if len(added) != len(tools):
        reasons.append("%d added lines, expected exactly %d" % (len(added), len(tools)))
    if removed:
        reasons.append("%d removed line(s), expected none" % len(removed))
    if set(seen) != set(tools):
        reasons.append("%d of %d contract tools have an added entry" % (len(seen), len(tools)))
    if reasons:
        print("VERDICT: FAIL-OGQ2-AC26 %s" % "; ".join(dict.fromkeys(reasons)))
        return 1
    print("VERDICT: PASS-OGQ2-AC26")
    return 0


def main(argv) -> int:
    if len(argv) < 2 or argv[1] != "AC26":
        print("usage: og_q2.py AC26 [cut-base]")
        return 2
    return ac26(argv[2] if len(argv) > 2 else DEFAULT_BASE)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
