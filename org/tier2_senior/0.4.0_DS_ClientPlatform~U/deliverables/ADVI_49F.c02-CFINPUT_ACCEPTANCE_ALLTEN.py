"""ADVI_49F.c02-CFINPUT acceptance, first pass: the pre-registered ALL-TEN table @4a1fd3e09b.

PRE  = baseline c00 + baseline c02, both from the pinned pre-fix vintage, recovered by CONTENT.
POST = working-tree c00 + working-tree c02.
Same inputs, same date, so the delta is attributable to the two changes and nothing else.

The table is the acceptance instrument the TO names. It was registered as "EXPECTED after BOTH
fixes", so it tests defect 1 and defect 2 together -- which is what this TO plus c01-SIGNFIELD
deliver between them.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

RUNNERS = Path("data/assets/scripts/gold/runners_49f").resolve()
sys.path.insert(0, str(RUNNERS))
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

BASELINE_COMMIT = "b56bd2b7f0"
DATE = "2026-08-24"
M = ("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
     "C--Users-AndrewBerman-Desktop-ajb-workspace/9c462caa-4942-4b63-85d3-1783cfb1645f/"
     "scratchpad/mirror")

# root-cause doc s.5b @4a1fd3e09b: account -> (emitted, EXPECTED after BOTH fixes, defects)
ALL_TEN = {
    "0032486794": (690.560, 0.0000, "1"),
    "0013289888": (27.223, 0.0003, "1"),
    "0057178995": (10.543, 0.0335, "1+2"),
    "0050000151": (3.107, -0.0000, "2 only"),
    "0042335575": (1.578, 0.0008, "1+2"),
    "0012942467": (1.086, -0.0012, "1+2"),
    "0066766188": (-1.000, 0.0000, "2 only"),
    "0048403874": (-1.000, -0.0038, "1+2"),
    "0049284242": (-0.998, -0.0067, "1+2"),
    "0016371483": (-0.993, -0.0026, "1+2"),
}
work = Path(sys.argv[0]).resolve().parent / "_c02_head"
work.mkdir(exist_ok=True)
(work / "runner_common.py").write_bytes((RUNNERS / "runner_common.py").read_bytes())
(work / "POLICY_BLOCK.json").write_bytes((RUNNERS / "POLICY_BLOCK.json").read_bytes())
sys.path.insert(0, str(work))


def load(name, path, src=None):
    if src is not None:
        (work / f"{name}.py").write_bytes(src)
        path = work / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def at_baseline(name, rel):
    return load(name, None, subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:{rel}"], capture_output=True, check=True).stdout)


c00_pre = at_baseline("c00p", "data/assets/scripts/gold/runners_49f/c00_flow_ledger.py")
c02_pre = at_baseline("c02p", "data/assets/scripts/gold/runners_49f/c02_twr_engine.py")
c00_post = load("c00q", RUNNERS / "c00_flow_ledger.py")
c02_post = load("c02q", RUNNERS / "c02_twr_engine.py")
assert c00_pre.SCHEMA_VERSION == "1.1", "baseline is not pre-fix"
assert "in_kind_signed_value" not in (work / "c02p.py").read_text(encoding="utf-8"), \
    "baseline c02 already consumes the signed field -- wrong pin"
print(f"baseline {BASELINE_COMMIT} content-checked: c00 schema {c00_pre.SCHEMA_VERSION}, "
      f"c02 does not reference the signed field")

trn = rc.read_partition(f"{rc.SILVER}/fact_trn", DATE)
ref = rc.read_partition(f"{rc.OUT_ROOT}/reference/ref_txn_classification", DATE)
bnd = rc.read_partition(f"{rc.OUT_ROOT}/dimensions/dim_boundary", DATE)
px = rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_positions", DATE,
                       columns=["cusip", "closing_price"])
led_pre, _ = c00_pre.build_flow_ledger(trn[[c for c in c00_pre.TRN_COLS if c in trn.columns]],
                                       ref, bnd, px, asof=DATE)
led_post, _ = c00_post.build_flow_ledger(trn[[c for c in c00_post.TRN_COLS if c in trn.columns]],
                                         ref, bnd, px, asof=DATE)

cal = pd.read_parquet(f"{M}/dimensions/dim_calendar/date={DATE}/data.parquet")
prev_map = dict(zip(cal["trading_day"].astype(str), cal["prev_trading_day"].astype(str)))
fv = pd.concat([
    pd.read_parquet(f"{M}/canonical/canonical_valuation/date={d}/data.parquet",
                    columns=["account_id", "business_date", "fair_value"])
    for d in (DATE, prev_map[DATE])], ignore_index=True)
policy = c02_post.load_policy()

f_pre = c02_pre.flows_from_ledger(led_pre)
f_post, census = c02_post.flows_from_ledger(led_post, boundary="account")
d_pre = c02_pre.daily_returns(fv, f_pre, prev_map=prev_map, policy=policy)
d_post = c02_post.daily_returns(fv, f_post, prev_map=prev_map, policy=policy)
p = d_pre[d_pre["business_date"] == DATE].set_index("account_id")
q = d_post[d_post["business_date"] == DATE].set_index("account_id")

print(f"\nCF census [account grain]: {census['rows_admitted']} of {census['rows_total']} rows, "
      f"abs ${census['admitted_abs_value']:,.2f}")
print(f"\n{'account':<12}{'defects':>9}{'registered emitted':>20}{'OBSERVED pre':>16}"
      f"{'EXPECTED':>12}{'OBSERVED post':>16}{'verdict':>10}")
band_ok = 0
present = 0
testable_n = 0
for a, (emit_reg, expect, dfx) in ALL_TEN.items():
    if a not in q.index:
        print(f"{a:<12}{dfx:>9}{'':>20}{'ABSENT on this partition -- not evaluated':>50}")
        continue
    present += 1
    rp = p.loc[a, "r_net"] if a in p.index else None
    rq = q.loc[a, "r_net"]
    # TESTABILITY GATE, and it is load-bearing. A row is evidence only if the PRE arm actually
    # reproduces the registered EMITTED outlier on THIS partition. Two of the ten do not --
    # their outlier dates are elsewhere -- and for those the post value sits near zero because
    # it was ALREADY near zero, not because the fix moved it. Scoring those PASS on numeric
    # proximity is a control passing where it had nothing to discriminate: both arms rest on
    # the same truth, which is exactly the arms-collapse failure a control set must not have.
    testable = (rp is not None and not pd.isna(rp)
                and abs(float(rp) - emit_reg) <= max(0.01, abs(emit_reg) * 0.01))
    ok = (testable and not pd.isna(rq) and abs(float(rq) - expect) <= 0.005)
    band_ok += bool(ok)
    testable_n += bool(testable)
    fp = f"{float(rp) * 100:>14,.2f}%" if rp is not None and not pd.isna(rp) else f"{'n/a':>15}"
    fq = f"{float(rq) * 100:>14,.2f}%" if not pd.isna(rq) else f"{'n/a':>15}"
    print(f"{a:<12}{dfx:>9}{emit_reg * 100:>19,.1f}%{fp}{expect * 100:>11.2f}%{fq}"
          f"{('PASS' if ok else 'FAIL') if testable else 'NOT-TESTABLE':>14}")
print(f"\nIN-BAND vs the pre-registered expectation: {band_ok} of {testable_n} TESTABLE "
      f"({present} present on this partition, {len(ALL_TEN)} registered).")
print("NOT-TESTABLE = the PRE arm does not reproduce the registered EMITTED outlier here, so")
print("this partition cannot judge that row -- its outlier date is elsewhere. Those rows are")
print("neither passes nor failures; counting them either way would misstate the evidence.")

# CF-3 first cut: the magnitude distribution the census could not give
both = p[["r_net"]].join(q[["r_net"]], lsuffix="_pre", rsuffix="_post", how="inner").dropna()
moved = both[(both["r_net_pre"] - both["r_net_post"]).abs() > 1e-9]
print(f"\nCF-3 MAGNITUDE DISTRIBUTION on {DATE} -- accounts whose r_net MOVED: "
      f"{len(moved)} of {len(both)} computable")
if len(moved):
    d = (moved["r_net_pre"] - moved["r_net_post"]).abs()
    for q_ in (0.5, 0.9, 0.99, 1.0):
        print(f"    |delta r_net| q{q_:<5}: {d.quantile(q_) * 100:>12,.2f} pp")
    print(f"    accounts moving >1pp: {int((d > 0.01).sum())} | >10pp: {int((d > 0.10).sum())} "
          f"| >100pp: {int((d > 1.0).sum())}")
