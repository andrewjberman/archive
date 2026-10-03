"""RIV-nm-1 AC4 (issuer amendment A1, 2026-10-02): the REAL two-field BQL response lands, types and names.

Source: the issuer's live probe at 16:47Z (one fund, BIDD, dates=2026-10-01, through nm-1's own excel_fetch, local file only).
With get(id(), name()) Bloomberg PREFIXES every metadata column by its field ("id().ORIG_IDS", "name().SOURCE", ...), and
the response fills exactly the 16 columns excel_fetch reads (A-P). silver_bloomberg.parse_capture refused the real bytes
with "header lacks ORIG_IDS", so as built nm-1 would stop the vehicle's Bloomberg leg on the next trading morning.

The fixture below is the probe's real header and three of its real rows (REPORT_DATE and DATE set to the requested day so
the import files them under it). Limbs:
  (a) the capture imports to bronze and types into ONE silver object (today: refused);
  (b) silver carries today's column names for the id() metadata (orig_ids, position, report_date) and `name`;
  (c) G1 security_name carries each captured name verbatim;
  (d) excel_fetch reads past column P (a fixed A-P read truncates the next field), by its source text;
  (e) CONTROL: today's single-field, unprefixed capture (test_b1's HDR) still imports and types.
At base and at nm-1's first build: (a)-(d) FAIL; (e) PASS.
"""
import datetime as dt
import inspect
import io
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-10-01"
TS = "2026-10-01 00:00:00+00:00"
HDR = ["ID", "id().SOURCE", "id().POSITION", "id().POSITION_CHANGE", "id().WEIGHTS", "id().CURRENCY",
       "id().REPORTED_MKT_VAL", "id().DATE", "id().REPORT_DATE", "id().ORIG_IDS", "id().POSITION_TYPE", "id()",
       "name().SOURCE", "name().POSITION_TYPE", "name().ID_DATE", "name()"]
ROWS = [
    ["6098 JP Equity", "ETF", 49700.0, 0.0, 1.3478718979888622, "USD", 5286447.841582, TS, TS, "BIDD US Equity", "L",
     "6098 JP Equity", "ETF", "L", TS, "Recruit Holdings Co Ltd"],
    ["ASRNL NA Equity", "ETF", 93759.0, 0.0, 1.9476877733548055, "USD", 7638967.650331, TS, TS, "BIDD US Equity", "L",
     "ASRNL NA Equity", "ETF", "L", TS, "ASR Nederland NV"],
    ["700 HK Equity", "ETF", 244940.0, 0.0, 3.4015814607275443, "USD", 13341240.364058, TS, TS, "BIDD US Equity", "L",
     "700 HK Equity", "ETF", "L", TS, "Tencent Holdings Ltd"],
]
NAMES = {r[0]: r[-1] for r in ROWS}


def land(cb, sb, sinks, tmp, cap, tag):
    spec = f"local:{tmp / ('sink_' + tag)}"
    (tmp / f"cap_{tag}.json").write_text(json.dumps(cap), encoding="utf-8")
    try:
        r1 = cb.handler_entry({"mode": "import", "captures": [str(tmp / f"cap_{tag}.json")], "batch_id": tag,
                               "sink": spec, "date": D})
        r2 = sb.handler_entry({"mode": "replay", "batch_id": tag + "s", "sink": spec, "date": D})
    except Exception as e:  # a raised refusal is the finding
        print(f"[{tag}] raised {type(e).__name__}: {str(e)[:200]}")
        return None, None, []
    s = sinks.get_sink(spec)
    uris = [u for u in s.list(sb.silver_prefix(D) + "/") if u.endswith(".parquet")]
    print(f"[{tag}] import {r1.get('status')} | silver {r2.get('status')} | {len(uris)} silver object(s)"
          + ("" if r2.get("status") == "OK" else f" | detail {str(r2)[:240]}"))
    return r1, r2, [(s, u) for u in uris]


def run(v):
    c.setup_path()
    import pyarrow.parquet as pq
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import gold_canonical_shape as gcs
    from rivalfunds import silver_bloomberg as sb
    from rivalfunds import sinks
    from rivalfunds.tests import test_b1_bloomberg_channel as tb1

    tmp = pathlib.Path(c.tmpdir("rv_nm1ac4_"))
    q = f"get(id(), name()) for(holdings(['BIDD US Equity'],dates={D}))"
    cap = {"requested_date": D, "at": "2026-10-02T12:47:27.181958-04:00", "query": q, "anchor": "ID",
           "rows": [HDR] + ROWS}
    r1, r2, objs = land(cb, sb, sinks, tmp, cap, "real")
    ok = r1 is not None and r1.get("status") == "OK" and r2.get("status") == "OK" and len(objs) == 1
    v.check(ok, "(a) the real two-field capture imports and types into ONE silver object (today: refused)")
    silver = []
    if len(objs) == 1:
        s, u = objs[0]
        silver = pq.read_table(io.BytesIO(s.get(u))).to_pylist()
        print("silver columns:", sorted(silver[0]))
    cols = set(silver[0]) if silver else set()
    v.check({"orig_ids", "position", "report_date", "name"} <= cols,
            "(b) silver keeps today's names for the id() metadata (orig_ids, position, report_date) and carries `name`")
    names = {}
    if silver:
        g1 = gcs.build_bloomberg_rows(silver, "BIDD", dt.date.fromisoformat(D), "rev-nm1ac4", objs[0][1],
                                      lambda sec, path=None: {"security_key": None, "reason": "fixture"}, None,
                                      "fixture")
        names = {r["security_bloomberg"]: r.get("security_name") for r in g1}
        print("G1 security_name:", names)
    v.check(all(names.get(k) == n for k, n in NAMES.items()),
            "(c) G1 security_name carries each captured name verbatim")

    src = inspect.getsource(cb.excel_fetch)
    fixed = re.findall(r'Range\("A1:([A-Z]+)%d"', src)
    wide = bool(fixed) and all(len(col) > 1 or col >= "Z" for col in fixed)
    print("excel_fetch read ranges:", fixed or "(no fixed A1:<col> range)", "| UsedRange.Columns:",
          "UsedRange.Columns" in src)
    v.check(wide or (not fixed and "UsedRange.Columns" in src),
            "(d) excel_fetch reads past column P (at least A:Z, or the used range's own width)")

    old_rows = [tb1._row("TXUE", sec, D) for sec in ("8306 JP Equity", "ATD CN Equity")]
    old = tb1._cap(D, f"{D}T23:00:00-04:00", old_rows, funds=("TXUE",), header=tb1.HDR)
    o1, o2, oobjs = land(cb, sb, sinks, tmp, old, "old")
    v.check(o1 is not None and o1.get("status") == "OK" and o2.get("status") == "OK" and len(oobjs) == 1,
            "(e) control: today's single-field, unprefixed capture still imports and types")


failures = c.guarded("AC4", run)
print("AC4 RESULT: PASS 0 failures" if failures == 0 else f"AC4 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
