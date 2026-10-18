"""ETFS_RIVALS round 32 -- the held-tr fill in three acts, none of which writes live S3 until act 3 (2.0.0_SA_COO~RV).

    python heldtr_stage.py pull     <code root> <layer dir> <units json> <max points> [--live]
    python heldtr_stage.py replay   <code root> <layer dir> <out dir> [--day YYYY-MM-DD] [--control]
    python heldtr_stage.py publish  <code root> <layer dir> [--apply]

pull     runs `enrichment_bloomberg` mode held-tr (RIV-za-1) through an OVERLAY sink: reads the local layer, then live S3 (so the
         stored currencies are the live ones); every write lands in <layer dir> only. A dry run unless --live. Bloomberg is called
         only with --live, on the Terminal machine.
replay   builds gold holding_contribution for the newest live day (or --day) TWICE through overlays: A with an empty layer (the
         live inputs as they are), B with <layer dir> (A plus the held-tr objects). Every build writes into its own scratch layer
         under <out dir>; no S3 write, no vendor call. Prints per fund: rows, content hash A and B, rows whose numbers differ, and
         the rank changes of the fund's holdings by contribution. --control plants synthetic held-tr rows into a COPY of the
         layer first (the comparison's positive control: B must differ).
publish  lists every `gold/security_market` object in <layer dir> and, with --apply, puts each to the same live S3 uri when that
         uri is absent (never overwriting), reading each back. Without --apply it prints the write set and writes nothing.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import pathlib
import shutil
import sys

ACT = sys.argv[1]
ROOT = pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))

import pandas as pd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from rivalfunds import enrichment_bloomberg as eb  # noqa: E402
from rivalfunds import gold_holding_contribution as hc  # noqa: E402
from rivalfunds import homes, sinks  # noqa: E402

G4 = homes.address("rivalfunds", "etfs", "gold", "security_market", "date=")
HC = homes.address("rivalfunds", "etfs", "gold", "holding_contribution", "date=")


class OverlaySink:
    """Reads the local layer first, then live S3; writes go to the local layer only."""
    kind = "overlay"

    def __init__(self, local_root):
        self.live, self.local = sinks.S3Sink(), sinks.LocalSink(str(local_root))

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.live.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.live.exists(uri)

    def list(self, prefix_uri):
        return sorted(set(self.live.list(prefix_uri)) | set(self.local.list(prefix_uri)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


def pull(argv) -> int:
    layer, units_path, max_points = pathlib.Path(argv[0]), argv[1], int(argv[2])
    live = "--live" in argv
    doc = json.loads(pathlib.Path(units_path).read_text(encoding="utf-8"))
    units = doc.get("securities") if isinstance(doc, dict) else doc
    layer.mkdir(parents=True, exist_ok=True)
    res = eb.handler_entry({"mode": "held-tr", "units": units, "max_points": max_points, "dry_run": not live,
                            "batch_id": f"rv-heldtr-{layer.name}", "sink": OverlaySink(layer)})
    print(json.dumps({k: v for k, v in res.items() if k != "detail"} | {"detail": str(res.get("detail"))[:600]}, default=str))
    return 0 if res.get("status") in ("OK", "PARTIAL") else 2


def _hc_day(live) -> str:
    days = sorted({u.split("date=", 1)[1][:10] for u in live.list(HC) if "date=" in u})
    return days[-1]


def _build(layer: pathlib.Path, scratch: pathlib.Path, day: str) -> pd.DataFrame:
    if scratch.exists():
        shutil.rmtree(scratch)
    if layer is not None and layer.exists():
        shutil.copytree(layer, scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    s = OverlaySink(scratch)
    before = set(s.local.list(HC + day + "/"))
    r = hc.handler_entry({"date": day, "sink": s})
    new = sorted(u for u in set(s.local.list(HC + day + "/")) - before if u.endswith(".parquet"))
    if not new:
        raise SystemExit(f"no table written for {day}: {r.get('status')} {str(r.get('detail'))[:300]}")
    return pq.read_table(io.BytesIO(s.local.get(new[-1]))).to_pandas()


def _plant_control(layer: pathlib.Path, live, day: str) -> int:
    """Synthetic held-tr rows on the 25 trading days before `day`: the newest live close of each security, TR +5 percent."""
    from lib import trading_calendar as tc
    have = sorted({u.split("date=", 1)[1][:10] for u in live.list(G4) if "date=" in u and u.split("date=", 1)[1][:10] <= day})
    us = sorted(u for u in live.list(G4 + have[-1] + "/") if u.endswith(".parquet"))
    base = pd.concat([pq.read_table(io.BytesIO(live.get(u))).to_pandas() for u in us], ignore_index=True)
    base = base[base.px_close.notna() & (base.px_close > 0)].drop_duplicates("security_id")
    d0 = dt.date.fromisoformat(day)
    days = [d.isoformat() for d in tc.trading_days_between(d0 - dt.timedelta(days=45), d0 - dt.timedelta(days=1))][-25:]
    s = sinks.LocalSink(str(layer))
    n = 0
    for d in days:
        data = {r.security_bloomberg: {"PX_LAST": float(r.px_close), "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": 5.0, "CRNCY": r.currency}
                for r in base.itertuples()}
        prov = {"revision": "20261017T000000Z-heldtrcontrol", "produced_at": "2026-10-17T00:00:00Z", "producer_version": "control",
                "input_manifest": "{}"}
        rows = eb.market_rows(data, d, eb.MARKET_SOURCE_HIST, prov, "held-tr")
        for r in rows:
            r["price_date"] = d
        s.put(eb.market_target_uri(d, "20261017T000000Z-heldtrcontrol"), eb._parquet_bytes(eb._topup_table(rows)))
        n += len(rows)
    return n


def replay(argv) -> int:
    layer, out = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    live = sinks.S3Sink()
    day = argv[argv.index("--day") + 1] if "--day" in argv else _hc_day(live)
    if "--control" in argv:
        ctl = out / "control_layer"
        if ctl.exists():
            shutil.rmtree(ctl)
        if layer.exists():
            shutil.copytree(layer, ctl)
        print(f"control: planted {_plant_control(ctl, live, day)} synthetic held-tr rows")
        layer = ctl
    n_obj = len([u for u in sinks.LocalSink(str(layer)).list(G4) if u.endswith(".parquet")]) if layer.exists() else 0
    print(f"day {day} | held-tr objects in the layer: {n_obj}")
    a = _build(None, out / "arm_A", day)
    b = _build(layer, out / "arm_B", day)
    key = ["fund_id", "period", "axis", "bucket"]   # one row of the table: a fund's holding (bucket) on one axis and period
    rec = {"day": day, "layer": str(layer), "held_tr_objects": n_obj, "whole_table": {"A": hc._content_sha(a), "B": hc._content_sha(b)},
           "key": key, "funds": {}}

    def _ne(x, y):
        both_nan = x.isna() & y.isna()
        return ~both_nan & ((x - y).abs().gt(1e-12) | x.isna() | y.isna())

    print(f"{'fund':<6} {'rows':>5} {'A':<13} {'B':<13} {'contrib_moved':>13} {'rank_best_moved':>15} {'implied_days A->B':>18}")
    for f in sorted(a["fund_id"].dropna().unique()):
        fa, fb = a[a["fund_id"] == f], b[b["fund_id"] == f]
        j = fa.set_index(key).join(fb.set_index(key), lsuffix="_A", rsuffix="_B", how="outer")
        dup = int(fa.duplicated(key).sum())
        contrib = int(_ne(j["contribution_A"], j["contribution_B"]).sum())
        rank = int(_ne(j["rank_best_A"], j["rank_best_B"]).sum())
        imp = (int(fa["n_days_holding_implied"].sum()), int(fb["n_days_holding_implied"].sum()))
        sha_a, sha_b = hc._content_sha(fa.reset_index(drop=True)), hc._content_sha(fb.reset_index(drop=True))
        moved = j[_ne(j["rank_best_A"], j["rank_best_B"])].reset_index()
        top = moved.assign(d=(moved["rank_best_B"] - moved["rank_best_A"]).abs()).sort_values("d", ascending=False).head(5)
        rec["funds"][str(f)] = {"rows": int(len(fa)), "duplicate_keys": dup, "A": sha_a, "B": sha_b, "equal": sha_a == sha_b,
                                "contribution_moved": contrib, "rank_best_moved": rank, "holding_implied_days": list(imp),
                                "largest_rank_moves": top[["period", "axis", "bucket", "rank_best_A", "rank_best_B"]].to_dict("records")}
        print(f"{str(f):<6} {len(fa):>5} {sha_a[:12]:<13} {sha_b[:12]:<13} {contrib:>13} {rank:>15} {imp[0]:>8} -> {imp[1]:<8}"
              + (f" DUP {dup}" if dup else ""))
    eq = sum(1 for v in rec["funds"].values() if v["equal"])
    print(f"funds equal: {eq} of {len(rec['funds'])} | whole table A == B: {rec['whole_table']['A'] == rec['whole_table']['B']}")
    (out / f"heldtr_replay_{day}{'_control' if '--control' in argv else ''}.json").write_text(json.dumps(rec, indent=2, default=str),
                                                                                        encoding="utf-8")
    return 0


def readers(argv) -> int:
    """CTO half condition 1 (@98d4271685): the two G4 readers act 2 did not measure, through the same overlays A (live) and B
    (live + layer). dramatic_move: `detect` only (no web lookup, no write) over the window; every candidate in B that A lacks is
    printed, and one on a date the layer holds is a STOP. price_series: `series` over every G4 security of the window, then per
    fund (the securities its G1 reports hold in the window): points by source (market, implied, none) and big-move gaps, A -> B."""
    from rivalfunds import dramatic_move as dm
    from rivalfunds import price_series as ps

    layer, out = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    day = argv[argv.index("--day") + 1] if "--day" in argv else _hc_day(sinks.S3Sink())
    hi = dt.date.fromisoformat(day)
    lo = hi - dt.timedelta(days=int(argv[argv.index("--window") + 1]) if "--window" in argv else 366)
    layer_dates = sorted({u.split("date=", 1)[1][:10] for u in sinks.LocalSink(str(layer)).list(G4)
                          if u.endswith(".parquet")}) if layer.exists() else []
    empty = out / "empty_layer"
    empty.mkdir(parents=True, exist_ok=True)
    arms = {"A": OverlaySink(empty), "B": OverlaySink(layer)}
    g1 = hc._read(arms["A"], hc._newest_by_date(arms["A"], homes.canonical_shape(""), lo.isoformat(), hi.isoformat()), hc.G1_COLUMNS)
    fund_col = "fund_ticker" if "fund_ticker" in g1.columns else "fund_id"
    held = g1.groupby(fund_col)["security_id"].agg(lambda x: sorted({str(v) for v in x if not hc._blank(v)})).to_dict()
    cand, curves = {}, {}
    for k, s in arms.items():
        g4, _ = hc.g4_window(s, lo.isoformat(), hi.isoformat(), dm._G4_COLUMNS)
        acts = ps._actions(s, lo.isoformat(), hi.isoformat())
        cand[k] = {(str(c["security_id"]), str(c["date"])[:10]) for c in dm.detect(g4, acts)}
        g4p, _ = hc.g4_window(s, lo.isoformat(), hi.isoformat(), ps._G4_COLUMNS)
        keys = sorted({str(v) for v in g4p["security_id"] if not hc._blank(v)} | {k2 for v in held.values() for k2 in v})
        curves[k] = ps.series(g4p, g1, keys, lo, hi, actions=acts)
    new = sorted(cand["B"] - cand["A"])
    gone = sorted(cand["A"] - cand["B"])
    stop = [c for c in new if c[1] in set(layer_dates)]
    print(f"day {day} | window {lo}..{hi} | layer dates {len(layer_dates)} | dramatic_move candidates A {len(cand['A'])} "
          f"B {len(cand['B'])} | new in B {len(new)} | gone in B {len(gone)} | NEW ON A LAYER DATE (STOP) {len(stop)}")
    for c in stop[:40]:
        print(f"  STOP candidate {c[0]} {c[1]}")

    def tally(cv, keys):
        t = {"market": 0, "implied": 0, "none": 0, "big_move_gaps": 0}
        for k in keys:
            r = cv.get(k)
            if not r:
                continue
            for _, _, code in r["points"]:
                t["market" if code == ps.SRC_MARKET else "implied" if code == ps.SRC_IMPLIED else "none"] += 1
            t["big_move_gaps"] += sum(1 for g in r["gaps"] if g["reason"] == ps.GAP_REASON_BIG_MOVE)
        return t

    rec = {"day": day, "window": [lo.isoformat(), hi.isoformat()], "layer_dates": len(layer_dates),
           "dramatic_move": {"A": len(cand["A"]), "B": len(cand["B"]), "new": [list(c) for c in new],
                             "gone": [list(c) for c in gone], "stop": [list(c) for c in stop]}, "price_series": {}}
    print(f"{'fund':<6} {'secs':>5} {'market A->B':>17} {'implied A->B':>17} {'none A->B':>17} {'bigmove A->B':>13}")
    for f in sorted(held):
        a, b = tally(curves["A"], held[f]), tally(curves["B"], held[f])
        rec["price_series"][str(f)] = {"securities": len(held[f]), "A": a, "B": b}
        print(f"{str(f):<6} {len(held[f]):>5} {a['market']:>8}->{b['market']:<8} {a['implied']:>8}->{b['implied']:<8} "
              f"{a['none']:>8}->{b['none']:<8} {a['big_move_gaps']:>5}->{b['big_move_gaps']:<6}")
    (out / f"heldtr_readers_{day}.json").write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
    print("VERDICT:", "STOP -- a new dramatic_move candidate on a held-tr date" if stop else "no new dramatic_move candidate on a held-tr date")
    return 3 if stop else 0


def publish(argv) -> int:
    layer = pathlib.Path(argv[0])
    apply = "--apply" in argv
    loc, live = sinks.LocalSink(str(layer)), sinks.S3Sink()
    objs = [u for u in loc.list(G4) if u.endswith(".parquet") and "/market-" in u]
    present = [u for u in objs if live.exists(u)]
    differ = [u for u in present if live.get(u) != loc.get(u)]
    for u in differ:
        print(f"DIFF: present and different {u}")
    print(f"objects in layer {len(objs)} | new {len(objs) - len(present)} | present-and-equal {len(present) - len(differ)} | "
          f"present-and-different {len(differ)}")
    if differ:
        print("REFUSED: a present object differs from the layer's; nothing is written")
        return 2
    wrote = skipped = 0
    for u in objs:
        if u in present:
            skipped += 1
            print(f"SKIP: exists (equal) {u}")
            continue
        if apply:
            live.put(u, loc.get(u), "application/octet-stream")
            wrote += 1
        print(f"{'PUT' if apply else 'PLAN'}: {u} ({len(loc.get(u))} bytes)")
    print(f"objects in layer {len(objs)} | written {wrote} | skipped (exist) {skipped} | apply {apply}")
    return 0


if __name__ == "__main__":
    sys.exit({"pull": pull, "replay": replay, "readers": readers, "publish": publish}[ACT](sys.argv[3:]))
