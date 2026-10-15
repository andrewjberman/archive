"""IRPT_BCKEND workstream ~PY round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the IB-pr-456 candidate REBUILT WITH A CANDIDATE MAP.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

Why: IB-pr-561's candidate (MfxpvRhV) was built from the trunk source map with no override. That map pins the three ENDPOINT members of
irpt-ycharts-generate at commits that predate commentary_requested, so the candidate silently DROPPED the feature (CTO row S187's premise, "the
candidate's ENDPOINT members equal live", was a pin artifact; ~Y2 msg 8161 measured the live zip). The IB-pr-456 method re-pins exactly the three
ENDPOINT members with deliverables/0.9.0_WK_IRPT_BCKEND~312/make_candidate_map.py and builds with BAU_SOURCE_MAP_OVERRIDE; the R29c pins
(uploads.py, interactive_access.py) stay as the trunk map has them.

  IB205-1  IB-pr-564
    AC1  the live digest, a candidate built with the override map and different from the wrong MfxpvRhV, from the stale AHxuDf7h and from live; the three ENDPOINT members are among the moved members
    AC2  release 29's members are not moved; each ENDPOINT member read at its pin (git show recomputes sha256_now and the commentary_requested count, which must be above zero); the signed hashes; resign exactly when one moved
    AC3  the restated pre-apply digest, composition_admission.py's status consistent with the moved list, notes, counters 0, no long digit run
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~408/IB205-1_ycharts_generate_rebuild_v2.json"
LIVE_DIGEST = "5TRFZf6Grgd9V9jWBVu2QDPRVbgfWBjsuuw8rtf8hRA="
WRONG_PREFIXES = ("MfxpvRhV", "AHxuDf7h")
R29C_MEMBERS = ("generate_installed.py", "uploads.py", "ordinary_viewer.py", "interactive_access.py")
G = "infra/aws/lambda/investor-reporting/ycharts/generate/"
ENDPOINT = {
    "submission.py": (G + "submission.py", "18aba4f0792f1f16c4ba14972b830fe670d4e91edef7f6c804a8fdb967d8b4cb"),
    "acceptance.py": (G + "acceptance.py", "abbdab4935097ea5d595c0e4abcde9cea977b12b15440b0ee70caa9eeb22895d"),
    "AnalysisSubmissionRequest.schema.json": ("docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json",
                                               "1052343f111b70a9297fdfb14fc9c88894793ade68fd2d23b4076def968b1a7d"),
}
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    if r.get("function") != "irpt-ycharts-generate" or r.get("live_codesha256") != LIVE_DIGEST:
        fail("function irpt-ycharts-generate with the live CodeSha256 %s" % LIVE_DIGEST)
    c = r.get("candidate") or {}
    d = c.get("codesha256")
    if not isinstance(d, str) or not re.fullmatch(r"[A-Za-z0-9+/]{43}=", d):
        fail("candidate.codesha256 must be a base64 SHA-256")
    if d.startswith(WRONG_PREFIXES) or d == LIVE_DIGEST:
        fail("the candidate must be a NEW build with the override map: it equals the stale AHxuDf7h, the wrong MfxpvRhV or the live digest")
    if r.get("override_map_used") is not True:
        fail("override_map_used must be true: the candidate map re-pins the three ENDPOINT members (make_candidate_map.py of IB-pr-456)")
    if not is_int(c.get("moved_count")) or not is_int(c.get("total_members")) or not 0 <= c["moved_count"] <= c["total_members"] or c["total_members"] < 20:
        fail("candidate.moved_count of total_members (the denominator) must be counts")
    moved = c.get("moved_members")
    if not isinstance(moved, list) or len(moved) != c["moved_count"]:
        fail("candidate.moved_members must list exactly moved_count members")
    names = {Path(m).name for m in moved}
    miss = sorted(set(ENDPOINT) - names)
    if miss:
        fail("the ENDPOINT members %r are not among the moved members: the candidate would not carry commentary_requested" % miss)
    print("OK: the live digest, a new candidate built with the override map, the ENDPOINT members moved")


def git_show(pin, path):
    p = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (pin, path)], capture_output=True, timeout=60)
    if p.returncode != 0:
        fail("the pin %s does not hold %s" % (str(pin)[:10], path))
    return p.stdout


def c2():
    r = load(REC)
    moved = {Path(m).name for m in (r.get("candidate") or {}).get("moved_members", [])}
    hit = sorted(moved & set(R29C_MEMBERS))
    if hit:
        fail("the candidate moves release 29's members %r: a silent revert of live code" % hit)
    if r.get("r29c_members_preserved") is not True:
        fail("r29c_members_preserved must be true")
    em = r.get("endpoint_members")
    if not isinstance(em, dict) or sorted(em) != sorted(ENDPOINT):
        fail("endpoint_members must hold %s" % ", ".join(sorted(ENDPOINT)))
    anyc = False
    for k, v in em.items():
        repo_path, signed = ENDPOINT[k]
        if v.get("repo_path") != repo_path:
            fail("%s: repo_path must be %s" % (k, repo_path))
        if v.get("sha256_at_signing") != signed:
            fail("%s: sha256_at_signing must be the signed build's hash" % k)
        pin = v.get("pin")
        if not re.fullmatch(r"[0-9a-f]{40}", str(pin)):
            fail("%s: pin must be the 40-hex commit the candidate map re-pinned to" % k)
        data = git_show(pin, repo_path)
        now = hashlib.sha256(data).hexdigest()
        if v.get("sha256_now") != now:
            fail("%s: sha256_now is not the sha256 of the member at its pin (%s)" % (k, now[:12]))
        n = data.count(b"commentary_requested")
        if n < 1 or v.get("commentary_requested_count") != n:
            fail("%s: the candidate's member must carry commentary_requested (found %d at the pin; record says %r)" % (k, n, v.get("commentary_requested_count")))
        if v.get("changed") is not (now != signed):
            fail("%s: changed must equal (sha256_now differs from the signed hash)" % k)
        anyc = anyc or (now != signed)
    if r.get("endpoint_bytes_moved") is not anyc or r.get("resign_needed") is not anyc:
        fail("endpoint_bytes_moved and resign_needed must both equal whether any ENDPOINT member differs from the signed hash (%s)" % anyc)
    print("OK: no silent revert of release 29; each ENDPOINT member carries commentary_requested at its pin; re-sign exactly when one moved from the signed hash")


def c3():
    r = load(REC)
    if r.get("pre_apply_digest_restated") != LIVE_DIGEST:
        fail("pre_apply_digest_restated must be the live digest %s" % LIVE_DIGEST)
    moved = {Path(m).name for m in (r.get("candidate") or {}).get("moved_members", [])}
    if r.get("composition_admission_moved") is not ("composition_admission.py" in moved):
        fail("composition_admission_moved must equal whether composition_admission.py is among the moved members")
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (the build with the override map, what was not read, where the candidate zip sits in scratch)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the pre-apply digest restated, composition_admission.py consistent, notes, counters 0")


CHECKS = {"IB205-1-AC1": c1, "IB205-1-AC2": c2, "IB205-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p205_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
