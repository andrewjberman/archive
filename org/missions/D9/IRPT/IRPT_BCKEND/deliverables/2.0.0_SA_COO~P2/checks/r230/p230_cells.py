"""IRPT_BCKEND workstream ~PJ round 5 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the release CANDIDATE of the 49 Financial performance function.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB230-1  IB-pr-597  the minimal candidate of irpt-holdings-performance-lambda carrying the split adjustment (IB-pr-578 and IB-pr-583), BUILD ONLY against the live digest, with a candidate source map
    AC1  the identity: base commit, the live CodeSha256 equal to the one the issuer read, a NEW candidate digest built with the override map, the two members among the moved ones
    AC2  the members at their pins: each member's sha256 recomputed from git at the pin, the split blocks present in the producer, the declaration present in sources.json, the pin an ancestor of HEAD, siblings left unmoved, any extra moved member named with its reason
    AC3  notes, the six counters 0, no long digit run
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r218"))
import p196_cells as P6  # noqa: E402
import p218_cells as P8  # noqa: E402

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~435/IB230-1_perf_candidate.json"
FN = "irpt-holdings-performance-lambda"
LIVE_DIGEST = "o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok="
H = "data/assets/scripts/gold/irpt_holdings_performance/"
MEMBERS = {"holdings_performance.py": H + "holdings_performance.py", "sources.json": H + "sources.json"}
SIBLINGS = ("irpt-inf-holdings-performance-lambda", "irpt-cot-holdings-performance-lambda")
fail, load, is_int = P6.fail, P6.load, P6.is_int


def git_show(pin, path):
    p = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (pin, path)], capture_output=True, timeout=60)
    if p.returncode != 0:
        fail("the pin %s does not hold %s" % (str(pin)[:10], path))
    return p.stdout


def ac1(r):
    P8.identity(r)
    if r.get("function") != FN or r.get("live_codesha256") != LIVE_DIGEST:
        fail("function %s with the live CodeSha256 %s (re-read it at the act: another value is a STOP)" % (FN, LIVE_DIGEST))
    c = r.get("candidate") or {}
    d = c.get("codesha256")
    if not isinstance(d, str) or not re.fullmatch(r"[A-Za-z0-9+/]{43}=", d) or d == LIVE_DIGEST:
        fail("candidate.codesha256 must be a base64 SHA-256 different from the live digest")
    if r.get("override_map_used") is not True:
        fail("override_map_used must be true (a candidate source map re-pinning the two members of this function only)")
    if not is_int(c.get("moved_count")) or not is_int(c.get("total_members")) or not 1 <= c["moved_count"] <= c["total_members"] or c["total_members"] < 5:
        fail("candidate.moved_count of total_members must be counts")
    moved = c.get("moved_members")
    if not isinstance(moved, list) or len(moved) != c["moved_count"]:
        fail("candidate.moved_members must list exactly moved_count members")
    names = {Path(m).name for m in moved}
    miss = sorted(set(MEMBERS) - names)
    if miss:
        fail("the members %r are not among the moved members: the candidate would not carry the split adjustment" % miss)
    print("OK: live digest, a new candidate, the two members moved (%d of %d)" % (c["moved_count"], c["total_members"]))


def ac2(r):
    mem = r.get("members")
    if not isinstance(mem, dict) or sorted(mem) != sorted(MEMBERS):
        fail("members must hold %s" % sorted(MEMBERS))
    for k, v in mem.items():
        if v.get("repo_path") != MEMBERS[k]:
            fail("%s: repo_path must be %s" % (k, MEMBERS[k]))
        pin = v.get("pin")
        if not re.fullmatch(r"[0-9a-f]{40}", str(pin)):
            fail("%s: pin must be a 40-hex commit" % k)
        anc = subprocess.run(["git", "-C", str(P6.ROOT), "merge-base", "--is-ancestor", pin, "HEAD"], capture_output=True)
        if anc.returncode != 0:
            fail("%s: the pin must be an ancestor of HEAD" % k)
        data = git_show(pin, MEMBERS[k])
        if v.get("sha256_now") != hashlib.sha256(data).hexdigest():
            fail("%s: sha256_now is not the sha256 of the member at its pin" % k)
        if k == "holdings_performance.py":
            a, b = data.count(b"BEGIN SPLIT-ADJUST-A"), data.count(b"BEGIN SPLIT-ADJUST-B")
            if a < 1 or b < 1 or v.get("split_blocks_a") != a or v.get("split_blocks_b") != b:
                fail("holdings_performance.py at the pin must carry SPLIT-ADJUST-A and -B blocks, counted in the record (found %d and %d)" % (a, b))
        else:
            if b'"split_adjust"' not in data or v.get("split_adjust_declared") is not True:
                fail("sources.json at the pin must declare split_adjust")
    sib = r.get("siblings_unmoved")
    if not isinstance(sib, list) or sorted(sib) != sorted(SIBLINGS):
        fail("siblings_unmoved must list %s (the other functions that stage these members are NOT released)" % (SIBLINGS,))
    moved = {Path(m).name for m in (r.get("candidate") or {}).get("moved_members", [])}
    extra = sorted(moved - set(MEMBERS))
    reasons = r.get("extra_moved_reasons") or {}
    if sorted(reasons) != extra or not all(isinstance(x, str) and len(x) >= 30 for x in reasons.values()):
        fail("every moved member beyond the two (%r) needs a reason of 30+ characters in extra_moved_reasons" % extra)
    print("OK: members at their pins; split blocks present; siblings unmoved; extras named (%d)" % len(extra))


CHECKS = {"IB230-1-AC1": lambda: ac1(load(REC)), "IB230-1-AC2": lambda: ac2(load(REC)), "IB230-1-AC3": lambda: P8.ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p230_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
