"""RIV-h-4 AC2 (hop-9 ruling a, the seam against REAL G1) -- on the served G1 for PFOE's window ending 2026-09-28, the merged G5
inference reads Universal Music Group (91377B109) as an EXIT and Quanta Services (74762E102) as an ENTRY, never an ID-CHANGE pair.

READ-ONLY S3: the newest served G1 object of each date (revision.newest), PFOE rows only; the window starts on PFOE's own prior
report date. `gold_trade_schedule.infer_trades` runs locally on those rows.
  - no row of confidence ID-CHANGE names 91377B109 or 74762E102;
  - 91377B109 appears as an exit and 74762E102 as an entry;
  - control: the window has trades at all (the read is not empty)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

FUND, END = "PFOE", "2026-09-28"
UMG, PWR = "91377B109", "74762E102"


def run(v):
    c.setup_path()
    from rivalfunds import gold_trade_schedule as g

    prior = c.served_prior_date(FUND, END)
    df = c.served_g1_fund(FUND, [prior, END]) if prior else None
    print(f"{FUND} window {prior} -> {END}: {0 if df is None else len(df)} G1 rows")
    v.check(df is not None and len(df) > 0, "control: the served G1 window is not empty")
    t = g.infer_trades(df)
    keys = lambda r: {str(r.get("security_key")), str(r.get("counterpart_security_key"))}  # noqa: E731
    named = [r for r in t.to_dict("records") if any(x in " ".join(keys(r)) for x in (UMG, PWR))]
    for r in named:
        print("  ", r.get("action"), r.get("confidence"), r.get("security_key"), "->", r.get("counterpart_security_key"))
    v.check(len(t) > 0, "control: the window infers trades")
    v.check(not any(r.get("confidence") == "ID-CHANGE" for r in named), "no ID-CHANGE row names UMG or PWR")
    acts = {(r.get("action"), x) for r in named for x in (UMG, PWR) if x in str(r.get("security_key"))}
    v.check(("exit", UMG) in acts and ("entry", PWR) in acts, "UMG is an exit and PWR an entry")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
