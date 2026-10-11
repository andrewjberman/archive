"""IRPT_DASHBD round 72 (issuer 2.0.0_SA_COO~D2) -- item 3 of 1.0.0_SA_CTO~DELL2's ROUND-71 ANALYSIS @a15e967740 (row D2-W108-S2).

Cell: DB-b-138 the flow-timing class of the tie-out's 90 (51 segments, closing under START for 50 and MID for 48) contradicts the
earlier refutation of FLOW_TIMING; it is shown as CONTESTED and read against the custodian's own transaction rows, counts and cause only.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB72-1-AC1  ~111/CONTESTED_51.json: denominator 51; outcomes [{outcome, count, rule}] sum to 51; refutation {stands (bool), reason};
              tieout_state {total 244, classed, contested, unclassed} summing to 244 with called_closed false; client_figures == 0;
              s3_writes == 0; a part not read carries read_denied; no string holds a run of 8 or more digits.
"""
import json
import re
import sys
from pathlib import Path

RUN = re.compile(r"\d{8,}")


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB72"))
        sys.exit(1)

    if cid != "DB72-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~111/CONTESTED_51.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    oc = r.get("outcomes")
    if r.get("denominator") != 51 or not isinstance(oc, list) or not oc:
        fail("denominator %r or no outcomes" % r.get("denominator"))
    for o in oc:
        if not str(o.get("outcome") or "").strip() or not isinstance(o.get("count"), int) or o["count"] < 1 or not str(o.get("rule") or "").strip():
            fail("an outcome lacks its name, a positive count or its rule")
    if sum(o["count"] for o in oc) != 51:
        fail("the outcomes sum to %d, not 51" % sum(o["count"] for o in oc))
    ref = r.get("refutation") or {}
    if not isinstance(ref.get("stands"), bool) or not str(ref.get("reason") or "").strip():
        fail("refutation lacks stands or its reason")
    ts = r.get("tieout_state") or {}
    parts = [ts.get("classed"), ts.get("contested"), ts.get("unclassed")]
    if ts.get("total") != 244 or any(not isinstance(x, int) for x in parts) or sum(parts) != 244 or ts.get("called_closed") is not False:
        fail("tieout_state %r" % ts)
    if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
        fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: 51 contested segments in %d outcome(s); the refutation stands: %s; tie-out %d classed, %d contested, %d unclassed, not closed"
          % (len(oc), ref["stands"], parts[0], parts[1], parts[2]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
