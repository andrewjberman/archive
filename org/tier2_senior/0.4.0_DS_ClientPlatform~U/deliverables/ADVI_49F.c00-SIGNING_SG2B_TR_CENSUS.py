"""SG-2b: THE TR CENSUS. Does a consistent direction convention exist for TR-coded code-rule
INTERNAL legs at n > 3?

Approved now by CTO 76788 s.2 as free inside the P14-STAMP gating window, with a LATE-JOIN rule:
a consistent convention found BEFORE the SG build reaches its deploy step lets TR ride the same
act; after that it is banked. So this runs early on purpose.

THE TEST, and it is the same one that answered FC -- restrict to accounts whose unsigned legs are
ALL tr_cd=TR (no mixing, which is what confounded my first pass), then ask whether the signed sum
implied by debit_credit reproduces the account's actual EMV-BMV move.

  |implied| / |move| near 1  -> the MAGNITUDE is recoverable
  implied/move consistently +1 -> the FC convention (CREDIT=+1/DEBIT=-1) holds for TR too
  implied/move consistently -1 -> TR is sign-INVERTED relative to FC; still designable
  no consistency               -> not designable from debit_credit; TR stays banked

⛔ A NEGATIVE RESULT IS A REAL RESULT HERE and costs only the census -- that is exactly why the
asymmetric payoff made it worth running. It must not be dressed up either way.

Read-only. Reads served artifacts (flow_ledger + twr_daily + canonical_valuation + fact_trn).
"""
import json
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
led_dates = rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/flow_ledger")
twr_dates = set(rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/twr_daily"))
val_dates = set(rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/canonical_valuation"))
usable = [d for d in led_dates if d in twr_dates and d in val_dates]
step = max(1, len(usable) // N)
sample = usable[::step][:N]
print(f"partitions with ledger+twr+valuation: {len(usable)} | sampling {len(sample)}")
print(f"span {sample[0]} .. {sample[-1]}\n")

recs = []
for D in sample:
    try:
        led = rc.read_partition(f"{rc.OUT_ROOT}/canonical/flow_ledger", D)
        twr = rc.read_partition(f"{rc.OUT_ROOT}/canonical/twr_daily", D)
        val = rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_valuation", D,
                                columns=["account_id", "fair_value"])
        trn = rc.read_partition(f"{rc.SILVER}/fact_trn", D,
                                columns=["account_id", "tr_cd", "debit_credit", "gross_amount"])
    except Exception as exc:
        print(f"  {D}: unreadable ({type(exc).__name__}) -- SKIPPED, not counted")
        continue
    for f in (led, twr, val):
        f["acct"] = f["account_id"].astype(str).str.zfill(10)
    trn["acct"] = trn["account_id"].astype(str).str.strip().str.zfill(10)
    amt = pd.to_numeric(led["signed_amount"], errors="coerce").fillna(0.0)
    uns = led[(led["final_class"] == "INTERNAL") & (led["resolution_provenance"] == "code-rule")
              & (amt == 0.0) & (~led["is_in_kind"].astype(bool))]
    ok = twr[twr["status"] == "OK"].copy()
    ok["r"] = pd.to_numeric(ok["r_net"], errors="coerce")
    ok["cf"] = pd.to_numeric(ok["cf_net"], errors="coerce").fillna(0.0)
    cand = ok[(ok["cf"] == 0.0) & (ok["r"].abs() > 0.02) & (ok["acct"].isin(set(uns["acct"])))]
    if not len(cand):
        continue
    trn["g"] = pd.to_numeric(trn["gross_amount"], errors="coerce").fillna(0.0)
    dc = trn["debit_credit"].fillna("").astype(str).str.strip().str.upper().str[:1]
    trn["sp"] = trn["g"].abs() * dc.map({"C": 1.0, "D": -1.0}).fillna(0.0)
    vmap = dict(zip(val["acct"], pd.to_numeric(val["fair_value"], errors="coerce")))
    n_tr = 0
    for a in cand["acct"]:
        legs = trn[trn["acct"] == a]
        cls = set(legs["tr_cd"].astype(str).str.strip())
        if cls != {"TR"}:
            continue                      # TR-ONLY: the confound removed
        emv = vmap.get(a)
        if emv is None or pd.isna(emv):
            continue
        r = float(cand[cand["acct"] == a]["r"].iloc[0])
        if (1.0 + r) == 0:
            continue
        bmv = emv / (1.0 + r)
        move = emv - bmv
        imp = float(legs["sp"].sum())
        absg = float(legs["g"].abs().sum())
        if abs(move) < 1.0 or absg < 1.0:
            continue                      # nothing to explain / nothing to explain it with
        recs.append({"d": D, "a": a, "r": r, "move": move, "implied": imp,
                     "abs_gross": absg, "legs": int(len(legs)),
                     "ratio": imp / move, "mag": absg / abs(move)})
        n_tr += 1
    if n_tr:
        print(f"  {D}: {n_tr} TR-only candidate(s)")

print(f"\n{'='*76}")
if not recs:
    print("NO TR-ONLY CANDIDATES in this sample. The convention question cannot be answered")
    print("from this evidence -- which is itself the answer: TR is not designable now.")
    sys.exit(0)
df = pd.DataFrame(recs)
print(f"TR-ONLY CANDIDATES: {len(df)} across {df['d'].nunique()} partitions "
      f"(previous pass had 3 -- the n>3 bar CTO set is {'MET' if len(df) > 3 else 'NOT met'})")
same = int((df["ratio"] > 0).sum())
inv = int((df["ratio"] < 0).sum())
near1 = int(((df["ratio"] > 0.8) & (df["ratio"] < 1.25)).sum())
nearm1 = int(((df["ratio"] < -0.8) & (df["ratio"] > -1.25)).sum())
magok = int(((df["mag"] > 0.8) & (df["mag"] < 1.25)).sum())
print(f"  implied/move  SAME sign {same} | INVERTED {inv}")
print(f"  ratio within 0.8..1.25 of +1 : {near1}   (FC convention holds for TR)")
print(f"  ratio within 0.8..1.25 of -1 : {nearm1}  (TR sign-INVERTED vs FC)")
print(f"  |gross|/|move| within 0.8..1.25: {magok}  (MAGNITUDE recoverable regardless of sign)")
print("\n  the candidates, largest |move| first:")
for _, x in df.reindex(df["move"].abs().sort_values(ascending=False).index).head(12).iterrows():
    print(f"    {x['d']} {x['a']}  r {x['r']*100:+8.2f}%  move {x['move']:>14,.2f}  "
          f"implied {x['implied']:>14,.2f}  ratio {x['ratio']:>7.2f}  |g|/|mv| {x['mag']:>6.2f}")
verdict = ("CONSISTENT +1 -- FC convention holds for TR" if near1 >= max(4, 0.7*len(df)) else
           "CONSISTENT -1 -- TR is sign-inverted" if nearm1 >= max(4, 0.7*len(df)) else
           "NOT CONSISTENT -- not designable from debit_credit on this evidence")
print(f"\n  VERDICT: {verdict}")
print("  (bar: a convention needs >=70% of candidates and at least 4, both stated in advance")
print("   so the threshold is not chosen after seeing the numbers)")
print(json.dumps(recs, indent=2, default=str)[:1200])
