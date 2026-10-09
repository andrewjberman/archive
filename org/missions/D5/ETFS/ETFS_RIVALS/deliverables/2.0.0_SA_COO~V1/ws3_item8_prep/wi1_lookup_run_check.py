"""RIV-wi-1 AC1 (CTO ruling ADDENDUM 6 @04214e638c) -- the sweep's dramatic-move step, `dramatic_move.run_for_day`.

    python wi1_lookup_run_check.py      (run from the repository root)

Calls `run_for_day(day, sink, g4=..., actions=..., search=<scripted>, cap=<n>)` on a LocalSink in a temp dir, with
closes for four securities: TKM falls 15x on 2026-10-07 (the Tokio Marine shape), FLT moves 1%, and DRA and DRB each fall
4x. The scripted search answers a split for TKM, nothing for DRA/DRB, and records every query.
ARM A: TKM is searched, one corporate-action row is written with a source_url, and the report counts it.
ARM B: FLT (no discontinuity) draws 0 searches.
ARM C: cap=2 with three candidates -> 2 candidates searched, the report's `capped` is 1, and a line naming the cap prints.
ARM D: a search that raises -> run_for_day returns (no exception), `failed` >= 1, nothing written.
Exit 0 = PASS, 1 = FAIL.
"""
import contextlib
import io
import os
import sys
import tempfile

import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "data", "etfs", "scripts"))
from rivalfunds import dramatic_move as dm  # noqa: E402
from rivalfunds import sinks  # noqa: E402

DAY = "2026-10-08"
rows = []
for sid, name, prices in (("8766 JP Equity", "Tokio Marine Holdings Inc", [7500.0, 7600.0, 500.0, 505.0]),
                          ("FLT US Equity", "Flat Co", [100.0, 101.0, 100.0, 101.0]),
                          ("DRA US Equity", "Drop A Co", [80.0, 81.0, 20.0, 20.5]),
                          ("DRB US Equity", "Drop B Co", [60.0, 61.0, 15.0, 15.2])):
    for d, px in zip(("2026-10-02", "2026-10-06", "2026-10-07", "2026-10-08"), prices):
        rows.append({"security_id": sid, "security_name": name, "date": d, "px_close": px})
g4 = pd.DataFrame(rows)
actions = pd.DataFrame(columns=["security_id", "action_type", "ex_date", "ratio"])

if not hasattr(dm, "run_for_day"):
    print("FAIL: dramatic_move.run_for_day does not exist")
    print("WI1 RESULT: FAIL 1 failures")
    sys.exit(1)


def scripted(queries):
    def search(q):
        queries.append(q)
        if "Tokio Marine" in q and "split" in q:
            return [{"title": "Tokio Marine Holdings announces 15-for-1 stock split",
                     "url": "https://example.test/tokio-split",
                     "snippet": "Tokio Marine Holdings Inc will conduct a 15-for-1 stock split effective October 7, 2026."}]
        return []
    return search


def boom(q):
    raise RuntimeError("SERP FAILED: transport")


def run(search, cap, label):
    tmp = tempfile.mkdtemp(prefix=f"wi1-{label}-")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rep = dm.run_for_day(DAY, sinks.LocalSink(tmp), g4=g4, actions=actions, search=search, cap=cap)
    written = [os.path.join(r, f) for r, _, fs in os.walk(tmp) for f in fs if f.endswith(".parquet")]
    return rep or {}, written, out.getvalue()


fails = []
qa = []
rep, written, printed = run(scripted(qa), 10, "a")
print(f"ARM A/B: report {rep}; files {len(written)}; queries {qa}")
if not any("Tokio Marine" in q for q in qa):
    fails.append("A: Tokio Marine was not searched")
tk = [pd.read_parquet(w) for w in written]
tk = pd.concat(tk) if tk else pd.DataFrame()
if len(tk) != 1 or "source_url" not in tk.columns or str(tk["source_url"].iloc[0]) != "https://example.test/tokio-split":
    fails.append(f"A: expected ONE corporate-action row with its source_url, found {len(tk)}")
if any("Flat Co" in q or "FLT" in q for q in qa):
    fails.append("B: a name with no discontinuity was searched")
qc = []
rep, written, printed = run(scripted(qc), 2, "c")
searched = {n for n in ("Tokio Marine", "Drop A", "Drop B") if any(n in q for q in qc)}
print(f"ARM C: report {rep}; candidates searched {sorted(searched)}; printed {printed.strip()[:200]!r}")
if len(searched) != 2 or int(rep.get("capped", -1)) != 1 or "cap" not in printed.lower():
    fails.append("C: cap=2 over three candidates did not search exactly 2, report capped 1 and print the cap")
try:
    rep, written, printed = run(boom, 10, "d")
    print(f"ARM D: report {rep}; files {len(written)}")
    if int(rep.get("failed", 0)) < 1 or written:
        fails.append("D: a failed search was not counted as failed, or something was written")
except Exception as ex:  # noqa: BLE001
    fails.append(f"D: run_for_day raised {type(ex).__name__}: {ex}")
for f in fails:
    print("FAIL:", f)
print(f"WI1 RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
