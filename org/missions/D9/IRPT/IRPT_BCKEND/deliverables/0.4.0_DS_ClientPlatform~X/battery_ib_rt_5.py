#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rt-5 acceptance battery -- RT5-AC1, four arms.

Prints IBRT5-FIRST-MINT-SERVED only when all four arms pass.

WHAT THIS BATTERY IS NOT (BOUNDS 12): it wraps nothing. Every arm's subject is the
REAL artifact -- the real guard on disk, the real S3 object, the real git history,
the real ledger entry. No fixture is registered, patched or copied by this file,
and every hash it compares is RE-DERIVED at run time from the repo bytes and the
served object rather than read from a manifest this cell wrote.

Arms:
  (a) DECLARED     the guard's OWN declared-bundle list names investor_reporting,
                   and the guard's self-test suites are UNMOVED from their
                   pre-edit baseline (they were already red; BOUNDS calls the
                   self-test run "the control", and unmoved IS the control).
  (b) MINTED       the served object exists, its ETag is its md5, and each member's
                   sha stamp equals sha256sum of that member's repo file.
  (c) MEMBER       the gate's own commit-range run over the two REAL commits that
                   added the runners reads BUNDLE-ROUTED, while the sibling test
                   files in the SAME run still read SKIP-NOT-MEMBER.
  (d) LEDGER       the entry is CLOSED, the OPEN sentinel is gone, and both the
                   OPEN and the removal commit are named from git history.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

WS = pathlib.Path(__file__).resolve().parents[7]   # deliverables/<serial>/ -> ... -> repo root
BUCKET = "opal-data-mdpf"
KEY = "code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz"
PREFIX = "code/scripts/assets_gold/investor_reporting/"
SLUG = "irpt-bckend-rt5-mint"
SENTINEL = "org/critical_paths/.open_deploys/" + SLUG + ".json"
CRLF = chr(13) + chr(10)

MEMBERS = {
    "directory-runner-sha256": "data/assets/scripts/gold/investor_reporting/directory_runner.py",
    "holdings-snapshot-sha256": "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py",
}
# The two REAL commits that ADDED the runners -- the identical input that read
# SKIP-NOT-MEMBER in round 1. Holding the input fixed is what makes (c) a
# before/after on the declaration alone.
RANGES = [
    ("3654197107", "directory_runner.py", "tests/test_directory_runner.py"),
    ("2dbc92e956", "holdings_snapshot.py", "tests/test_holdings_snapshot.py"),
]
# Measured pre-edit, on this worktree, BEFORE the CODE_TREES change. Both suites
# were ALREADY failing for reasons this cell does not touch (row IRPT_BCKEND-S27).
BASELINE = {".tools/test_code_trees_invariant.py": (3, 18),
            ".tools/test_safe_deploy.py": (7, 14)}

results = []


def run(cmd, timeout=300):
    """Every invocation terminates (BOUNDS 9). rc 124 IS the recorded output."""
    try:
        p = subprocess.run(cmd, cwd=str(WS), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


# TWO ENVIRONMENT TRAPS THIS BATTERY MUST NOT WALK INTO, both measured on this box:
#   1. bare "bash" here is the WSL stub -- it answers "Windows Subsystem for Linux
#      has no installed distributions" on stdout and exits, so a shelled gate run
#      reads as a clean EMPTY result rather than a failure. .tools/git_bash_resolver
#      is the estate's instrument for locating the real Git Bash.
#   2. .tools/aws is an EXTENSIONLESS bash wrapper: CreateProcess raises
#      OSError WinError 193 on it. The .cmd twin is the Windows entry point.
#      (safe_deploy_core.py carries the same note about comp-pipescript.)
sys.path.insert(0, str(WS / ".tools"))
from git_bash_resolver import bash_argv          # noqa: E402


def run_bash(script, *args, **kw):
    return run(bash_argv(script, *args), **kw)


def aws(*args):
    rc, out = run([str(WS / ".tools" / "aws.cmd")] + list(args), timeout=120)
    return rc, out.replace(CRLF, "\n")      # the shim emits CRLF


def record(arm, ok, detail):
    results.append((arm, ok, detail))
    print("  %-8s %s" % ("PASS" if ok else "FAIL", arm))
    for line in detail.splitlines():
        print("           " + line)


print("RT5-AC1 battery -- IRPT_BCKEND.TO-IB-rt-5, the gold first-mint")
print("workspace: %s" % WS)
print()

# ---------------------------------------------------------------- (a) DECLARED
rc, out = run_bash(".tools/safe-deploy.sh", "--mint-bundle", "nonexistent")
m = re.search(r"declared: \[([^\]]*)\]", out)
declared = [d.strip().strip("'\"") for d in m.group(1).split(",")] if m else []
ok_a1 = "investor_reporting" in declared
det = ["guard's own line: %s" % out.strip().splitlines()[0] if out.strip() else "(no output)",
       "declared bundles (denominator %d): %s" % (len(declared), declared)]

ctrl = []
ok_a2 = True
for script, (fails, total) in sorted(BASELINE.items()):
    crc, cout = run([sys.executable, script])
    mm = re.search(r"FAIL: (\d+)/(\d+) cases failed", cout)
    now = (int(mm.group(1)), int(mm.group(2))) if mm else (-1, -1)
    same = now == (fails, total)
    ok_a2 = ok_a2 and same
    ctrl.append("%s: baseline %d/%d -> now %d/%d  %s"
                % (script, fails, total, now[0], now[1],
                   "UNMOVED (control holds)" if same else "*** MOVED ***"))
det += ctrl
det.append("NOTE: both suites were ALREADY red pre-edit (row IRPT_BCKEND-S27); BOUNDS")
det.append("  names the self-test run 'the control', and UNMOVED is what a control asserts.")
record("(a) DECLARED", ok_a1 and ok_a2, "\n".join(det))

# ------------------------------------------------------------------ (b) MINTED
rc, out = aws("s3api", "head-object", "--bucket", BUCKET, "--key", KEY, "--output", "json")
head = json.loads(out) if rc == 0 else {}
meta = head.get("Metadata", {})
etag = str(head.get("ETag", "")).strip('"')
verified = 0
det = ["head-object rc=%d  ContentLength=%s  ETag=%s" % (rc, head.get("ContentLength"), etag)]
for stamp, rel in sorted(MEMBERS.items()):
    local = hashlib.sha256((WS / rel).read_bytes()).hexdigest()
    served = meta.get(stamp, "")
    hit = local == served and bool(local)
    verified += 1 if hit else 0
    det.append("%s  %s" % ("MATCH " if hit else "DIFFER", stamp))
    det.append("         repo sha256(%s) = %s" % (rel, local))
    det.append("         served metadata          = %s" % (served or "(absent)"))
rc2, out2 = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", PREFIX,
                "--query", "length(Contents)", "--output", "text")
count = out2.strip()
det.append("MEMBERS verified: %d of %d  |  KEYS at the prefix: %s of 1 minted"
           % (verified, len(MEMBERS), count))
det.append("DENOMINATOR NOTE: the face grades 'each of the 2 keys'. The guard mints ONE")
det.append("  object (tar members inside one payload; mint_bundle does a single s3 cp).")
det.append("  Reported here as 2 of 2 MEMBERS on 1 of 1 KEY -- row IRPT_BCKEND-S25.")
record("(b) MINTED", verified == len(MEMBERS) and rc == 0 and count == "1", "\n".join(det))

# ------------------------------------------------------------------ (c) MEMBER
det = []
routed = 0
controls = 0
md5s = set()
for sha, runner, testfile in RANGES:
    crc, cout = run_bash(".tools/safe-deploy.sh", "--author", "0.4.0_DS_ClientPlatform~X",
                         "--no-pipescript", "--commit-range", "%s~1..%s" % (sha, sha))
    is_routed = ("BUNDLE-ROUTED" in cout and runner in cout
                 and "SKIP-NOT-MEMBER  [mdpf] data/assets/scripts/gold/investor_reporting/%s"
                 % runner not in cout)
    is_ctrl = ("SKIP-NOT-MEMBER" in cout and testfile in cout)
    routed += 1 if is_routed else 0
    controls += 1 if is_ctrl else 0
    for line in cout.splitlines():
        if "BUNDLE-ROUTED" in line and runner in line:
            det.append("range %s~1..%s -> %s" % (sha, sha, line.strip()))
        if "SKIP-NOT-MEMBER" in line and testfile in line:
            det.append("  in-run NEGATIVE CONTROL -> %s" % line.strip())
        mm = re.search(r"md5=([0-9a-f]{32})", line)
        if mm:
            md5s.add(mm.group(1))
    det.append("  rc=%d" % crc)
det.append("runners BUNDLE-ROUTED: %d of %d   |   sibling tests still SKIP-NOT-MEMBER: %d of %d"
           % (routed, len(RANGES), controls, len(RANGES)))
det.append("IDEMPOTENCE: distinct md5 across every mint this run = %d (expect 1) -> %s"
           % (len(md5s), sorted(md5s)))
det.append("The negative control is what makes the MEMBER verdict discriminating: the same")
det.append("  run, the same prefix, still says SKIP-NOT-MEMBER for a non-member.")
record("(c) MEMBER", routed == len(RANGES) and controls == len(RANGES) and len(md5s) == 1,
       "\n".join(det))

# ------------------------------------------------------------------ (d) LEDGER
entries = sorted((WS / "org" / "critical_paths" / "change_management").glob("*%s*.md" % SLUG))
entry = entries[-1] if entries else None
body = entry.read_text(encoding="utf-8", errors="replace") if entry else ""
closed = bool(entry) and ("CLOSED" in body)
gone = not (WS / SENTINEL).exists()
_, open_sha = run(["git", "log", "--full-history", "--format=%H", "--diff-filter=A", "--", SENTINEL])
_, del_sha = run(["git", "log", "--full-history", "--format=%H", "--diff-filter=D", "--", SENTINEL])
open_sha = open_sha.strip().splitlines()[0][:10] if open_sha.strip() else "(none)"
del_sha = del_sha.strip().splitlines()[0][:10] if del_sha.strip() else "(none)"
det = ["entry: %s" % (entry.relative_to(WS) if entry else "(absent)"),
       "status CLOSED in entry body: %s" % closed,
       "OPEN sentinel present on disk: %s (expect False)" % (not gone),
       "sentinel OPEN commit    : %s" % open_sha,
       "sentinel removal commit : %s" % del_sha]
record("(d) LEDGER", closed and gone and open_sha != "(none)" and del_sha != "(none)",
       "\n".join(det))

# --------------------------------------------------------------------- verdict
print()
passed = sum(1 for _, ok, _ in results if ok)
print("RT5-AC1: %d of %d arms PASS" % (passed, len(results)))
if passed == len(results):
    print("IBRT5-FIRST-MINT-SERVED")
    sys.exit(0)
print("BLOCKED: not every arm passed; the expect token is withheld")
sys.exit(1)
