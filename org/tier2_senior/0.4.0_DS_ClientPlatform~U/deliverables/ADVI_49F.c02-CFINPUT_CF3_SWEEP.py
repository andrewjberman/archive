"""CF-3 magnitude distribution, multi-partition -- AND the sensitivity that lets 1.0.0_SA_CTO
rule the provenance fork against numbers instead of against a principle alone.

Computes r_net PRE vs POST on each sampled partition under TWO readings of the account-grain
filter, differing ONLY in whether `code-rule` INTERNAL legs (which establish no counterparty)
are admitted:

  STRICT  = EXTERNAL + INTERNAL{pair-match, text-counterpart}   <- what is implemented
  WIDE    = STRICT + INTERNAL{code-rule}                        <- the class-grain reading

Everything else is held constant. The delta between them IS the fork's price.
Read-only against S3; writes nothing.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUNNERS = Path("data/assets/scripts/gold/runners_49f").resolve()
sys.path.insert(0, str(RUNNERS))
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

BASELINE_COMMIT = "b56bd2b7f0"
work = Path(sys.argv[0]).resolve().parent / "_cf3"
work.mkdir(exist_ok=True)
(work / "runner_common.py").write_bytes((RUNNERS / "runner_common.py").read_bytes())
(work / "POLICY_BLOCK.json").write_bytes((RUNNERS / "POLICY_BLOCK.json").read_bytes())
sys.path.insert(0, str(work))


def load(name, path=None, src=None):
    if src is not None:
        (work / f"{name}.py").write_bytes(src)
        path = work / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def at_base(name, rel):
    return load(name, src=subprocess.run(["git", "show", f"{BASELINE_COMMIT}:{rel}"],
                                         capture_output=True, check=True).stdout)


c00_pre = at_base("c00b", "data/assets/scripts/gold/runners_49f/c00_flow_ledger.py")
c02_pre = at_base("c02b", "data/assets/scripts/gold/runners_49f/c02_twr_engine.py")
c00_post = load("c00n", RUNNERS / "c00_flow_ledger.py")
c02_post = load("c02n", RUNNERS / "c02_twr_engine.py")
assert c00_pre.SCHEMA_VERSION == "1.1"
policy = c02_post.load_policy()

val_dates = set(rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/canonical_valuation"))
trn_dates = rc.list_partition_dates(f"{rc.SILVER}/fact_trn")
cal = None
usable = []
for d in reversed(trn_dates):
    if d in val_dates:
        usable.append(d)
    if len(usable) >= 40:
        break
print(f"denominator context: fact_trn partitions={len(trn_dates)}, "
      f"canonical_valuation partitions={len(val_dates)}")

rows, per_date = [], []
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
picked = 0
for d in usable:
    if picked >= N:
        break
    try:
        trn = rc.read_partition(f"{rc.SILVER}/fact_trn", d)
        ref = rc.read_partition(f"{rc.OUT_ROOT}/reference/ref_txn_classification", d)
        bnd = rc.read_partition(f"{rc.OUT_ROOT}/dimensions/dim_boundary", d)
        px = rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_positions", d,
                               columns=["cusip", "closing_price"])
        cal = rc.read_partition(f"{rc.OUT_ROOT}/dimensions/dim_calendar", d)
    except Exception as exc:
        print(f"  {d}: input unavailable ({type(exc).__name__}) -- SKIPPED, not counted")
        continue
    prev_map = dict(zip(cal["trading_day"].astype(str), cal["prev_trading_day"].astype(str)))
    prev = prev_map.get(d)
    if prev not in val_dates:
        print(f"  {d}: D-1 {prev} valuation absent -- SKIPPED (every row would REFUSE)")
        continue
    fv = pd.concat([rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_valuation", x,
                                      columns=["account_id", "business_date", "fair_value"])
                    for x in (d, prev)], ignore_index=True)
    led_pre, _ = c00_pre.build_flow_ledger(
        trn[[c for c in c00_pre.TRN_COLS if c in trn.columns]], ref, bnd, px, asof=d)
    led_post, _ = c00_post.build_flow_ledger(
        trn[[c for c in c00_post.TRN_COLS if c in trn.columns]], ref, bnd, px, asof=d)

    def ret(c02mod, led, **kw):
        f = c02mod.flows_from_ledger(led, **kw)
        f = f[0] if isinstance(f, tuple) else f
        dr = c02mod.daily_returns(fv, f, prev_map=prev_map, policy=policy)
        return dr[dr["business_date"] == d].set_index("account_id")["r_net"]

    r_pre = ret(c02_pre, led_pre)
    _, cen = c02_post.flows_from_ledger(led_post, boundary="account")
    r_strict = ret(c02_post, led_post, boundary="account")
    orig = c02_post.INTER_ACCOUNT_PROVENANCE
    c02_post.INTER_ACCOUNT_PROVENANCE = frozenset(orig | {"code-rule"})
    r_wide = ret(c02_post, led_post, boundary="account")
    c02_post.INTER_ACCOUNT_PROVENANCE = orig

    j = pd.DataFrame({"pre": r_pre, "strict": r_strict, "wide": r_wide}).dropna()
    ds = (j["pre"] - j["strict"]).abs()
    dw = (j["strict"] - j["wide"]).abs()
    per_date.append({
        "date": d, "computable": int(len(j)),
        "moved_by_fix": int((ds > 1e-9).sum()),
        "moved_gt_1pp": int((ds > 0.01).sum()),
        "max_move_pp": round(float(ds.max() * 100), 2) if len(ds) else 0.0,
        "fork_accounts_differing": int((dw > 1e-9).sum()),
        "fork_max_pp": round(float(dw.max() * 100), 4) if len(dw) else 0.0,
        # CTO 76329: the residue is named all the way up. Unestablished code-rule legs stay
        # EXCLUDED, and the P1.5 re-grade report carries their per-day dollar size WITH its
        # denominator so the serve read is made with it in view, never a silent drop.
        "residual_excluded_abs_usd": cen["in_scope_class_but_no_counterparty"]["abs_value"],
        "residual_rows": cen["in_scope_class_but_no_counterparty"]["rows"],
        "admitted_abs_usd": cen["admitted_abs_value"],
    })
    rows.append(ds)
    picked += 1
    p = per_date[-1]
    print(f"  {d}: computable={p['computable']:>5} moved={p['moved_by_fix']:>4} "
          f">1pp={p['moved_gt_1pp']:>4} max={p['max_move_pp']:>12,.2f}pp | "
          f"FORK differs on {p['fork_accounts_differing']:>4} accounts, "
          f"max {p['fork_max_pp']:>10,.4f}pp")

allmoves = pd.concat(rows) if rows else pd.Series(dtype=float)
moved = allmoves[allmoves > 1e-9]
print(f"\n===== CF-3, pooled over {picked} partitions "
      f"(of {len(trn_dates)} fact_trn partitions -- a SAMPLE, not the estate)")
print(f"  account-days computable : {int(len(allmoves)):,}")
print(f"  account-days MOVED      : {int(len(moved)):,} "
      f"({100.0 * len(moved) / max(1, len(allmoves)):.3f}%)")
if len(moved):
    for q in (0.25, 0.5, 0.75, 0.9, 0.99, 1.0):
        print(f"    |delta r_net| q{q:<5}: {moved.quantile(q) * 100:>14,.2f} pp")
    for t, lbl in ((0.01, ">1pp"), (0.10, ">10pp"), (1.0, ">100pp"), (10.0, ">1000pp")):
        print(f"    moved {lbl:<8}: {int((moved > t).sum()):>6}")
tot_fork = sum(p["fork_accounts_differing"] for p in per_date)
print(f"\n===== THE FORK'S PRICE, measured: STRICT vs WIDE differ on {tot_fork} account-days "
      f"across {picked} partitions")
print("  (WIDE = also admit code-rule INTERNAL, which establishes no counterparty)")
res = sum(p["residual_excluded_abs_usd"] for p in per_date)
adm = sum(p["admitted_abs_usd"] for p in per_date)
print("")
print("===== THE RESIDUE, per CTO 76329 (carried, never silently dropped)")
print(f"  EXCLUDED code-rule INTERNAL, pooled abs value : ${res:>18,.2f}")
print(f"  ADMITTED flow, pooled abs value              : ${adm:>18,.2f}")
print(f"  residue as a share of admitted flow          : {100.0*res/max(1e-9,adm):>17.3f}%")
print(f"  per-day mean residue                         : ${res/max(1,picked):>18,.2f}"
      f"   (denominator: {picked} partitions)")
out = {"partitions_sampled": picked, "fact_trn_partitions_total": len(trn_dates),
       "per_date": per_date, "residual_pooled_abs_usd": round(res,2),
       "admitted_pooled_abs_usd": round(adm,2)}
Path(sys.argv[2] if len(sys.argv)>2 else "cf3.json").write_text(
    json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(per_date, indent=2))
