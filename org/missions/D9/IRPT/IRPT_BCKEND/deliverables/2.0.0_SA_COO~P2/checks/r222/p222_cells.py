"""IRPT_BCKEND workstream ~PJ round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the release CANDIDATES of the three per-firm holdings bundles.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB222-1  IB-pr-589  per firm, the bundle that the scheduled fire fetches, built from a pin that carries IB-pr-576, 577 and 582, BUILD ONLY, compared with the live bundle (member by member)
    AC1  the identity and the pin: base commit, read date, the pin an ancestor of HEAD that carries the absent_at_source blocks, the three firms, the claim measured
    AC2  per firm: the live bundle hash, the candidate hash different from it, the changed members (each recomputed from git at the pin), holdings_snapshot.py among them, any other changed member named with its reason
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

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~428/IB222-1_holdings_bundles_candidate.json"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
FIRMS = ("49financial", "cottonwood", "inflection")
fail, load, is_int = P6.fail, P6.load, P6.is_int


def git(*a):
    return subprocess.run(["git", "-C", str(P6.ROOT), *a], capture_output=True, timeout=60)


def ac1(r):
    P8.identity(r)
    pin = r.get("pin")
    if not re.fullmatch(r"[0-9a-f]{40}", str(pin)):
        fail("pin must be a 40-hex commit")
    if git("merge-base", "--is-ancestor", pin, "HEAD").returncode != 0:
        fail("the pin must be an ancestor of HEAD")
    p = git("show", "%s:%s" % (pin, HS))
    if p.returncode != 0 or b"BEGIN ABSENT-AT-SOURCE-A" not in p.stdout or b"BEGIN ABSENT-AT-SOURCE-B" not in p.stdout or b"BEGIN ABSENT-AT-SOURCE-C" not in p.stdout:
        fail("holdings_snapshot.py at the pin must carry the ABSENT-AT-SOURCE A, B and C blocks (IB-pr-576, 577, 582)")
    if r.get("holdings_snapshot_blob") != git("rev-parse", "%s:%s" % (pin, HS)).stdout.decode().strip():
        fail("holdings_snapshot_blob must equal the git blob of holdings_snapshot.py at the pin")
    if not isinstance(r.get("firms"), dict) or sorted(r["firms"]) != sorted(FIRMS):
        fail("firms must hold exactly %s" % (FIRMS,))
    print("OK: identity; the pin carries the exemption blocks; three firms")


def ac2(r):
    for f in FIRMS:
        e = r["firms"][f]
        for k in ("live_bundle_sha256", "candidate_bundle_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(e.get(k, ""))):
                fail("%s.%s must be a 64-hex sha256" % (f, k))
        if e["live_bundle_sha256"] == e["candidate_bundle_sha256"]:
            fail("%s: the candidate must differ from the live bundle" % f)
        P8.count(e.get("members_total"), f + ".members_total")
        ch = e.get("changed_members")
        if not isinstance(ch, list) or not ch or len(ch) > e["members_total"]:
            fail("%s.changed_members must list the changed members (at least holdings_snapshot.py)" % f)
        names = set()
        for m in ch:
            path, sha = m.get("repo_path"), m.get("sha256_at_pin")
            names.add(path)
            d = git("show", "%s:%s" % (r["pin"], path))
            if d.returncode != 0 or hashlib.sha256(d.stdout).hexdigest() != sha:
                fail("%s: %s sha256_at_pin is not the sha256 of the file at the pin" % (f, path))
        if HS not in names:
            fail("%s: holdings_snapshot.py must be among the changed members" % f)
        extra = sorted(names - {HS})
        reasons = e.get("extra_changed_reasons") or {}
        if sorted(reasons) != extra or not all(isinstance(x, str) and len(x) >= 30 for x in reasons.values()):
            fail("%s: every changed member beyond holdings_snapshot.py (%r) needs a reason of 30+ characters in extra_changed_reasons" % (f, extra))
    print("OK: per firm, the live and candidate bundles differ; changed members at their pin")


CHECKS = {"IB222-1-AC1": lambda: ac1(load(REC)), "IB222-1-AC2": lambda: ac2(load(REC)), "IB222-1-AC3": lambda: P8.ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p222_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
