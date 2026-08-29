"""G-1/G-4 instrument: the SIGNED gross-minus-net gap on the STORED twr_daily leg.

0.4.0_DS_ClientPlatform~N, ADVI_49F.c02-GROSSLEG.

DELIBERATELY SIGNED EVERYWHERE. No abs(), no !=-only census: the whole content of the
observation is DIRECTION, and an absolute value is the one operation that discards it
(3.0.0_SA_CVO 83567 s.3, disclosing the blindness in its own instrument).

Partitions chosen so the coverage does NOT rest on the reporter's window
(0.4.0_DS_ClientPlatform~C read flow_ledger date=2026-07-07 and twr_daily
2026-07-01..08-28). This reads 15: a 12-point EVERY-45TH spread across the whole
534-date history (2024-07-08..2026-06-26, entirely OUTSIDE that window) plus the three
most recent (2026-08-26..28). Denominators printed per partition.

SCHEMA VARIANCE IS HANDLED, NOT ASSUMED AWAY: c02 only writes bmv/emv/cf_net/cf_gross
onto OK rows, so a partition with zero OK rows carries none of them. Those partitions
are named as NOT-EVALUABLE-BY-SCHEMA with their status census rather than dropped
silently -- a partition that could not be asked is not a partition that answered NO.
"""
import os

import pandas as pd

# RE-RUN NOTE: ROOT is this file's own directory, so the partitions must be staged BESIDE
# it as twr_daily_<date>/ and flow_ledger_<date>/. They are deliberately NOT committed --
# they are S3 artifacts, not repo content. Restage with:
#   aws s3 cp s3://opal-data-49financial/gold/advi/canonical/{twr_daily,flow_ledger}/date=<d>/ <dir>/ --recursive

ROOT = os.path.dirname(os.path.abspath(__file__))
DATES = ['2024-07-08', '2024-09-10', '2024-11-12', '2025-01-17', '2025-03-25',
         '2025-05-29', '2025-08-04', '2025-10-07', '2025-12-10', '2026-02-17',
         '2026-04-22', '2026-06-26', '2026-08-26', '2026-08-27', '2026-08-28']
CFCOLS = ("bmv", "emv", "cf_net", "cf_gross")


def rule(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------- LEG 1: fee sign
rule("LEG 1 -- FEE-MANAGEMENT signed_amount SIGN, with a mixed-sign CONTROL")
print("The whole `cf_gross > cf_net` result hangs on this sign. If FEE-MANAGEMENT")
print("signed_amount were POSITIVE, `cf_net - fee_cf` would be the correct build and")
print("outcome (c) would be live.")
L = {"rows": 0, "fee": 0, "neg": 0, "pos": 0, "zero": 0,
     "cneg": 0, "cpos": 0, "czero": 0, "cother": 0, "parts_with_fee": 0}
for d in DATES:
    led = pd.read_parquet(f"{ROOT}/flow_ledger_{d}/data.parquet")
    amt = pd.to_numeric(led["signed_amount"], errors="coerce").fillna(0.0)
    fee = led["final_class"] == "FEE-MANAGEMENT"
    f, o = amt[fee], amt[~fee]
    L["rows"] += len(led)
    L["fee"] += len(f)
    L["neg"] += int((f < 0).sum())
    L["pos"] += int((f > 0).sum())
    L["zero"] += int((f == 0).sum())
    L["cneg"] += int((o < 0).sum())
    L["cpos"] += int((o > 0).sum())
    L["czero"] += int((o == 0).sum())
    L["cother"] += len(o)
    L["parts_with_fee"] += 1 if len(f) else 0
    print(f"  date={d}  rows={len(led):>7,}  FEE-MGMT={len(f):>6,}  "
          f"NEG {int((f < 0).sum()):>6,} / POS {int((f > 0).sum()):>3,} / ZERO {int((f == 0).sum()):>3,}"
          f"   signed sum {f.sum():>15,.2f}")
print(f"\n  TOTAL ledger rows read              : {L['rows']:,} across {len(DATES)} partitions")
print(f"  FEE-MANAGEMENT rows                 : {L['fee']:,} "
      f"(present on {L['parts_with_fee']} of {len(DATES)} partitions)")
print(f"    signed_amount NEGATIVE            : {L['neg']:,} of {L['fee']:,}")
print(f"    signed_amount POSITIVE            : {L['pos']:,} of {L['fee']:,}")
print(f"    signed_amount ZERO                : {L['zero']:,} of {L['fee']:,}")
print(f"  CONTROL -- non-FEE-MANAGEMENT rows  : {L['cother']:,} "
      f"(NEG {L['cneg']:,} / POS {L['cpos']:,} / ZERO {L['czero']:,})")
print("    -> the same column, same reader, reads BOTH signs on the control population,")
print("       so an all-negative fee read is a property of the FEE CLASS, not the instrument.")

# ------------------------------------------------------ LEG 2: the signed stored gap
rule("LEG 2 -- STORED twr_daily: SIGNED gap r_gross - r_net, fee-day vs non-fee-day")
tot = {"ok": 0, "fee": 0, "nonfee": 0, "neg": 0, "pos": 0, "zero": 0, "eq": 0}
skipped, worst, resid_max, addback_neg = [], None, 0.0, 0
for d in DATES:
    df = pd.read_parquet(f"{ROOT}/twr_daily_{d}/data.parquet")
    cens = df["status"].value_counts().to_dict()
    ok = df[df["status"] == "OK"].copy()
    missing = [c for c in CFCOLS if c not in df.columns]
    if missing:
        skipped.append((d, len(df), len(ok), missing, cens))
        print(f"  date={d}  rows={len(df):>6,}  OK={len(ok):>6,}  "
              f"NOT-EVALUABLE-BY-SCHEMA (absent: {','.join(missing)})  status={cens}")
        continue
    for c in ("r_net", "r_gross") + CFCOLS:
        ok[c] = pd.to_numeric(ok[c], errors="coerce")
    # FEE-DAY discriminator is INTERNAL to the artifact: nothing but the fee limb moves
    # cf_gross off cf_net (c02_twr_engine.py:286), so it needs no join.
    ok["addback"] = ok["cf_gross"] - ok["cf_net"]
    ok["gap"] = ok["r_gross"] - ok["r_net"]          # SIGNED. never abs.
    feed, nonf = ok[ok["addback"] != 0.0], ok[ok["addback"] == 0.0]
    tot["ok"] += len(ok)
    tot["fee"] += len(feed)
    tot["nonfee"] += len(nonf)
    tot["neg"] += int((feed["gap"] < 0).sum())
    tot["pos"] += int((feed["gap"] > 0).sum())
    tot["zero"] += int((feed["gap"] == 0).sum())
    tot["eq"] += int((nonf["r_net"] == nonf["r_gross"]).sum())
    addback_neg += int((feed["addback"] < 0).sum())
    line = (f"  date={d}  rows={len(df):>6,}  OK={len(ok):>6,}  fee-days={len(feed):>5,}  "
            f"non-fee={len(nonf):>6,}")
    if len(feed):
        g = feed["gap"]
        r = float((g - (-(feed['addback']) / feed['bmv'])).abs().max())
        resid_max = max(resid_max, r)
        line += (f" | SIGNED gap min {g.min():+.6f} med {g.median():+.6f} max {g.max():+.6f}"
                 f" | NEG {int((g < 0).sum()):,}/POS {int((g > 0).sum()):,}/ZERO {int((g == 0).sum()):,}"
                 f" | resid {r:.1e}")
        row = feed.loc[g.idxmin()]
        if worst is None or row["gap"] < worst["gap"]:
            worst = {"date": d, **{k: row[k] for k in
                     ("account_id", "bmv", "emv", "cf_net", "cf_gross", "r_net", "r_gross", "gap")}}
    line += f" | non-fee EXACT-EQ {int((nonf['r_net'] == nonf['r_gross']).sum()):,}"
    print(line)

rule(f"TOTALS -- {len(DATES) - len(skipped)} of {len(DATES)} partitions EVALUABLE")
if skipped:
    print(f"  NOT-EVALUABLE-BY-SCHEMA ({len(skipped)}): "
          + ", ".join(f"{d} (OK={o:,})" for d, _, o, _, _ in skipped))
    print("    -> each carries ZERO OK rows, so c02 never wrote the cf/bmv/emv columns there.")
    print("       A partition that could not be asked is NOT a partition that answered NO.")
print(f"  OK account-days evaluated                    : {tot['ok']:,}")
print(f"  fee-days (cf_gross != cf_net)                : {tot['fee']:,}")
print(f"    addback (cf_gross - cf_net) NEGATIVE       : {addback_neg:,} of {tot['fee']:,}")
print(f"  SIGNED gap NEGATIVE  (r_gross < r_net)       : {tot['neg']:,} of {tot['fee']:,}")
print(f"  SIGNED gap POSITIVE  (r_gross > r_net)       : {tot['pos']:,} of {tot['fee']:,}")
print(f"  SIGNED gap ZERO                              : {tot['zero']:,} of {tot['fee']:,}")
print(f"  NEGATIVE CONTROL non-fee-day exact equality  : {tot['eq']:,} of {tot['nonfee']:,}")
print(f"  identity gap == -(cf_gross-cf_net)/bmv, max resid : {resid_max:.3e}")

if worst:
    rule("THE MOST NEGATIVE STORED ACCOUNT-DAY -- hand-checkable in six numbers")
    for k, v in worst.items():
        print(f"    {k:12s} = {v}")
    b, e = float(worst["bmv"]), float(worst["emv"])
    cn, cg = float(worst["cf_net"]), float(worst["cf_gross"])
    ab = cg - cn
    print(f"\n    addback (cf_gross - cf_net) = {ab:+,.2f}     fee_cf = {-ab:+,.2f}")
    print(f"    r_net             (emv - cf_net)/bmv - 1            = {(e - cn) / b - 1:+.8f}")
    print(f"    r_gross AS STORED (emv - cf_gross)/bmv - 1          = {(e - cg) / b - 1:+.8f}")
    print(f"    r_gross SIBLING   (emv - cf_net + addback)/bmv - 1  = {(e - cn + ab) / b - 1:+.8f}")
    print(f"\n    STORED  gap = {(e - cg) / b - 1 - ((e - cn) / b - 1):+.8f}   "
          f"(= -addback/bmv -- the fee removed a SECOND time)")
    print(f"    SIBLING gap = {(e - cn + ab) / b - 1 - ((e - cn) / b - 1):+.8f}   "
          f"(= +addback/bmv -- the sec8 add-back identity)")
