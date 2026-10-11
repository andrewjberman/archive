"""IRPT_DASHBD round 74 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ROUND-74 ANALYSIS @d8b69fa413 (row D2-W111-S1).

Cell: DB-b-140 the 18 segments where the custodian's flow rows do not reproduce the served flow day by day: read day by day until the
difference has a cause; counts and cause only.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB74-1-AC1  ~113/UNREPRODUCED_18.json: denominator 18; flow_days {total, differing}; causes [{cause, segments, flow_days, rule}]
              whose segments sum, with no_cause.segments, to 18; a non-zero no_cause carries why; tieout_state {total 244, classed,
              contested, unclassed} summing to 244, unreproduced_within_contested (int), called_closed false; client_figures == 0;
              s3_writes == 0; no string holds a run of 8 or more digits.
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
        print("%s FAIL" % (cid or "DB74"))
        sys.exit(1)

    if cid != "DB74-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~113/UNREPRODUCED_18.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    if r.get("denominator") != 18:
        fail("denominator %r" % r.get("denominator"))
    fd = r.get("flow_days") or {}
    if not isinstance(fd.get("total"), int) or not isinstance(fd.get("differing"), int):
        fail("flow_days lacks total or differing")
    cs = r.get("causes")
    nc = r.get("no_cause") or {}
    if not isinstance(cs, list) or not isinstance(nc.get("segments"), int):
        fail("causes is not a list or no_cause.segments is missing")
    for c in cs:
        if not str(c.get("cause") or "").strip() or not isinstance(c.get("segments"), int) or c["segments"] < 1 \
                or not isinstance(c.get("flow_days"), int) or not str(c.get("rule") or "").strip():
            fail("a cause lacks its name, a positive segment count, its flow days or its rule")
    total = sum(c["segments"] for c in cs) + nc["segments"]
    if total != 18:
        fail("causes and no_cause sum to %d segments, not 18" % total)
    if nc["segments"] and not str(nc.get("why") or "").strip():
        fail("segments with no cause and no why")
    ts = r.get("tieout_state") or {}
    parts = [ts.get("classed"), ts.get("contested"), ts.get("unclassed")]
    if ts.get("total") != 244 or any(not isinstance(x, int) for x in parts) or sum(parts) != 244 \
            or not isinstance(ts.get("unreproduced_within_contested"), int) or ts.get("called_closed") is not False:
        fail("tieout_state %r" % ts)
    if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
        fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: 18 segments, %d differing flow day(s): %d cause(s) holding %d segment(s), %d with no cause; tie-out not closed"
          % (fd["differing"], len(cs), total - nc["segments"], nc["segments"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
