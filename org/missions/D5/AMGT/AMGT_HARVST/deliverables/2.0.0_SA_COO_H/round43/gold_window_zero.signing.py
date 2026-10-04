"""HARVST round 43 HVST-ap-1 -- the serializing dry run the explicit-zero `chatter_window` pair signs (issuer, NO WRITE).

`window_tone.build_window` (with ap-1's universe keys) runs through the issuer's capturing client (PUTS SENT 0). The result
is diffed against the SERVED `chatter_window` part and recomputed independently (round42/gold_window.signing.py `recompute`,
extended to every universe name: a name with no mention rows reads 0 / 0 / 0 / null).

THE RULE (explicit zero rows):
- built rows == 3 x the universe (212 x 3 = 636), each window_days in {30, 90, 365};
- every SERVED row is in the build and EQUAL on every field (GONE 0, CHANGED 0);
- every ADDED row belongs to a universe name with 0 mention rows and reads articles_total 0, scored 0, voters 0, tone null,
  scorer null;
- every row equals the independent recompute (MISMATCH 0), and tone is null exactly when voters == 0.

Writes `round43/gold_window_zero_signing.json` (or GOLD_WINDOW_ZERO_SIGNING_OUT). Prints `RULE (explicit zero rows): HOLDS`
only when all of it holds.
"""
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
os.environ.setdefault("HVST_GOLD_UNIVERSE", os.path.join(DELIV, "round33", "securities.universe.r33.json"))
_spec = importlib.util.spec_from_file_location("win42", os.path.join(DELIV, "round42", "gold_window.signing.py"))
w42 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(w42)
sg, pg, store, wt, fs, tc = w42.sg, w42.pg, w42.store, w42.wt, w42.fs, w42.trading_calendar

import pyarrow.parquet as pq  # noqa: E402

OUT = os.environ.get("GOLD_WINDOW_ZERO_SIGNING_OUT") or os.path.join(HERE, "gold_window_zero_signing.json")
ZERO = {"articles_total": 0, "scored": 0, "voters": 0, "tone": None, "scorer": None}


def dumps(r):
    return json.dumps(r, sort_keys=True, default=str)


def same_numbers(r, e):
    if e is None or any(r[k] != e[k] for k in ("articles_total", "scored", "voters")):
        return False
    if r["tone"] is None or e["tone"] is None:
        return r["tone"] is None and e["tone"] is None
    return abs(r["tone"] - e["tone"]) < 1e-12


def main():
    universe = os.environ["HVST_GOLD_UNIVERSE"]
    securities = json.load(open(universe, encoding="utf-8"))
    wanted = {s["security_key"] for s in securities}
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    window_end = tc.prev_trading_day(as_of)
    real = store._default_client()
    parts_before = w42.window_parts(real)
    served = pg._latest_gold_snapshot_rows(wt.TABLE)
    mention = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_TABLE) if r.get("security_key") in wanted]
    scores = fs.latest_scores(real)
    cw = sg.CapturingClient(real)
    wt.build_window(securities, as_of, client=cw, sentiment_by_key=scores)
    (wkey, wbody), = cw.puts.items()
    rows = pq.read_table(io.BytesIO(wbody)).to_pylist()

    expect = w42.recompute(mention, scores, window_end)
    mentioned = {r["security_key"] for r in mention}
    for sec in wanted - mentioned:
        for n in wt.WINDOWS:
            expect[(sec, n)] = {"articles_total": 0, "scored": 0, "voters": 0, "tone": None}

    k = lambda r: (r["security_key"], r["window_days"])  # noqa: E731
    built = {k(r): r for r in rows}
    old = {k(r): r for r in served}
    gone = [list(x) for x in old if x not in built]
    changed = [list(x) for x in old if x in built and dumps(old[x]) != dumps(built[x])]
    added = [x for x in built if x not in old]
    added_bad = [list(x) for x in added if x[0] in mentioned
                 or any(built[x][f] != v for f, v in ZERO.items())]
    mismatch = [list(k(r)) for r in rows if not same_numbers(r, expect.get(k(r)))]
    null_bad = sum(1 for r in rows if (r["tone"] is None) != (r["voters"] == 0))
    shape_ok = len(rows) == 3 * len(wanted) and len(built) == len(rows) and {x[1] for x in built} == set(wt.WINDOWS)

    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "window_end": str(window_end), "universe": len(wanted), "parts_before": parts_before,
           "served_rows": len(served), "built_rows": len(rows), "gone": len(gone), "changed": len(changed),
           "changed_sample": changed[:10], "added": len(added),
           "added_names": sorted({x[0] for x in added}), "added_not_explicit_zero": len(added_bad),
           "mismatch": len(mismatch), "mismatch_sample": mismatch[:10], "tone_null_not_iff_zero_voters": null_bad,
           "shape_ok": shape_ok, "key": wkey, "bytes": len(wbody), "built_digest": w42.digest(rows), "puts_sent": cw.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("PARTS BEFORE: %d (newest %s)" % (len(parts_before), parts_before[-1] if parts_before else None))
    print("SERVED %d -> BUILT %d (universe %d x 3); gone %d, changed %d, added %d on %s"
          % (len(served), len(rows), len(wanted), len(gone), len(changed), len(added), out["added_names"]))
    print("CHECKS: added not explicit zero %d; mismatch vs independent recompute %d; tone-null not iff 0 voters %d; shape ok %s"
          % (len(added_bad), len(mismatch), null_bad, shape_ok))
    holds = (shape_ok and not gone and not changed and not added_bad and not mismatch and not null_bad
             and out["puts_sent"] == 0)
    print("RULE (explicit zero rows): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
