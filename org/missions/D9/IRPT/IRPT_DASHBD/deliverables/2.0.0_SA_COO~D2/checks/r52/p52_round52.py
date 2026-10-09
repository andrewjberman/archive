"""IRPT_DASHBD round 52 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 16 item 1 and ADDENDUM 17 (msg 3583, @6d3d12876c).

Cells: DB-b-105 the never-widen packet for ONE gold Lambda release of DB-b-97 + DB-b-104 over live oNgy4rnr (census shows only their member,
reporting-gold handler.py), with the memory headroom stated; DB-b-106 Black Diamond's own transaction / posting dates read against Opal's for
every FLOW_TIMING and INCOME_DATE segment -- agree is confirmed, disagree is UNEXPLAINED.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB52-1-AC1  ~80/R45_RELEASE_CENSUS.json: base_codesha256 == oNgy4rnr; members_changed paths EXACTLY {reporting-gold handler.py}; its pin is a
              commit whose blob sha256 equals the recorded sha256 and HEAD's bytes; rollback.base_s3_version non-empty.
  DB52-1-AC2  ~80/NEVER_WIDEN_PACKET_R45_RELEASE.md carries "## Branch A", "## Branch B", "## Rollback", "## Memory headroom", "## COO half",
              "## CTO half", each half reading UNSIGNED.
  DB52-2-AC1  (AMENDMENT 1, CTO msg 3617) ~81/BD_DATES_TWO_SIDED.json in the repo carries no 10-digit token, n_segments == 475, by_verdict
              summing to 475, and private_record {path (absolute, outside the repo), sha256}; the private record at that path matches the
              sha256 and its segments cover exactly 475 distinct segments, each verdict confirmed or UNEXPLAINED, confirmed entries carrying
              bd_date and opal_date; bd_source names the served address read; vendor_calls == 0.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="
MEMBER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB52"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB52-1-AC1":
        r = load(D + "80/R45_RELEASE_CENSUS.json")
        if r.get("base_codesha256") != LIVE:
            fail("base_codesha256 %r" % r.get("base_codesha256"))
        ms = r.get("members_changed") or []
        if [m.get("path") for m in ms] != [MEMBER]:
            fail("members_changed %r, want exactly [%s]" % ([m.get("path") for m in ms], MEMBER))
        m = ms[0]
        out = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (m.get("pin"), MEMBER)], capture_output=True)
        if not m.get("pin") or out.returncode != 0:
            fail("pin %r does not resolve" % m.get("pin"))
        h = hashlib.sha256(out.stdout).hexdigest()
        if h != m.get("sha256") or hashlib.sha256((root / MEMBER).read_bytes()).hexdigest() != h:
            fail("pin blob / HEAD bytes / recorded sha256 differ")
        if not str((r.get("rollback") or {}).get("base_s3_version") or "").strip():
            fail("rollback.base_s3_version missing")
        print("OK: one member over oNgy4rnr, pinned to HEAD bytes")
    elif cid == "DB52-1-AC2":
        p = root / (D + "80/NEVER_WIDEN_PACKET_R45_RELEASE.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for hd in ("## Branch A", "## Branch B", "## Rollback", "## Memory headroom", "## COO half", "## CTO half"):
            if hd not in t:
                fail("missing heading %r" % hd)
        for hd in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(hd, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % hd)
        print("OK: packet sections present; both halves UNSIGNED")
    elif cid == "DB52-2-AC1":
        # AMENDMENT 1 (CTO msg 3617): account-level evidence lives OUTSIDE the repo. The repo record carries counts and the private
        # record's path + sha256; the check reads the private record by that path and verifies its sha256.
        want = 475
        r = load(D + "81/BD_DATES_TWO_SIDED.json")
        if re.search(r"(?<![0-9A-Za-z])\d{10}(?![0-9A-Za-z])", (root / (D + "81/BD_DATES_TWO_SIDED.json")).read_text(encoding="utf-8")):
            fail("the repo record carries a 10-digit account-like token")
        pr = r.get("private_record") or {}
        pp = Path(str(pr.get("path") or ""))
        if not pp.is_absolute() or not pp.is_file() or hashlib.sha256(pp.read_bytes()).hexdigest() != pr.get("sha256"):
            fail("private_record %r missing or sha256 mismatch" % pr)
        if r.get("n_segments") != want or sum((r.get("by_verdict") or {}).values()) != want:
            fail("repo record n_segments %r / by_verdict %r" % (r.get("n_segments"), r.get("by_verdict")))
        r = json.loads(pp.read_bytes().decode("utf-8"))
        segs = r.get("segments") or []
        keys = [(x.get("account"), json.dumps(x.get("segment"), sort_keys=True)) for x in segs]
        if len(segs) != want or len(set(keys)) != want:
            fail("%d segments (%d distinct), want %d" % (len(segs), len(set(keys)), want))
        for x in segs:
            v = x.get("verdict")
            if v not in ("confirmed", "UNEXPLAINED"):
                fail("verdict %r" % v)
            if v == "confirmed" and (not x.get("bd_date") or not x.get("opal_date")):
                fail("confirmed without both dates: %r" % x.get("segment"))
        if not r.get("bd_source") or r.get("vendor_calls") != 0:
            fail("bd_source %r / vendor_calls %r" % (r.get("bd_source"), r.get("vendor_calls")))
        bv = r.get("by_verdict") or {}
        if sum(bv.values()) != want:
            fail("by_verdict sums %d, want %d" % (sum(bv.values()), want))
        print("OK: %d segments read two-sided: %r" % (want, bv))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
