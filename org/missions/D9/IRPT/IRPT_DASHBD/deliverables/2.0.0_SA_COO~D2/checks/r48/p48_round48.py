"""IRPT_DASHBD round 48 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 14 item 2 (msg 3416): one LOCAL cell classifies each of
the 510 UNEXPLAINED outside segments of TIEOUT_COMPOUND_V2.json (990 outside) by a named reason from a declared set with its rule-24 record,
or files it as a defect row; the denominator (990) is printed and the per-reason counts sum to it.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB48-1-AC1  ~73/UNEXPLAINED_CLASSIFIED.json: denominator_outside == the count of OUTSIDE verdicts in the V2 file (990); by_reason sums to it;
              every key of by_reason is in reason_set or is DEFECT; by_reason has no UNEXPLAINED key; classified holds exactly V2's
              summary UNEXPLAINED count (510) of distinct V2 OUTSIDE segments (account + segment), each with a reason in reason_set or
              DEFECT; every DEFECT entry names a row id
              present in the surprise channel; rule24_record names a file at HEAD.
"""
import json
import sys
from pathlib import Path

V2 = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~35/TIEOUT_COMPOUND_V2.json"
REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~73/UNEXPLAINED_CLASSIFIED.json"
CHAN = "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/INVESTIGATION_v1.md"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB48"))
        sys.exit(1)

    if cid != "DB48-1-AC1":
        fail("unknown criterion %r" % cid)
    v2 = json.loads((root / V2).read_bytes().decode("utf-8"))
    outside = [s for s in v2["segments"] if s.get("verdict") == "OUTSIDE"]
    if not (root / REC).is_file():
        fail("no %s" % REC)
    r = json.loads((root / REC).read_bytes().decode("utf-8"))
    rs = set(r.get("reason_set") or [])
    if not rs or "UNEXPLAINED" in rs:
        fail("reason_set %r" % sorted(rs))
    by = r.get("by_reason") or {}
    if r.get("denominator_outside") != len(outside) or sum(by.values()) != len(outside):
        fail("denominator %r / sum %r vs %d outside in V2" % (r.get("denominator_outside"), sum(by.values()), len(outside)))
    if "UNEXPLAINED" in by or any(k not in rs and k != "DEFECT" for k in by):
        fail("by_reason keys %r outside reason_set" % sorted(by))
    # V2 records the reason only in its summary, so the worker re-derives which OUTSIDE segments were UNEXPLAINED; the check holds
    # the classified set to that summary count, to OUTSIDE segments of V2, and to no repeats.
    def k(a, seg):
        return (a, json.dumps(seg, sort_keys=True))
    out_keys = {k(s["account"], s["segment"]) for s in outside}
    n_unexp = int((v2.get("outside_by_reason") or {}).get("UNEXPLAINED", 0))
    cl = r.get("classified") or []
    keys = [k(c.get("account"), c.get("segment")) for c in cl]
    if len(keys) != n_unexp or len(set(keys)) != len(keys) or not set(keys) <= out_keys:
        fail("classified %d entries (%d unique, %d outside V2's OUTSIDE set); V2 summary UNEXPLAINED = %d"
             % (len(keys), len(set(keys)), len(set(keys) - out_keys), n_unexp))
    chan = (root / CHAN).read_text(encoding="utf-8")
    for c in cl:
        if c.get("reason") not in rs and c.get("reason") != "DEFECT":
            fail("segment %r reason %r" % (c.get("segment"), c.get("reason")))
        if c.get("reason") == "DEFECT" and ('"id": "%s"' % c.get("row")) not in chan:
            fail("DEFECT segment %r names no channel row (%r)" % (c.get("segment"), c.get("row")))
    if not r.get("rule24_record") or not (root / r["rule24_record"]).is_file():
        fail("rule24_record %r" % r.get("rule24_record"))
    print("OK: %d outside classified over %d reasons; %d formerly unexplained" % (len(outside), len(by), len(cl)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
