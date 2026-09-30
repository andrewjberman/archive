"""HVST-aa-2 pre-daily gate (issuer, read-only; the CTO half @98900f9339 condition): BEFORE the build-daily put, a
put-captured dry run of the producer's own `build_daily` (as-of 2026-09-30) is diffed against the served chatter_daily.

PASS (prints `PREDAILY GATE: OK`) only if every difference is one of:
- the added column `publishers_found_codes` (absent from the served part, which predates q-5);
- on a Lenovo (992_HK_Equity) row whose day lies inside THIS run's wsj run-record span: `publishers_covered_codes` gains
  `wsj`, with its derived fields `publishers_covered` and `data_status` moving accordingly.
Any other changed field, row, or key prints the first offenders and `PREDAILY GATE: STOP`.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "round26", "checks"))
import aa2_common as a  # noqa: E402
import p3_common as d  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402

ALLOWED_LENOVO = {"publishers_covered_codes", "publishers_covered", "data_status"}


def as_date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def main():
    run = a.c.load(os.path.join(a.WK, "aa2_run.json"))
    rec = [r for r in pg._iter_run_records() if r.get("run_id") == run.get("run_id")]
    lenovo = [s for s in a.c.securities() if s.get("security_key") == a.LENOVO]
    spans = pg.run_record_spans(rec, lenovo).get(a.LENOVO, {}).get("wsj") or []
    print("this run's wsj span(s) for Lenovo: %s" % spans)
    _summary, new_rows = d.dry_build()
    served = {(r["security_key"], str(r["day"])): r for r in d.served()}
    new = {(r["security_key"], str(r["day"])): r for r in new_rows}
    bad, lenovo_moved, col_added = [], 0, 0
    if set(new) != set(served):
        bad.append("row keys differ: +%d / -%d" % (len(set(new) - set(served)), len(set(served) - set(new))))
    for k in sorted(set(new) & set(served)):
        o, n = served[k], new[k]
        fields = {f for f in set(o) | set(n) if json.dumps(o.get(f), default=str) != json.dumps(n.get(f), default=str)}
        if "publishers_found_codes" in fields and "publishers_found_codes" not in o:
            col_added += 1
            fields.discard("publishers_found_codes")
        if not fields:
            continue
        in_span = k[0] == a.LENOVO and any(as_date(lo) <= as_date(k[1]) <= as_date(hi) for lo, hi in [tuple(s) for s in spans])
        gained_wsj = "wsj" in (n.get("publishers_covered_codes") or []) and "wsj" not in (o.get("publishers_covered_codes") or [])
        if in_span and fields <= ALLOWED_LENOVO and gained_wsj:
            lenovo_moved += 1
        else:
            bad.append("%s %s: %s" % (k[0], k[1], sorted(fields)))
    print("rows: served %d, dry build %d; column publishers_found_codes added on %d; Lenovo rows gaining wsj in span: %d; other diffs: %d"
          % (len(served), len(new), col_added, lenovo_moved, len(bad)))
    for b in bad[:10]:
        print("  OFFENDER " + b)
    print("PREDAILY GATE: %s" % ("OK" if not bad else "STOP"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
