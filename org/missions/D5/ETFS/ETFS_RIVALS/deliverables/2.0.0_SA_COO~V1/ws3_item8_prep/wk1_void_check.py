"""RIV-wk-1 AC1 (CTO half condition 11, @63bdddfbb9) -- a stored corporate-action row can be VOIDED without a delete.

    python wk1_void_check.py      (run from the repository root; LocalSink in a temp dir; no S3, no search)

Writes two inferred split rows with `dramatic_move.write_rows` into a LocalSink (Tokio Marine 8766 JP Equity 15-for-1
ex 2026-10-07; DRA US Equity 4-for-1 ex 2026-10-06), then:
ARM A: `price_series._adjustments(price_series._actions(...))` adjusts both keys.
ARM B: the CLI `python -m rivalfunds.dramatic_move void --sink local:<dir> --revision <Tokio row's revision>
       --security-id "8766 JP Equity" --reason <text>` exits 0 and writes ONE new object whose name starts
       `actions-void-` under gold corporate_actions; the action object is untouched (append-only, nothing deleted).
ARM C: after the void, Tokio Marine is NOT adjusted and DRA (the control) still is.
ARM D: the void object is never read as an action: `_actions` returns no row from it (no row without an event_type).
Exit 0 = PASS, 1 = FAIL.
"""
import datetime as dt
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(os.getcwd())
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
from rivalfunds import dramatic_move as dm  # noqa: E402
from rivalfunds import price_series as ps  # noqa: E402
from rivalfunds import sinks  # noqa: E402

tmp = tempfile.mkdtemp(prefix="wk1-")
s = sinks.LocalSink(tmp)
now = dt.datetime(2026, 10, 8, 13, 5, tzinfo=dt.timezone.utc)
rows = []
for sid, ratio, ex, prior in (("8766 JP Equity", 15.0, dt.date(2026, 10, 7), "2026-10-06"),
                              ("DRA US Equity", 4.0, dt.date(2026, 10, 6), "2026-10-02")):
    cand = {"security_id": sid, "date": ex.isoformat(), "prior_date": prior, "prior_close": 100.0, "close": 100.0 / ratio}
    rows.append(dm._row(cand, "split", ratio, f"{int(ratio)}-for-1", {"url": f"https://example.test/{sid[:4]}"}, ex, "q", now))
tk_uri = dm.write_rows(s, rows[:1], "2026-10-08")
dr_uri = dm.write_rows(s, rows[1:], "2026-10-08")
start, end = dt.date(2026, 9, 1), dt.date(2026, 10, 9)
wanted = {"8766_JP_Equity", "DRA_US_Equity"}


def adjusted():
    acts = ps._actions(s, start.isoformat(), end.isoformat())
    return set(ps._adjustments(acts, wanted, start, end)), acts


fails = []
keys, acts = adjusted()
print(f"ARM A: adjusted keys {sorted(keys)}; action rows {len(acts)}")
if keys != wanted:
    fails.append("A: the two stored splits do not both adjust before the void")
tk_rev = str(acts[acts["security_id"].astype(str) == "8766 JP Equity"]["revision"].iloc[0]) if len(acts) else ""
before = sorted(str(p.relative_to(tmp)) for p in pathlib.Path(tmp).rglob("*.parquet"))
r = subprocess.run([sys.executable, "-m", "rivalfunds.dramatic_move", "void", "--sink", f"local:{tmp}", "--revision", tk_rev,
                    "--security-id", "8766 JP Equity", "--reason", "wk1 check: a wrong find"],
                   cwd=str(ROOT / "data" / "etfs" / "scripts"), capture_output=True, text=True)
after = sorted(str(p.relative_to(tmp)) for p in pathlib.Path(tmp).rglob("*.parquet"))
new = [p for p in after if p not in before]
print(f"ARM B: CLI rc {r.returncode}; new objects {new}; stderr {r.stderr.strip()[-200:]!r}")
if r.returncode != 0 or len(new) != 1 or not pathlib.Path(new[0]).name.startswith("actions-void-") or not set(before) <= set(after):
    fails.append("B: the void CLI did not write exactly one new actions-void-* object, append-only")
keys, acts = adjusted()
print(f"ARM C: adjusted keys after the void {sorted(keys)}")
if "8766_JP_Equity" in keys or "DRA_US_Equity" not in keys:
    fails.append("C: the voided Tokio row still adjusts, or the control DRA row stopped adjusting")
if len(acts) and ("event_type" not in acts.columns or acts["event_type"].isna().any()):
    fails.append("D: the void object was read as action rows")
for f in fails:
    print("FAIL:", f)
print(f"WK1 RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
