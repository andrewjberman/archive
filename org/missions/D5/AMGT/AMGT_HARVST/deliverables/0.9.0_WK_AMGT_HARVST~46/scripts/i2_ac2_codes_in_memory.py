"""HVST-i-2 AC2 (read-only; S3 GET/LIST only -- no put, no delete, no vendor call, no deploy).

THE REBUILD, IN MEMORY, OVER TODAY'S INPUTS with i-1's securities file (deliverables/0.9.0_WK_AMGT_HARVST~46/
securities.universe.json), set beside the SERVED newest chatter_daily part.
 (a) every PRE-EXISTING column equal on every row; any difference printed in full and attributed:
     DRIFT     = the rebuild by the BASE code (HEAD before this cell, git show 7668249a78) over the SAME inputs
                 gives the same row as the new code on the pre-existing columns (so the inputs moved, not the code);
     NON-DRIFT = the new code moved a pre-existing column against the base code. Must be 0.
 (b) the new column: row counts per data_status class; PARTIAL names >= 1 code, DENIED names 0, len(codes) ==
     publishers_covered on EVERY row; every security with a PARTIAL day listed with its day count and codes.
 (c) /timeline and timeline_day bodies built by timeline_api over these in-memory rows (loaders stubbed).
PASS only if (a)-(c) print and (a) holds (0 non-DRIFT), plus the (b) invariants."""
import datetime
import importlib.util
import io
import os
import subprocess
import sys

import pyarrow as pa
import pyarrow.parquet as pq

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_common as C  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import timeline_api as api  # noqa: E402

BASE_COMMIT = "7668249a78"
NEW_COL = "publishers_covered_codes"
SHOW = ("ASML_NA_Equity", "FDX_US_Equity")


def load_base_module():
    src = subprocess.run(["git", "show", "%s:lib/research/harvest/publication_gold.py" % BASE_COMMIT],
                         cwd=C.REPO, capture_output=True, check=True).stdout.decode("utf-8")
    spec = importlib.util.spec_from_loader("publication_gold_base", loader=None)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = os.path.join(C.REPO, "lib", "research", "harvest", "publication_gold_base.py")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)  # noqa: S102
    return mod


def dkey(r):
    return (r["security_key"], r["day"].isoformat() if hasattr(r["day"], "isoformat") else r["day"])


def main():
    problems = []
    client = store._default_client()
    key, nparts = C.newest_key(pg.GOLD_DAILY_TABLE, client)
    served = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE, client=client)
    as_of = datetime.date.fromisoformat(pg._DATE_PARTITION_RE.search(key).group(1))
    securities = C.load_json(C.NEW_PATH)
    print("== HVST-i-2 AC2: publishers_covered_codes, IN MEMORY, over today's inputs ==")
    print("securities input: %s (%d securities)" % (os.path.relpath(C.NEW_PATH, C.REPO), len(securities)))
    print("SERVED newest chatter_daily part: %s (parts=%d, rows=%d, as_of=%s)" % (key, nparts, len(served), as_of))
    print("served part has the column %s: %s" % (NEW_COL, NEW_COL in (served[0] if served else {})))
    articles, hits, _srv = C.fetch(client)
    print("inputs: silver articles=%d, listing_hit rows=%d" % (len(articles), len(hits)))

    # NEW code rebuild and BASE code rebuild over the SAME inputs
    built, _enriched = C.build_memory(securities, articles, hits, as_of)
    new_rows = built[pg.GOLD_DAILY_TABLE]
    base = load_base_module()
    mention_rt = C.roundtrip([m for art in articles for m in pg.mention_rows(art, securities)], pg.GOLD_TABLE)
    base_cov = base.publisher_coverage(hits, securities)
    base_rows = base.daily_rows(mention_rt, securities, start=base.BACKFILL_FLOOR, end=as_of, coverage=base_cov)
    base_rows = pa.Table.from_pylist(base_rows, schema=base.GOLD_DAILY_SCHEMA).to_pylist()
    print("base code (%s) schema columns=%d; new code schema columns=%d; extra column(s): %s" % (
        BASE_COMMIT, len(base.GOLD_DAILY_SCHEMA.names), len(pg.GOLD_DAILY_SCHEMA.names),
        [n for n in pg.GOLD_DAILY_SCHEMA.names if n not in base.GOLD_DAILY_SCHEMA.names]))
    assert [n for n in pg.GOLD_DAILY_SCHEMA.names if n != NEW_COL] == base.GOLD_DAILY_SCHEMA.names, "existing columns moved"

    # ---- (a) ----
    print("\n== (a) every PRE-EXISTING column, served vs in-memory rebuild ==")
    pre_cols = [n for n in pg.GOLD_DAILY_SCHEMA.names if n != NEW_COL]
    s_by = {dkey(r): r for r in served}
    n_by = {dkey(r): r for r in new_rows}
    b_by = {dkey(r): r for r in base_rows}
    print("denominator: served rows=%d (distinct keys %d); rebuilt rows=%d (distinct keys %d); base-code rebuilt rows=%d; "
          "pre-existing columns=%d" % (len(served), len(s_by), len(new_rows), len(n_by), len(base_rows), len(pre_cols)))

    def proj(r):
        return None if r is None else {c: C.canon(r.get(c)) for c in pre_cols}

    # code-change effect: new vs base on the pre-existing columns, every row
    code_moved = [k for k in set(n_by) | set(b_by) if proj(n_by.get(k)) != proj(b_by.get(k))]
    print("rows where the NEW code differs from the BASE code on a pre-existing column (same inputs): %d of %d" % (
        len(code_moved), len(n_by)))
    if code_moved:
        problems.append("new code moved %d pre-existing cells vs base code" % len(code_moved))

    diffs = sorted(k for k in set(s_by) | set(n_by) if proj(s_by.get(k)) != proj(n_by.get(k)))
    drift = nondrift = 0
    for k in diffs:
        s, n, b = s_by.get(k), n_by.get(k), b_by.get(k)
        att = "DRIFT" if proj(b) == proj(n) else "NON-DRIFT"
        if att == "DRIFT":
            drift += 1
        else:
            nondrift += 1
        if s is None or n is None:
            print("  [%s] %s | one side absent (served %s, rebuilt %s)" % (
                att, C.a(str(k)), "present" if s else "absent", "present" if n else "absent"))
        else:
            for c in pre_cols:
                if C.canon(s.get(c)) != C.canon(n.get(c)):
                    print("  [%s] %s | %s: served=%s rebuilt=%s" % (att, C.a(str(k)), c, C.a(C.canon(s.get(c))), C.a(C.canon(n.get(c)))))
    print("(a) rows with any pre-existing-column difference: %d of %d served rows -> DRIFT=%d NON-DRIFT=%d" % (
        len(diffs), len(s_by), drift, nondrift))
    if nondrift:
        problems.append("(a) %d non-DRIFT differences" % nondrift)

    # ---- (b) ----
    print("\n== (b) %s ==" % NEW_COL)
    classes = {}
    bad_len = bad_partial = bad_denied = bad_order = bad_complete = 0
    partial_secs = {}
    for r in new_rows:
        codes = r[NEW_COL]
        ds = r["data_status"]
        classes[ds] = classes.get(ds, 0) + 1
        if codes is None or len(codes) != r["publishers_covered"]:
            bad_len += 1
        if codes is not None and codes != [p for p in pg.ENABLED_PUBLISHERS if p in codes]:
            bad_order += 1
        if ds == "PARTIAL":
            if not codes:
                bad_partial += 1
            e = partial_secs.setdefault(r["security_key"], {"days": 0, "codes": {}})
            e["days"] += 1
            t = tuple(codes or ())
            e["codes"][t] = e["codes"].get(t, 0) + 1
        if ds == "DENIED" and codes:
            bad_denied += 1
        if ds == "COMPLETE" and codes != list(pg.ENABLED_PUBLISHERS):
            bad_complete += 1
    print("rows=%d; ENABLED_PUBLISHERS=%s" % (len(new_rows), list(pg.ENABLED_PUBLISHERS)))
    print("row counts per data_status: %s" % dict(sorted(classes.items())))
    print("violations: len(codes)!=publishers_covered=%d; codes out of ENABLED order=%d; PARTIAL naming 0 codes=%d; "
          "DENIED naming >0 codes=%d; COMPLETE not naming all=%d" % (bad_len, bad_order, bad_partial, bad_denied, bad_complete))
    for name, v in (("len", bad_len), ("order", bad_order), ("partial", bad_partial), ("denied", bad_denied),
                    ("complete", bad_complete)):
        if v:
            problems.append("(b) %s violations=%d" % (name, v))
    print("securities with a PARTIAL day: %d" % len(partial_secs))
    for sk in sorted(partial_secs):
        e = partial_secs[sk]
        print("  %-28s partial_days=%-4d codes=%s" % (sk, e["days"], {",".join(k): v for k, v in sorted(e["codes"].items())}))
    # the round-trip through the parquet schema
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pylist(new_rows, schema=pg.GOLD_DAILY_SCHEMA), buf)
    back = pq.read_table(io.BytesIO(buf.getvalue())).to_pylist()
    rt_ok = [C.canon_row(r) for r in back] == [C.canon_row(r) for r in new_rows]
    print("in-memory parquet round trip (no S3): %d rows equal: %s; column type: %s" % (
        len(back), rt_ok, pg.GOLD_DAILY_SCHEMA.field(NEW_COL).type))
    if not rt_ok:
        problems.append("(b) parquet round trip differs")
    asml = {sk: partial_secs.get(sk) for sk in ("ASML_NA_Equity", "ASML_US_Equity")}
    print("ASML: %s" % {k: (None if v is None else (v["days"], {",".join(c): n for c, n in v["codes"].items()})) for k, v in asml.items()})

    # ---- (c) ----
    print("\n== (c) timeline_api bodies over the in-memory rows (loaders stubbed) ==")
    by_sec = {}
    for r in new_rows:
        by_sec.setdefault(r["security_key"], []).append(r)
    for sk in SHOW:
        rows = by_sec.get(sk)
        if not rows:
            print("\n%s: no rows in the rebuild" % sk)
            problems.append("(c) %s has no rows" % sk)
            continue
        res = api.get_timeline(sk, pg.BACKFILL_FLOOR.isoformat(), as_of.isoformat(), lambda k: by_sec.get(k, []), lambda k: [])
        if api.is_error_body(res):
            problems.append("(c) %s timeline is an error body" % sk)
            print(res)
            continue
        series = res["series"]
        cls = {}
        for e, r in zip(series, sorted(rows, key=lambda x: x["day"])):
            cls[e["data_status"]] = cls.get(e["data_status"], 0) + 1
        print("\n%s: series entries=%d per class=%s; every entry carries both fields: %s" % (
            sk, len(series), dict(sorted(cls.items())),
            all("publishers_covered" in e and "publishers_covered_codes" in e for e in series)))
        for status in ("PARTIAL", "DENIED"):
            ent = next((e for e in series if e["data_status"] == status), None)
            if ent is None:
                print("  %s: no %s entry for this security" % (sk, status))
                continue
            print("  /timeline series entry (%s): %s" % (status, C.a(ent)))
            body = api.get_timeline_day(sk, ent["date"], lambda k: by_sec.get(k, []), lambda k, d: [])
            print("  timeline_day body      (%s): %s" % (status, C.a(body)))
            if body.get("publishers_covered_codes") != ent["publishers_covered_codes"] or \
                    body.get("publishers_covered") != ent["publishers_covered"]:
                problems.append("(c) %s %s route bodies disagree" % (sk, status))

    print("\nproblems: %d" % len(problems))
    for p in problems:
        print("PROBLEM: %s" % C.a(p))
    print("AC2 RESULT: %s" % ("PASS" if not problems else "FAIL"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
