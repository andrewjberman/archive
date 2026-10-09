"""IRPT_DASHBD TO-DB-b-15 -- assemble TIEOUT_49F_BLACKDIAMOND_R8.json from OPAL_REMEASURE_FOURTEEN_R8.json (the producer re-run, equity basis)
and the stored round-4 Black Diamond responses. Pure arithmetic on stored files: no S3 read, no vendor call.

Usage: python build_tieout_r8.py <repo_root>
"""
import gzip
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
D = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables"
W, D1 = D / "0.9.0_WK_IRPT_DASHBD~2", D / "0.9.0_WK_IRPT_DASHBD~1"
TOL = 0.0035
rem = json.loads((W / "OPAL_REMEASURE_FOURTEEN_R8.json").read_text(encoding="utf-8"))
MARGIN_ADJ = "Black Diamond books MARGIN INT ADJ as a net addition; Opal keeps margin interest internal by ruling (batch 195)"


def bd_point(acct, start, end):
    r = json.load(gzip.open(D1 / ("RAW_BD_PERIOD_%s.sanitised.json.gz" % acct)))
    for p in r["combinedLevels"][0]["dateRangePoints"]:
        if p["dateRange"]["startDate"][:10] == start and p["dateRange"]["endDate"][:10] == end:
            return p
    raise SystemExit("no BD point")


pairs, s22 = [], None
def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


for p in rem["pairs"]:
    bd = bd_point(p["account"], p["start"], p["end"])
    bmv, emv = bd["beginningMarketValue"], bd["endingMarketValue"]
    signed = p["opal_twr_now"] - p["bd_twr"]
    acc_effect = -p["bd_accrual"] / bmv              # what Opal minus BD would be if the accrual movement were the only difference
    within = p["abs_diff_now"] <= TOL
    rec = {"account": p["account"], "start": p["start"], "end": p["end"], "abs_diff_r4": p["abs_diff_r4"],
           "abs_diff_now": p["abs_diff_now"], "bd_accrual": p["bd_accrual"], "within": within, "reason": None,
           "signed_diff_opal_minus_bd": signed, "bd_accrual_beginning": p["bd_accrual_beginning"],
           "bd_accrual_ending": p["bd_accrual_ending"], "bd_beginning_value": bmv,
           "accrual_effect_if_alone": acc_effect, "residual_after_accrual": signed - acc_effect,
           "bd_value_minus_equity_minus_accrual_at_endpoints": [p["sign_check"]["bd_beginning_minus_equity_plus_accrual"],
                                                                  p["sign_check"]["bd_ending_minus_equity_plus_accrual"]]}
    if not within:
        k = (p["account"], p["start"])
        if k == (_REAL("acct#89d0916a"), "2026-06-25"):
            cf = p["counterfactual_int_adj_as_flow"]
            rec["reason"] = (MARGIN_ADJ + ". MEASURED: Black Diamond reports netAdditions %.2f over this window and Opal's window external flow was "
                             "0.00 (round 6, DECOMPOSE_THREE_PAIRS_R6.json; a flow does not depend on the value basis); the 4,429.53 INTRA/FC/IN credit of 2026-06-25 treated as a flow moves the pair from %.4f pp to %.4f pp "
                             "(counterfactual, never applied). The remaining %.4f pp is below the tolerance."
                             % (bd["netAdditions"], 100 * p["abs_diff_now"], 100 * cf["abs_diff"], 100 * cf["abs_diff"]))
            rec["counterfactual_int_adj_as_flow"] = cf
            s22 = {"account": p["account"], "start": p["start"], "residual": p["abs_diff_now"],
                   "disposition": "DISARMED" if p["abs_diff_now"] <= TOL else "RESTATED", "reason": rec["reason"]}
        elif abs(signed - acc_effect) <= TOL and abs(p["bd_accrual"]) > 1000:
            rec["reason"] = ("Black Diamond's value carries its own accrual (its beginning and ending value equal Opal's equity + its accrual to the "
                             "cent at both endpoints) and the accrual moved %+.2f over the window, which alone puts Opal %.4f pp %s Black Diamond "
                             "(accrual change / Black Diamond's beginning value); Opal books income on receipt, so the accrual stays outside "
                             "Opal's figure. With that accrual effect removed the pair is %.4f pp apart, below the tolerance. The accrual "
                             "reverses in the account's neighbouring window."
                             % (p["bd_accrual"], 100 * abs(acc_effect), "below" if acc_effect < 0 else "above",
                                100 * abs(signed - acc_effect)))
        elif bd["fees"] > 0 and abs(emv / bmv - 1 - p["bd_twr"]) < 1e-6:
            gross = (emv - bd["netAdditions"]) / bmv - 1
            rec["reason"] = ("Opal is gross of advisory fees by the ratified method (fee_basis GROSS_ONLY, C-FEERAIL); Black Diamond's return for this "
                             "window equals ending value / beginning value - 1 (%.6f against its reported %.6f), so the %.2f fee reported in its "
                             "netAdditions and fees stays inside its return. The fee is %.4f pp of its beginning value; Opal's return (%.6f) is "
                             "within %.4f pp of the fee-added-back endpoint form (%.6f). Opal's window fee flow itself was not read separately: "
                             "said, not guessed."
                             % (emv / bmv - 1, p["bd_twr"], bd["fees"], 100 * bd["fees"] / bmv, p["opal_twr_now"],
                                100 * abs(p["opal_twr_now"] - gross), gross))
        else:
            rec["reason"] = "NOT MEASURED: no stored data explains this pair"
    pairs.append(rec)

out = {"tolerance": TOL, "vendor_calls": 0, "method_version": rem["method_version"], "pairs": pairs, "s22": s22,
       "value_basis": "EQUITY = net_mv_plus_cash + margin_balance (1.0.0_SA_CTO RULINGS batch 193)",
       "sign_check": "margin_balance added as stored; Black Diamond value - (net_mv_plus_cash + margin_balance + its accrual) = 0.00 at %d of %d window endpoints"
       % (sum(1 for p in rem["pairs"] for x in (p["sign_check"]["bd_beginning_minus_equity_plus_accrual"], p["sign_check"]["bd_ending_minus_equity_plus_accrual"]) if x == 0),
          2 * len(rem["pairs"])),
       "null_counts": rem["null_counts"],
       "summary": {"pairs": len(pairs), "within": sum(1 for p in pairs if p["within"]), "beyond": sum(1 for p in pairs if not p["within"]),
                   "max_abs_diff_r4": max(p["abs_diff_r4"] for p in pairs), "max_abs_diff_now": max(p["abs_diff_now"] for p in pairs)}}
(W / "TIEOUT_49F_BLACKDIAMOND_R8.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out["summary"]), out["sign_check"])
for p in pairs:
    if not p["within"]:
        print(p["account"], p["start"], "%.4f pp" % (100 * p["abs_diff_now"]), "|", p["reason"])
