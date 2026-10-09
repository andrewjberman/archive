"""IRPT_DASHBD round 39 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-38 ADDENDUM 7 (on ADJUDICATION_v23 @ab9ad6b27a).

Cell: DB-b-82 a readable billing flag for Inflection's fee slices, where a source exists (row D2-W53-S2: IncludedInBilling unreadable for 526
of 562). Items E1 and E2 of the enrichment (the 11:41Z fire's A1-A7 and its REPORT duration) are the issuer's own reads at close, not cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB39-1-AC1  ~59/INF_BILLING_FLAG.json source non-empty, searched a non-empty list of {where, result}, denominator int > 0, readable int in
              [0, denominator], baseline_readable == 36 (round 37's), and gained == readable - baseline_readable.
  DB39-1-AC2  slices billed, unbilled, billing_total each {value number, readable int, denominator int, status}: billed and unbilled readable
              equal the record's readable, billing_total readable == denominator, and status "PARTIAL" iff readable < denominator.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~59/INF_BILLING_FLAG.json"


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB39"))
        sys.exit(1)

    p = root / D
    if not p.is_file():
        fail("no %s" % D)
    r = json.loads(p.read_bytes().decode("utf-8"))
    n, k = r.get("denominator"), r.get("readable")
    if cid == "DB39-1-AC1":
        s = r.get("searched")
        if not str(r.get("source") or "").strip() or not isinstance(s, list) or not s \
                or any(not isinstance(x, dict) or not x.get("where") or not x.get("result") for x in s):
            fail("source %r / searched %r" % (r.get("source"), s))
        if not isinstance(n, int) or n <= 0 or not isinstance(k, int) or not 0 <= k <= n:
            fail("denominator %r / readable %r" % (n, k))
        if r.get("baseline_readable") != 36 or r.get("gained") != k - 36:
            fail("baseline_readable %r / gained %r (readable %r)" % (r.get("baseline_readable"), r.get("gained"), k))
        print("OK: %s -- %d of %d readable (was 36, gained %d); %d place(s) searched" % (r["source"], k, n, r["gained"], len(s)))
    elif cid == "DB39-1-AC2":
        sl = r.get("slices") or {}
        bad = []
        for key in ("billed", "unbilled", "billing_total"):
            x = sl.get(key) or {}
            want = n if key == "billing_total" else k
            if not num(x.get("value")) or x.get("readable") != want or x.get("denominator") != n \
                    or x.get("status") != ("PARTIAL" if want < n else "COMPLETE"):
                bad.append((key, x))
        if bad:
            fail("slices %r" % bad[:3])
        print("OK: billed/unbilled at %d of %d (%s), billing_total COMPLETE" % (k, n, sl["billed"]["status"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
