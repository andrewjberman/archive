"""CF-3b, MEASUREMENT FIRST (CTO 76329 / COO 76335, non-gating).

The question: of the code-rule INTERNAL IN-KIND legs currently REFUSED because the transaction
code establishes no counterparty, how many would a cross-account pair-scan actually GRADUATE --
same business_date, same CUSIP, opposite-direction quantity, in a DIFFERENT account?

This is a read, not a mechanism. Nothing is changed. The point is to size the graduation before
proposing any code, because the residue's $1,067,868.77 pooled bound is an upper limit on what
could graduate and the realised number may be far smaller.

DIRECTION comes from the c00 1.2 field `in_kind_signed_value` (sign) -- the same source c00 uses,
so no second direction instrument is invented here.

Two failure modes named up front, because both would inflate the graduation count:
  - AMBIGUITY: >2 candidate legs on one (date, cusip, |qty|) key. Counted separately, never
    silently paired.
  - SELF-PAIRING: a leg matching another leg of the SAME account is not a counterparty.
"""
import importlib.util
import json
import sys
from pathlib import Path

RUNNERS = Path("data/assets/scripts/gold/runners_49f").resolve()
sys.path.insert(0, str(RUNNERS))
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

spec = importlib.util.spec_from_file_location("c00x", RUNNERS / "c00_flow_ledger.py")
c00 = importlib.util.module_from_spec(spec)
sys.modules["c00x"] = c00
spec.loader.exec_module(c00)

DATES = ["2026-08-26", "2026-08-25", "2026-08-24", "2026-08-21", "2026-08-20", "2026-08-19"]
out = []
for d in DATES:
    trn = rc.read_partition(f"{rc.SILVER}/fact_trn", d)
    ref = rc.read_partition(f"{rc.OUT_ROOT}/reference/ref_txn_classification", d)
    bnd = rc.read_partition(f"{rc.OUT_ROOT}/dimensions/dim_boundary", d)
    px = rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_positions", d,
                           columns=["cusip", "closing_price"])
    src = trn[[c for c in c00.TRN_COLS if c in trn.columns]]
    led, _ = c00.build_flow_ledger(src, ref, bnd, px, asof=d)
    # ⛔ `cusip` DOES NOT SURVIVE INTO THE EMITTED LEDGER (not in c00's out_cols), so the
    # pair-scan CTO 76329 specifies -- "same day, same CUSIP, opposite-direction quantity in
    # ANOTHER account's ledger" -- CANNOT be run against flow_ledger alone. Recovered here by
    # txn_ref, whose suffix is the ORIGINAL fact_trn positional index (c00 assigns txn_ref
    # BEFORE the classification merge resets it). This is a measurement workaround, and the
    # fact that it is needed is itself the finding: a production CF-3b needs either cusip
    # carried into the ledger or this join made explicit.
    idx = led["txn_ref"].astype(str).str.rsplit(":", n=1).str[-1].astype(int)
    led["cusip"] = idx.map(src["cusip"].astype(str)).values
    ic = led["is_in_kind"].astype(bool)
    refused = led[(led["final_class"] == "INTERNAL")
                  & (led["resolution_provenance"] == "code-rule") & ic].copy()
    if not len(refused):
        out.append({"date": d, "refused_legs": 0, "graduated": 0, "ambiguous": 0,
                    "self_only": 0, "unmatched": 0, "refused_abs": 0.0, "graduated_abs": 0.0})
        print(f"  {d}: no code-rule INTERNAL in-kind legs")
        continue
    # candidate pool = EVERY in-kind leg on the partition, any class -- a counterparty need not
    # itself be code-rule INTERNAL, and restricting the pool would understate graduation.
    pool = led[ic].copy()
    pool["absq"] = pd.to_numeric(pool["quantity"], errors="coerce").fillna(0.0).abs().round(6)
    pool["sgn"] = pd.to_numeric(pool["in_kind_signed_value"], errors="coerce").fillna(0.0)
    refused["absq"] = pd.to_numeric(refused["quantity"], errors="coerce").fillna(0.0).abs().round(6)
    refused["sgn"] = pd.to_numeric(refused["in_kind_signed_value"], errors="coerce").fillna(0.0)

    # ⛔ POSITIVE CONTROL, MANDATORY, RUN BEFORE THE VERDICT IS BELIEVED. A uniform 0-of-N is
    # the signature of a broken instrument at least as often as a real absence, and TWO things
    # here could produce a false uniform zero: the txn_ref->cusip recovery could be misaligned,
    # or the sign/quantity comparison could be wrong. So run the SAME scan against the rows
    # c00's OWN pair-match stage already matched -- those are KNOWN to have a cross-account
    # counterparty. If the scan cannot find THOSE, its zero on the refused set means nothing.
    known = led[ic & (led["resolution_provenance"] == "pair-match")].copy()
    known["absq"] = pd.to_numeric(known["quantity"], errors="coerce").fillna(0.0).abs().round(6)
    known["sgn"] = pd.to_numeric(known["in_kind_signed_value"], errors="coerce").fillna(0.0)
    ctrl_hit = 0
    for i, r in known.iterrows():
        cand = pool[(pool["cusip"] == r["cusip"]) & (pool["absq"] == r["absq"])
                    & (pool.index != i) & (pool["account_id"] != r["account_id"])]
        if len(cand):
            ctrl_hit += 1
    print(f"    POSITIVE CONTROL on {len(known)} known pair-matched in-kind legs: "
          f"scan finds a cross-account candidate for {ctrl_hit} of {len(known)}"
          + ("  -- INSTRUMENT LIVE" if ctrl_hit else
             "  *** INSTRUMENT DEAD -- the 0 below is meaningless ***"))

    grad = amb = selfonly = unm = 0
    grad_abs = 0.0
    for i, r in refused.iterrows():
        cand = pool[(pool["cusip"] == r["cusip"]) & (pool["absq"] == r["absq"])
                    & (pool.index != i)]
        if not len(cand):
            unm += 1
            continue
        cross = cand[cand["account_id"] != r["account_id"]]
        if not len(cross):
            selfonly += 1
            continue
        opp = cross[(cross["sgn"] * r["sgn"]) < 0]
        if not len(opp):
            unm += 1
            continue
        if len(opp) > 1:
            amb += 1          # >1 candidate counterparty: NOT silently picked
            continue
        grad += 1
        grad_abs += abs(float(r["sgn"]))
    rec = {"date": d, "control_known_legs": int(len(known)),
           "control_found": ctrl_hit, "control_live": bool(ctrl_hit and len(known)),
           "refused_legs": int(len(refused)),
           "refused_abs": round(float(refused["sgn"].abs().sum()), 2),
           "graduated": grad, "graduated_abs": round(grad_abs, 2),
           "ambiguous": amb, "self_only": selfonly, "unmatched": unm}
    out.append(rec)
    print(f"  {d}: refused={rec['refused_legs']:>4} (${rec['refused_abs']:>14,.2f}) -> "
          f"GRADUATE={grad:>4} (${grad_abs:>13,.2f}) | ambiguous={amb} self-only={selfonly} "
          f"unmatched={unm}")

live = [r for r in out if r.get("control_live")]
dead = [r for r in out if r["refused_legs"] and not r.get("control_live")]
lr = sum(r["refused_legs"] for r in live)
lra = sum(r["refused_abs"] for r in live)
lg = sum(r["graduated"] for r in live)
lga = sum(r["graduated_abs"] for r in live)
dr = sum(r["refused_legs"] for r in dead)
dra = sum(r["refused_abs"] for r in dead)
tr = sum(r["refused_legs"] for r in out)
tg = sum(r["graduated"] for r in out)
tra = sum(r["refused_abs"] for r in out)
tga = sum(r["graduated_abs"] for r in out)
print(f"\n===== CF-3b, pooled over {len(DATES)} partitions")
print(f"  code-rule INTERNAL in-kind legs REFUSED : {tr:>6}   ${tra:>16,.2f}")
print(f"  would GRADUATE on a cross-account scan  : {tg:>6}   ${tga:>16,.2f}"
      f"   ({100.0*tg/max(1,tr):.1f}% of legs, {100.0*tga/max(1e-9,tra):.1f}% of value)")
print(f"  AMBIGUOUS (>1 candidate, never picked)  : {sum(r['ambiguous'] for r in out):>6}")
print(f"  self-account matches only (not a cpty)  : {sum(r['self_only'] for r in out):>6}")
print(f"  no opposite-direction cross-account leg : {sum(r['unmatched'] for r in out):>6}")
print("")
print("===== AND THE SPLIT THE POSITIVE CONTROL FORCES -- a zero is only evidence where the")
print("      instrument was SHOWN able to find a match on that same partition:")
print(f"  CONTROLLED (control fired): refused {lr} legs / ${lra:,.2f} -> GRADUATE {lg} / ${lga:,.2f}")
print("  UNCONTROLLED (no known pair-matched in-kind leg existed on that partition, so the")
print(f"      scan could not be shown live there): refused {dr} legs / ${dra:,.2f} -- NOT EVIDENCE")
print("  Reporting these pooled as a single 0 of 39 would claim controlled coverage this")
print("  measurement does not have.")
Path(sys.argv[1] if len(sys.argv) > 1 else "cf3b.json").write_text(
    json.dumps({"per_date": out,
                "pooled_all": {"refused_legs": tr, "graduated": tg,
                               "refused_abs": round(tra, 2), "graduated_abs": round(tga, 2)},
                "controlled": {"refused_legs": lr, "refused_abs": round(lra, 2),
                               "graduated": lg, "graduated_abs": round(lga, 2)},
                "uncontrolled_not_evidence": {"refused_legs": dr, "refused_abs": round(dra, 2)},
                "note": ("A zero is evidence only on a partition where the scan was SHOWN able "
                         "to find a cross-account match. Pooling controlled and uncontrolled "
                         "partitions into one 0-of-39 would overclaim coverage.")}, indent=2),
    encoding="utf-8")
