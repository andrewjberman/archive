"""KEEPER #10, THE SECOND HALF (CTO 76744 s.1): is the direction RECOVERABLE at all?

If fact_trn does not carry enough to sign these legs, the fix option does not exist and the
materiality decision simplifies to "bank it". So this does not ask how often the defect appears
-- that is the rate, already measured -- it asks whether a signing rule could exist.

THE TEST, and it is a real falsifier rather than a look: for accounts that (a) hold unsigned
code-rule INTERNAL cash legs and (b) have a computable return, take the candidate direction
signal from fact_trn's debit_credit and ask whether the SIGNED SUM it implies PREDICTS the
account's actual EMV-BMV move. If a convention exists, one of the two sign assignments should
track the move; if neither does, the column is not direction-semantic on these rows and the
value is genuinely unrecoverable from it.

Two arms so the answer cannot be manufactured by picking a convention after the fact:
  ARM +  CREDIT=+1 / DEBIT=-1   (the F-AMT convention c00 already uses on FC rows)
  ARM -  the inverse
A convention that WORKS should show a strong correlation on one arm. Both weak = unrecoverable
from debit_credit, which is the finding that closes the option.

Read-only.
"""
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

DATES = ["2026-03-24", "2026-02-04", "2025-12-01", "2026-04-09"]
rows = []
for D in DATES:
    try:
        led = rc.read_partition(f"{rc.OUT_ROOT}/canonical/flow_ledger", D)
        twr = rc.read_partition(f"{rc.OUT_ROOT}/canonical/twr_daily", D)
        trn = rc.read_partition(f"{rc.SILVER}/fact_trn", D,
                                columns=["account_id", "tr_cd", "debit_credit", "gross_amount"])
    except Exception as exc:
        print(f"  {D}: unreadable ({type(exc).__name__}) -- SKIPPED")
        continue
    for f in (led, twr):
        f["acct"] = f["account_id"].astype(str).str.zfill(10)
    trn["acct"] = trn["account_id"].astype(str).str.strip().str.zfill(10)
    amt = pd.to_numeric(led["signed_amount"], errors="coerce").fillna(0.0)
    uns = led[(led["final_class"] == "INTERNAL")
              & (led["resolution_provenance"] == "code-rule")
              & (amt == 0.0) & (~led["is_in_kind"].astype(bool))]
    ok = twr[twr["status"] == "OK"].copy()
    ok["r"] = pd.to_numeric(ok["r_net"], errors="coerce")
    ok["cf"] = pd.to_numeric(ok["cf_net"], errors="coerce").fillna(0.0)
    # candidates: computable, no attributed flow, holding unsigned legs, non-trivial move
    cand = ok[(ok["cf"] == 0.0) & (ok["r"].abs() > 0.05) & (ok["acct"].isin(set(uns["acct"])))]
    print(f"\n=== {D}: {len(cand)} candidate accounts (computable, cf=0, |r|>5%, unsigned legs)")
    if not len(cand):
        continue
    trn["g"] = pd.to_numeric(trn["gross_amount"], errors="coerce").fillna(0.0)
    dc = trn["debit_credit"].fillna("").astype(str).str.strip().str.upper().str[:1]
    trn["sgn_plus"] = trn["g"].abs() * dc.map({"C": 1.0, "D": -1.0}).fillna(0.0)
    codes = {}
    for a in cand["acct"]:
        legs = trn[trn["acct"] == a]
        if not len(legs):
            continue
        for c in legs["tr_cd"].astype(str).str.strip().unique():
            codes[c] = codes.get(c, 0) + 1
        implied = float(legs["sgn_plus"].sum())
        rows.append({"date": D, "acct": a, "r": float(cand[cand["acct"] == a]["r"].iloc[0]),
                     "implied_plus": implied,
                     "legs": len(legs), "abs_gross": float(legs["g"].abs().sum())})
    print(f"    tr_cd values on their legs: {codes}")

if rows:
    df = pd.DataFrame(rows)
    print(f"\n{'='*74}\nRECOVERABILITY TEST over {len(df)} candidate account-days")
    # does the implied signed sum agree in SIGN with the return's direction?
    agree_plus = int(((df["implied_plus"] > 0) == (df["r"] > 0)).sum())
    agree_minus = int(((-df["implied_plus"] > 0) == (df["r"] > 0)).sum())
    n = len(df)
    print(f"  ARM +  CREDIT=+1/DEBIT=-1 : sign agrees with the return on {agree_plus} of {n}"
          f"  ({100.0*agree_plus/n:.0f}%)")
    print(f"  ARM -  the inverse        : sign agrees with the return on {agree_minus} of {n}"
          f"  ({100.0*agree_minus/n:.0f}%)")
    print("  (a real convention shows one arm strongly >50%; both near 50% means the column")
    print("   is not direction-semantic on these rows and the value is UNRECOVERABLE from it)")
    print("\n  the candidates, largest |r| first:")
    for _, x in df.reindex(df["r"].abs().sort_values(ascending=False).index).head(8).iterrows():
        print(f"    {x['date']} {x['acct']}  r {x['r']*100:+9.2f}%  legs {int(x['legs']):>3}  "
              f"|gross| {x['abs_gross']:>13,.2f}  implied(+) {x['implied_plus']:>13,.2f}")
else:
    print("\nNo candidates found -- the option question cannot be answered from this sample.")
